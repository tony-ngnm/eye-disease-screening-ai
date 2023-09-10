from __future__ import annotations

import io

import streamlit as st
from PIL import Image
from streamlit_cropperjs import st_cropperjs

from eye_screening import questionnaire as q
from eye_screening.content import CONDITIONS
from eye_screening.inference import classify_image, load_condition_images, load_model
from eye_screening.ui_components import inject_custom_css, render_condition_card, render_guidance


def ask_yes_no_block(question_set: q.QuestionSet, answer_list: list[str]) -> None:
    """Render a block of yes/no questions, appending "Yes" answers' keys.

    Args:
        question_set: The questions and their corresponding answer keys.
        answer_list: Running list of collected symptom keys (mutated in
            place, matching the original app's accumulation pattern).
    """
    for question, key in zip(question_set.questions, question_set.keys):
        if st.selectbox(question, q.CHOICES) == "Có":
            answer_list.append(key)


def handle_normal_eye(images: dict[str, Image.Image]) -> None:
    """Branch for a 'Normal' (healthy-looking) classification.

    Runs a differential questionnaire since some stroke symptoms can
    present with eye-related complaints; flags urgent care when enough
    overlapping symptoms are present.
    """
    st.success("**KHÔNG CÓ DẤU HIỆU CỦA BỆNH MẮT**")
    st.caption(
        "***Hãy trả lời trắc nghiệm dưới đây nhằm đảm bảo bạn không gặp "
        "bệnh nào ở mắt***"
    )
    st.divider()

    answer_list: list[str] = []
    ask_yes_no_block(q.NORMAL_EYE_DIFFERENTIAL, answer_list)

    if not st.button("Kết quả"):
        return

    if not answer_list:
        st.success("**MẮT CỦA BẠN HIỆN ĐANG TRONG TÌNH TRẠNG TỐT**")
        return

    if answer_list == ["đau mắt"]:
        st.error("**BẠN CẦN PHẢI ĐẾN BỆNH VIỆN GẤP**")
        st.info("Bạn có thể đang mắc các dấu hiệu nguy hiểm của bệnh mắt khác")
        return

    if answer_list[-1] == "chấn thương":
        st.error("**BẠN CẦN ĐẾN BỆNH VIỆN GẤP**")
        st.info("Bạn có thể đang mắc các triệu chứng liên quan đến các bệnh nguy hiểm khác")
        return

    # Overlapping neurological symptoms alongside eye complaints:
    # flag as a stroke-related differential, not an eye-only condition.
    st.error("**BẠN CẦN ĐẾN BỆNH VIỆN GẤP**")
    st.info("BẠN ĐANG CÓ NHỮNG DẤU HIỆU CỦA CHỨNG ĐỘT QUỴ")
    st.divider()
    card = st.container(border=True)
    render_condition_card(card, CONDITIONS["stroke"])


def handle_eye_surface_conditions(images: dict[str, Image.Image]) -> None:
    """Branch for Conjunctivitis / Dry Eye / Corneal Ulcer predictions.

    Runs the primary functional-symptom questionnaire, then routes to
    condition-specific guidance based on which symptom pattern the
    answers match.
    """
    st.error("**CÓ DẤU HIỆU MẮT ĐỎ**")
    st.caption(
        "***Hãy trả lời trắc nghiệm dưới đây nhằm phân loại mức độ nguy "
        "hiểm của mắt đỏ mà bạn đang mắc phải***"
    )
    st.divider()

    # First 10 questions map 1:1 to a symptom key. The 11th question
    # ("how much discharge?") only makes sense as a follow-up, so it's
    # only shown when the most recently recorded symptom was "đổ ghèn"
    # (eye discharge) — matching the original app's conditional logic.
    answer_list: list[str] = []
    ask_yes_no_block(
        q.QuestionSet(q.PRIMARY_SYMPTOMS.questions[:-1], q.PRIMARY_SYMPTOMS.keys),
        answer_list,
    )
    if answer_list and answer_list[-1] == "đổ ghèn":
        discharge_amount = st.selectbox(
            q.PRIMARY_SYMPTOMS.questions[-1], q.CONTACT_LENS_CHOICES
        )
        answer_list.append(discharge_amount)

    # Always asked, independent of the above answers. Used only to decide
    # whether contact-lens-specific care tips are shown later — it does
    # NOT factor into the symptom-pattern matching below.
    check_var: list[str] = []
    if st.selectbox("Câu hỏi thêm: Bạn có đeo kính áp tròng không?", q.CHOICES) == "Có":
        check_var.append("kính áp tròng")

    if not st.button("Kết quả"):
        return

    if not answer_list:
        _render_combined_mild_case(images, [])
        return

    if tuple(answer_list) in (q.ALL_SYMPTOMS_PATTERN, q.ALL_SYMPTOMS_LIGHT_DISCHARGE_PATTERN):
        _render_all_three_urgent(images, check_var)
    elif tuple(answer_list) == q.CONJUNCTIVITIS_PATTERN:
        _render_single_condition(
            images, "conjunctivitis",
            severity="**CÓ THỂ ĐIỀU TRỊ TẠI NHÀ VÀ QUAN SÁT THÊM**",
            summary="Bạn có thể đang mắc các dấu hiệu liên quan đến bệnh viêm kết mạc",
            level="warning",
            check_var=check_var,
        )
    elif tuple(answer_list) == q.DRY_EYE_PATTERN:
        _render_single_condition(
            images, "dry_eye",
            severity="**CÓ THỂ ĐIỀU TRỊ TẠI NHÀ VÀ QUAN SÁT THÊM**",
            summary="Bạn có thể đang mắc các dấu hiệu liên quan đến hội chứng khô mắt",
            level="warning",
            check_var=check_var,
        )
    elif tuple(answer_list) == q.CORNEAL_ULCER_PATTERN:
        _render_single_condition(
            images, "corneal_ulcer",
            severity="**BẠN CẦN PHẢI ĐẾN BỆNH VIỆN GẤP**",
            summary="Bạn có thể đang mắc các dấu hiệu nguy hiểm liên quan đến bệnh viêm loét giác mạc",
            level="error",
            check_var=check_var,
        )
    else:
        _render_combined_mild_case(images, check_var)


def _render_all_three_urgent(images: dict[str, Image.Image], check_var: list[str]) -> None:
    st.error("**BẠN CẦN PHẢI ĐẾN BỆNH VIỆN GẤP**")
    st.info(
        "Bạn có thể đang mắc các dấu hiệu liên quan đến bệnh viêm kết mạc, "
        "hội chứng khô mắt hoặc bệnh viêm loét giác mạc"
    )
    st.divider()
    col1, col2, col3 = st.columns(3)
    for col, condition_id in zip(
        (col1, col2, col3), ("conjunctivitis", "dry_eye", "corneal_ulcer")
    ):
        card = col.container(border=True)
        render_condition_card(card, CONDITIONS[condition_id], images.get(condition_id))

    st.divider()
    col1, col2 = st.columns(2)
    do_items = [
        "Rửa tay thường xuyên cùng với xà phòng.",
        "Vệ sinh chăn gối, khăn lau mặt thường xuyên.",
        "Vệ sinh mặt và mắt thường xuyên.",
    ]
    if check_var:
        do_items += list(q.CONTACT_LENS_TIPS) + [
            "Nếu đang mắc các dấu hiệu hay đang trong quá trình theo dõi, "
            "điều trị các bệnh trên, hãy đổi sang đeo kính gọng thay vì "
            "kính áp tròng."
        ]
    render_guidance(
        col1, col2,
        do_items=do_items,
        dont_items=["Không dùng tay dụi mắt."],
    )


def _render_combined_mild_case(images: dict[str, Image.Image], check_var: list[str]) -> None:
    st.warning("**CÓ THỂ ĐIỀU TRỊ TẠI NHÀ VÀ QUAN SÁT THÊM**")
    st.info(
        "Bạn có thể đang mắc các dấu hiệu liên quan đến bệnh viêm kết mạc "
        "hoặc hội chứng khô mắt"
    )
    st.divider()
    col1, col2 = st.columns(2)
    for col, condition_id in zip((col1, col2), ("conjunctivitis", "dry_eye")):
        card = col.container(border=True)
        render_condition_card(card, CONDITIONS[condition_id], images.get(condition_id))

    st.divider()
    col1, col2, col3 = st.columns(3)
    do_items = [
        "Rửa tay thường xuyên cùng với xà phòng.",
        "Vệ sinh chăn gối, khăn lau mặt thường xuyên.",
        "Vệ sinh mặt và mắt thường xuyên.",
    ]
    if check_var:
        do_items += list(q.CONTACT_LENS_TIPS) + [
            "Nếu đang mắc các triệu chứng hoặc trong quá trình điều trị, "
            "theo dõi các bệnh trên, hãy đổi sang đeo kính gọng thay vì "
            "kính áp tròng."
        ]
    render_guidance(
        col1, col2,
        do_items=do_items,
        dont_items=["Không dùng tay dụi mắt."],
        watch_col=col3,
        watch_items=[
            "Triệu chứng bệnh không giảm sau 2 tuần.",
            "Xuất hiện các đốm lạ trên mí mắt do đeo kính áp tròng hoặc bị "
            "viêm kết mạc.",
        ],
        urgent_watch_items=[
            "Đau nhức mắt.",
            "Nhạy cảm với ánh sáng.",
            "Thị lực giảm, thị giác bị méo mó hoặc chói sáng.",
            "Bệnh nhân là em bé chưa đủ 1 tháng tuổi.",
        ],
    )


def _render_single_condition(
    images: dict[str, Image.Image],
    condition_id: str,
    severity: str,
    summary: str,
    level: str,
    check_var: list[str],
) -> None:
    getattr(st, level)(severity)
    st.info(summary)
    st.divider()
    card = st.container(border=True)
    render_condition_card(card, CONDITIONS[condition_id], images.get(condition_id))

    st.divider()
    col1, col2, col3 = st.columns(3)

    do_items_by_condition = {
        "conjunctivitis": [
            "Rửa tay thường xuyên cùng với xà phòng.",
            "Vệ sinh chăn gối, khăn lau mặt thường xuyên.",
            "Che miệng và mũi khi hắt hơi.",
        ],
        "dry_eye": [
            "Vệ sinh mắt hằng ngày với nước ấm.",
            "Đặt máy tính ngang hoặc thấp hơn một chút so với tầm mắt, "
            "điều chỉnh độ sáng phù hợp.",
            "Tạo điều kiện cho mắt nghỉ ngơi.",
            "Sử dụng máy lọc không khí hoặc hít thở khí trời.",
        ],
        "corneal_ulcer": [
            "Điều trị tốt và dứt điểm các bệnh mắt và bệnh toàn thân có "
            "nguy cơ gây viêm loét giác mạc.",
            "Cung cấp đủ vitamin A cho mắt.",
            "Sử dụng phương tiện bảo hộ lao động (kính bảo hộ...) để bảo "
            "vệ mắt.",
        ],
    }
    dont_items_by_condition = {
        "conjunctivitis": [
            "Không dùng chung khăn mặt và chăn gối với người nhiễm bệnh.",
            "Không dùng tay dụi mắt.",
            "Không sử dụng lại khăn giấy dùng 1 lần.",
        ],
        "dry_eye": [
            "Hạn chế rượu, bia.",
            "Hạn chế ở trong môi trường khói bụi, khô lạnh hoặc nóng bức.",
            "Không được dừng sử dụng những loại thuốc theo toa khi không "
            "có chỉ định của bác sĩ.",
        ],
        "corneal_ulcer": [
            "Không được tuỳ tiện sử dụng thuốc khi chưa có chỉ định của "
            "bác sĩ.",
        ],
    }
    watch_items_by_condition = {
        "conjunctivitis": (
            [
                "Triệu chứng bệnh không giảm sau 2 tuần.",
                "Xuất hiện các đốm lạ trên mí mắt do đeo kính áp tròng hoặc "
                "bị viêm kết mạc.",
            ],
            [
                "Đau nhức mắt.",
                "Nhạy cảm với ánh sáng.",
                "Thị lực giảm, thị giác bị méo mó hoặc chói sáng.",
                "Bệnh nhân là em bé chưa đủ 1 tháng tuổi.",
            ],
        ),
        "dry_eye": (
            [
                "Triệu chứng bệnh không giảm sau 2 tuần.",
                "Mí mắt có những thay đổi về hình dáng bất thường.",
            ],
            ["Đau nhức mắt.", "Giảm thị lực."],
        ),
    }

    do_items = list(do_items_by_condition[condition_id])
    if check_var:
        do_items += list(q.CONTACT_LENS_TIPS)
    if condition_id == "dry_eye":
        do_items += [
            "Sử dụng thuốc nhỏ mắt.",
            "Bổ sung omega-3 fatty acids (trong cá) (các loại viên nén "
            "hoặc tinh dầu cần có sự đồng ý từ bác sĩ nhãn khoa).",
        ]

    watch_items, urgent_items = watch_items_by_condition.get(condition_id, ([], []))
    render_guidance(
        col1, col2,
        do_items=do_items,
        dont_items=dont_items_by_condition[condition_id],
        watch_col=col3 if watch_items or urgent_items else None,
        watch_items=watch_items,
        urgent_watch_items=urgent_items,
    )


def handle_cataract(images: dict[str, Image.Image]) -> None:
    """Branch for a 'Cataracts_Glaucoma' prediction."""
    st.error("**CÓ DẤU HIỆU CỦA BỆNH ĐỤC THỦY TINH THỂ**")
    st.caption(
        "***Hãy trả lời trắc nghiệm dưới đây nhằm xác định rõ hơn tình "
        "trạng bạn đang gặp phải***"
    )
    st.divider()

    answer_list: list[str] = []
    ask_yes_no_block(q.CATARACT_DIFFERENTIAL, answer_list)

    if not st.button("Kết quả"):
        return

    st.error("**BẠN CẦN ĐẾN BỆNH VIỆN GẤP**")
    st.info("Bạn có thể đang mắc các dấu hiệu liên quan đến bệnh đục thủy tinh thể")
    st.divider()
    card = st.container(border=True)
    render_condition_card(card, CONDITIONS["cataract"], images.get("cataract"))

    st.divider()
    col1, col2 = st.columns(2)
    render_guidance(
        col1, col2,
        do_items=[
            "Ăn nhiều đậu lăng (lentils), hành, tỏi, rau bina (spinach), "
            "bắp cải, giá, đậu và hạt tươi.",
            "Tạo điều kiện cho mắt nghỉ ngơi.",
            "Thư giãn và hít thở khí trời thường xuyên.",
            "Xét nghiệm xem có bị ngộ độc chì hay thủy ngân không? Phát "
            "hiện và điều trị suy giáp, đái tháo đường, tăng cholesterol "
            "và triglycerid máu.",
        ],
        dont_items=["Ngưng hút thuốc lá.", "Không tiếp xúc trực tiếp nắng gắt, tia UV."],
    )


def handle_subconjunctival_hemorrhage(images: dict[str, Image.Image]) -> None:
    """Branch for a 'Subconjunctival hemorrhage' prediction."""
    st.error("**CÓ DẤU HIỆU XUẤT HUYẾT DƯỚI KẾT MẠC**")
    st.caption("***Hãy trả lời trắc nghiệm dưới đây để xác định các tình trạng khác***")
    st.divider()

    answer_list: list[str] = []
    ask_yes_no_block(q.HEMORRHAGE_DIFFERENTIAL, answer_list)

    if not st.button("Kết quả"):
        return

    card = st.container(border=True)
    if answer_list:
        st.error("**BẠN CẦN PHẢI ĐẾN BỆNH VIỆN GẤP**")
        st.info("Tình trạng xuất huyết mắt của bạn có thể đang đi kèm với các bệnh lí nguy hiểm khác")
    else:
        st.warning("**BẠN NÊN GẶP BÁC SĨ NHÃN KHOA**")
        st.info("Bạn hiện đang gặp tình trạng xuất huyết mắt nhưng chưa có các triệu chứng nguy hiểm khác đi kèm")

    st.divider()
    render_condition_card(
        card, CONDITIONS["subconjunctival_hemorrhage"],
        images.get("subconjunctival_hemorrhage"),
    )

    st.divider()
    col1, col2 = st.columns(2)
    render_guidance(
        col1, col2,
        do_items=[
            "Hãy đến gặp bác sĩ nhãn khoa nếu thường xuyên bị xuất huyết "
            "dưới kết mạc.",
            "Nhỏ mắt bằng nước mắt nhân tạo ngày 6 lần có thể làm dễ chịu "
            "vùng mắt. (Lưu ý: nước mắt nhân tạo không có tác dụng làm "
            "tan máu.)",
            "Trong trường hợp xuất huyết dưới kết mạc khi đang điều trị "
            "bệnh bằng các thuốc chống đông: " + q.BLOOD_THINNER_TIPS[0],
        ],
        dont_items=["Không dùng tay dụi mắt khi bị xuất huyết dưới kết mạc."],
    )


def handle_pterygium(images: dict[str, Image.Image]) -> None:
    """Branch for a 'Pterygium' prediction."""
    st.error("**CÓ DẤU HIỆU CỦA BỆNH MỘNG THỊT**")
    st.caption(
        "***Hãy trả lời trắc nghiệm dưới đây nhằm phân loại mức độ nguy "
        "hiểm của bệnh mộng mắt mà bạn đang mắc phải***"
    )
    st.divider()

    answer_list: list[str] = []
    ask_yes_no_block(q.PTERYGIUM_SEVERITY, answer_list)

    if not st.button("Kết quả"):
        return

    card = st.container(border=True)
    if answer_list:
        st.error("**BẠN CẦN PHẢI ĐẾN BỆNH VIỆN GẤP**")
        st.info("Bệnh mộng thịt của bạn đang có dấu hiệu phát triển đến cấp độ III và IV")
    else:
        st.warning("**BẠN NÊN GẶP BÁC SĨ NHÃN KHOA**")
        st.info("Bạn hiện đang gặp dấu hiệu của bệnh mộng thịt nhưng chưa quá nguy hiểm")

    st.divider()
    render_condition_card(card, CONDITIONS["pterygium"], images.get("pterygium"))

    st.divider()
    col1, col2 = st.columns(2)
    render_guidance(
        col1, col2,
        do_items=[
            "Đeo kính râm khi ra đường.",
            "Tránh môi trường khô nóng, nhiều khói bụi hoặc gió.",
            "Thường xuyên nhận biết liệu có sự thay đổi nào trong mắt. "
            "Nếu có mộng thịt, hãy thường xuyên quan sát kích thước, màu "
            "sắc và hình dạng. Ngoài ra, khi nhận thấy bất kỳ các biểu "
            "hiện bất thường ở mắt hãy đến bệnh viện để bác sĩ chẩn đoán "
            "và điều trị kịp thời.",
        ],
        dont_items=[
            "Không nhìn thẳng trực tiếp vào nguồn sáng mạnh.",
            "Hạn chế tiếp xúc với tia UV.",
        ],
    )


BRANCH_HANDLERS = {
    "Normal": handle_normal_eye,
    "Conjunctivitis_Dry Eye Syndrome_Uveitis": handle_eye_surface_conditions,
    "Cataracts_Glaucoma": handle_cataract,
    "Subconjunctival hemorrhage": handle_subconjunctival_hemorrhage,
    "Pterygium": handle_pterygium,
}


def main() -> None:
    """App entrypoint: page setup, image upload/crop, and branch dispatch."""
    inject_custom_css()
    st.title("Hỗ trợ nhận diện một số bệnh nguy hiểm ở mắt")
    st.warning("**ⓘ** *Hãy thu phóng khi chụp để cho ra bức ảnh phù hợp như lưu ý trên!*")

    model = load_model()
    condition_images = load_condition_images()

    uploaded_file = st.file_uploader("Tải ảnh:", key="uploaded_pic")
    if not uploaded_file:
        return

    # Let the user crop to just the eye before classification, matching
    # the original app's capture guidance (only the eye, portrait
    # orientation — see the "LƯU Ý" panel on the project poster).
    raw_bytes = uploaded_file.read()
    cropped_bytes = st_cropperjs(pic=raw_bytes, btn_text="Cắt ảnh", key="crop")
    if not cropped_bytes:
        return

    image = Image.open(io.BytesIO(cropped_bytes)).convert("RGB")
    st.image(image)

    class_label, _ = classify_image(image, model)
    handler = BRANCH_HANDLERS.get(class_label)
    if handler is None:
        st.error(f"Nhãn không xác định: {class_label}")
        return
    handler(condition_images)


if __name__ == "__main__":
    main()
