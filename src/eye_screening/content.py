from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Condition:
    id: str
    title_vi: str
    label_en: str
    description_vi: str
    causes_vi: tuple[str, ...] = field(default_factory=tuple)


CONDITIONS: dict[str, Condition] = {
    "stroke": Condition(
        id="stroke",
        title_vi="ĐỘT QUỴ HAY TAI BIẾN MẠCH MÁU NÃO",
        label_en="Stroke (differential warning)",
        description_vi=(
            "Đây là tình trạng não bộ bị tổn thương nghiêm trọng do quá trình "
            "cấp máu não bị gián đoạn hoặc giảm đáng kể khiến não bộ bị thiếu "
            "oxy, không đủ dinh dưỡng để nuôi các tế bào. Tổn thương não ở "
            "đường dẫn truyền thị giác, có thể gây ảnh hưởng thị lực."
        ),
        causes_vi=(
            "Thiếu máu cục bộ.",
            "Xuất huyết.",
            "Bị các bệnh về tim mạch.",
            "Do tuổi tác.",
            "Do hút thuốc.",
            "Do lối sống không lành mạnh hoặc thừa cân, béo phì.",
            "Những trường hợp có nguy cơ cao bị đột quỵ: cao huyết áp, tiểu "
            "đường, cholesterol cao/mỡ máu, rối loạn nhịp tim.",
        ),
    ),
    "conjunctivitis": Condition(
        id="conjunctivitis",
        title_vi="VIÊM KẾT MẠC",
        label_en="Conjunctivitis",
        description_vi=(
            "Viêm kết mạc là tình trạng viêm lớp màng trong suốt ở bề mặt "
            "nhãn cầu (tròng trắng)."
        ),
        causes_vi=(
            "Do dị ứng khói thuốc, động vật... hoặc các yếu tố của môi trường.",
            "Bị lây nhiễm do tiếp xúc với dịch cơ thể (nước bọt, ...).",
            "Do kính áp tròng chưa đảm bảo vệ sinh hoặc kém chất lượng.",
        ),
    ),
    "dry_eye": Condition(
        id="dry_eye",
        title_vi="TÌNH TRẠNG KHÔ MẮT",
        label_en="Dry eye syndrome",
        description_vi=(
            "Tình trạng khô mắt thường xảy ra khi đôi mắt mất đi sự cân bằng "
            "giữa khả năng sản sinh và bốc hơi của film nước mắt."
        ),
        causes_vi=(
            "Do tuổi tác (thường xảy ra với những người ngoài 50 tuổi).",
            "Do đeo kính áp tròng trong khoảng thời gian dài.",
            "Do tiếp xúc lâu với ánh sáng xanh, màn hình điện tử.",
            "Do hoạt động mắt liên tục với cường độ cao (đọc sách, làm việc, ...).",
            "Do tiếp xúc lâu với môi trường khô lạnh, nóng bức hoặc khói bụi.",
            "Do tác hại của bia rượu, thuốc lá.",
            "Do sử dụng các loại thuốc như: thuốc ngủ; thuốc điều trị lo âu, "
            "trầm cảm; beta blocker (thuốc tim mạch); thuốc điều trị ợ nóng; "
            "thuốc kháng sinh, chống dị ứng; thuốc lợi tiểu (Diuretics) điều "
            "trị cao huyết áp.",
        ),
    ),
    "corneal_ulcer": Condition(
        id="corneal_ulcer",
        title_vi="VIÊM LOÉT GIÁC MẠC",
        label_en="Corneal ulcer",
        description_vi=(
            "Viêm loét giác mạc là tình trạng giác mạc bị trầy và bị nhiễm "
            "trùng."
        ),
        causes_vi=(
            "Do giác mạc bị trầy rách hoặc bị nhiễm trùng.",
            "Do thương tích ở mắt (vật lạ va quẹt, khô mắt trầm trọng, ...).",
            "Do thiếu protein và vitamin A.",
            "Do nhiễm vi khuẩn, nấm, vi rút hoặc kí sinh trùng. Trong trường "
            "hợp đã từng bị loét giác mạc do virus, bệnh vẫn có thể tái phát.",
            "Do lông mi mọc vào trong, mi mắt lật vào trong hoặc viêm bờ mi.",
            "Do mi mắt không khép lại đúng cách, dẫn đến giác mạc bị khô và "
            "kích ứng.",
            "Do kính áp tròng chưa đảm bảo vệ sinh hoặc kém chất lượng.",
            "Do sử dụng thuốc nhỏ có chất dexa mà không có chỉ định của bác "
            "sĩ nhãn khoa.",
            "Do các bệnh lí như bệnh đái tháo đường không được kiểm soát.",
        ),
    ),
    "cataract": Condition(
        id="cataract",
        title_vi="ĐỤC THUỶ TINH THỂ",
        label_en="Cataract",
        description_vi=(
            "Bệnh đục thủy tinh thể là hiện tượng đục mờ thủy tinh thể, "
            "không cho ánh sáng chiếu qua, kết quả là võng mạc không nhận "
            "được hình ảnh và thị lực của bệnh nhân sẽ suy giảm dẫn đến mù "
            "lòa."
        ),
        causes_vi=(
            "Có thể do di truyền.",
            "Do mắc các bệnh lí khác như tiểu đường, ...",
            "Do tác hại của thuốc lá hoặc bia rượu.",
            "Gặp chấn thương mắt (có thể sau khi sinh) hoặc đã tiến hành xạ "
            "trị ở nửa trên của cơ thể.",
            "Gặp các vấn đề về gene hay nhiễm sắc thể (ví dụ như hội chứng "
            "Down, hội chứng sản ngoại bì, ...).",
            "Sản phụ gặp các bệnh như rubella, giang mai, HIV, bệnh sởi khi "
            "mang thai có thể gây đục thủy tinh thể bẩm sinh cho thai nhi.",
        ),
    ),
    "subconjunctival_hemorrhage": Condition(
        id="subconjunctival_hemorrhage",
        title_vi="XUẤT HUYẾT DƯỚI KẾT MẠC",
        label_en="Subconjunctival hemorrhage",
        description_vi=(
            "Xuất huyết dưới kết mạc là tình trạng vỡ một hay một vài mạch "
            "máu nhỏ ngay dưới củng mạc (phần lòng trắng của mắt)."
        ),
        causes_vi=(
            "Do va đập, chấn thương vùng mắt hoặc vùng đầu.",
            "Do dụi mắt quá mạnh.",
            "Do hắt hơi, ho mạnh hoặc các hành động mạnh tương tự. Do lặn "
            "quá sâu, cố gắng rặn đẻ hay mang vác đồ nặng, ...",
            "Do bệnh tiểu đường hoặc huyết áp cao.",
            "Do sử dụng thuốc aspirin hay coumadin.",
            "Do rối loạn đông máu, thiếu vitamin C.",
            "Do yếu tố viêm nhiễm vùng mắt như viêm kết mạc do Enterovirus "
            "70, nhiễm xoắn khuẩn Leptospira...",
            "Do dùng thuốc, đặc biệt các thuốc chống đông máu trong điều trị "
            "bệnh lý tim mạch.",
        ),
    ),
    "pterygium": Condition(
        id="pterygium",
        title_vi="MỘNG THỊT",
        label_en="Pterygium",
        description_vi=(
            "Mộng thịt là một trong những bệnh về mắt mà trong đó kết mạc "
            "phát triển, một mô mỏng, rõ ràng bao phủ một phần tròng trắng "
            "của mắt. Mộng mắt ở khóe mắt có thể xảy ra ở một hoặc cả hai "
            "mắt."
        ),
        causes_vi=(
            "Do ánh nắng gắt, tia cực tím.",
            "Do bệnh nhân có tiền sử bị khô mắt có nguy cơ cao mắc bệnh "
            "mộng thịt.",
            "Nam giới có nguy cơ dễ mắc bệnh mộng thịt hơn nữ giới.",
            "Do môi trường khô nóng, cát bụi.",
        ),
    ),
}


def get_condition(condition_id: str) -> Condition:
    return CONDITIONS[condition_id]
