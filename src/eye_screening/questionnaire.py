from __future__ import annotations

from dataclasses import dataclass

CHOICES: tuple[str, str] = ("Có", "Không")  # Yes / No
CONTACT_LENS_CHOICES: tuple[str, str] = ("nhiều ghèn", "ít ghèn")  # heavy / light discharge


@dataclass(frozen=True)
class QuestionSet:
    questions: tuple[str, ...]
    keys: tuple[str, ...]


# --------------------------------------------------------------------------- #
# Primary functional-symptom questionnaire
# --------------------------------------------------------------------------- #
PRIMARY_SYMPTOMS = QuestionSet(
    questions=(
        "Câu 1: Bạn có bị đột ngột giảm thị lực không?",
        "Câu 2: Bạn có hay bị đau nhức mắt không?",
        "câu 3: Bạn có hay cảm thấy khó chịu, ngứa rát mắt không?",
        "câu 4: Bạn có hay cảm thấy nóng ngứa ở mắt không?",
        "Câu 5: Bạn có hay bị mỏi mắt không?",
        "Câu 6: Bạn có hay bị chảy nước mắt không?",
        "Câu 7: Bạn có hay cảm giác mắt bị cộm, giống như có dị vật trong "
        "mắt không?",
        "Câu 8: Mắt bạn có bị nhạy cảm với ánh sáng không?",
        "Câu 9: Bạn có hay bị khô mắt không?",
        "Câu 10: Mắt bạn có bị đổ ghèn không?",
        "Câu 11: Nếu có thì đổ ghèn nhiều hay ít",
    ),
    keys=(
        "giảm thị lực",
        "đau nhức mắt",
        "ngứa rát mắt",
        "nóng ngứa mắt",
        "mỏi mắt",
        "chảy nước mắt",
        "cộm mắt",
        "nhạy cảm với ánh sáng",
        "khô mắt",
        "đổ ghèn",
    ),
)

# once PRIMARY_SYMPTOMS has been answered.
CONJUNCTIVITIS_PATTERN: tuple[str, ...] = (
    "nóng ngứa mắt", "chảy nước mắt", "cộm mắt",
    "nhạy cảm với ánh sáng", "đổ ghèn", "nhiều ghèn",
)
DRY_EYE_PATTERN: tuple[str, ...] = (
    "ngứa rát mắt", "mỏi mắt", "chảy nước mắt", "cộm mắt",
    "nhạy cảm với ánh sáng", "khô mắt", "đổ ghèn", "ít ghèn",
)
CORNEAL_ULCER_PATTERN: tuple[str, ...] = (
    "giảm thị lực", "đau nhức mắt", "chảy nước mắt", "cộm mắt",
    "nhạy cảm với ánh sáng",
)
ALL_SYMPTOMS_PATTERN: tuple[str, ...] = (
    "giảm thị lực", "đau nhức mắt", "ngứa rát mắt", "nóng ngứa mắt",
    "mỏi mắt", "chảy nước mắt", "cộm mắt", "nhạy cảm với ánh sáng",
    "khô mắt", "đổ ghèn", "nhiều ghèn",
)
ALL_SYMPTOMS_LIGHT_DISCHARGE_PATTERN: tuple[str, ...] = (
    "giảm thị lực", "đau nhức mắt", "ngứa rát mắt", "nóng ngứa mắt",
    "mỏi mắt", "chảy nước mắt", "cộm mắt", "nhạy cảm với ánh sáng",
    "khô mắt", "đổ ghèn", "ít ghèn",
)

# --------------------------------------------------------------------------- #
# Subconjunctival-hemorrhage differential questionnaire
# --------------------------------------------------------------------------- #
HEMORRHAGE_DIFFERENTIAL = QuestionSet(
    questions=(
        "Câu 1: Bạn có bị đau nhức vùng mắt hay không?",
        "Câu 2: Gần đây, bạn có gặp chấn thương vùng mắt hay đầu không?",
        "Câu 3: Thị lực của bạn có đang gặp vấn đề không? (VD: nhìn mờ, "
        "khó nhìn hoặc nhìn đôi)",
        "Câu 4: Bạn có tiền sử bị bệnh tăng huyết áp không?",
        "Câu 5: Hiện tượng xuất huyết có diễn ra ở hai bên mắt của bạn và "
        "kèm theo xuất huyết ở những chỗ khác như chảy máu mũi, cháy máu "
        "chân răng, nôn ra máu, đi ngoài ra máu,.. không?",
        "Câu 6: Bạn có thấy tình trạng xuất huyết mắt của bạn không có dấu "
        "hiệu thuyên giảm, thậm chí có xu hướng lan rộng hơn ban đầu không?",
    ),
    keys=(
        "đau nhức mắt",
        "chấn thương",
        "thị lực có vấn đề",
        "tiền sử bị tăng huyết áp",
        "xuất huyết 2 bên mắt và chỗ khác",
        "không thuyên giảm",
    ),
)

# --------------------------------------------------------------------------- #
# Healthy-eye / stroke-differential questionnaire
# --------------------------------------------------------------------------- #
NORMAL_EYE_DIFFERENTIAL = QuestionSet(
    questions=(
        "Câu 1: Bạn có bị đau mắt không?",
        "Câu 2: Mắt bạn có hay bị mờ không?",
        "Câu 3: Bạn có hay bị nhìn đôi không?",
        "Câu 4: Khi cười thì mặt bạn có bị méo không?",
        "Câu 5: Bạn có thể nâng hai tay qua đầu không?",
        "Câu 6: Bạn có hay bị đau đầu không?",
        "Câu 7: Bạn có gặp khó khăn trong việc giao tiếp không? (vd: khó "
        "phát âm, nói không rõ chữ, bị dính chữ, nói ngọng bất thường)",
        "Câu 8: Bạn có gặp khó khăn trong việc đi lại hay giữ thăng bằng "
        "không?",
        "Câu 9: Bạn có hay bị buồn nôn, ói không?",
        "Câu 10: Gần đây bạn có bị chấn thương ở vùng đầu không?",
    ),
    keys=(
        "đau mắt", "mờ", "nhìn đôi", "méo", "nâng qua đầu", "đau đầu",
        "khó giao tiếp", "khó", "buồn nôn", "chấn thương",
    ),
)
STROKE_WARNING_KEYS: tuple[str, ...] = (
    "mờ", "nhìn đôi", "méo", "đau đầu", "khó giao tiếp", "khó", "buồn nôn",
)

# --------------------------------------------------------------------------- #
# Cataract differential questionnaire
# --------------------------------------------------------------------------- #
CATARACT_DIFFERENTIAL = QuestionSet(
    questions=(
        "Câu 1: Mắt bạn có bị mờ không?",
        "Câu 2: Mắt bạn có đau không?",
    ),
    keys=("mờ", "đau"),
)

# --------------------------------------------------------------------------- #
# Pterygium severity questionnaire
# --------------------------------------------------------------------------- #
PTERYGIUM_SEVERITY = QuestionSet(
    questions=("Câu 1: Mắt của bạn có bị mờ không?",),
    keys=("mờ",),
)

DRY_EYE_FOLLOWUPS = QuestionSet(
    questions=(
        "Câu 13: Bạn có sử dụng máy tính thường xuyên hay công việc của "
        "bạn có gắn liền với máy tính thường xuyên không?",
        "Câu 14: Bạn có uống rượu, bia không?",
        "Câu 15: Bạn có đang sử dụng thuốc theo toa không?",
    ),
    keys=("máy tính thường xuyên", "rượu, bia", "thuốc theo toa"),
)
DRY_EYE_FOLLOWUP_TIPS: tuple[str, ...] = (
    "Đảm bảo rằng màn hình máy tính nằm ngay tầm mắt hoặc thấp hơn tầm mắt.",
    "Hạn chế rượu, bia.",
    "Không được dừng sử dụng những loại thuốc theo toa khi không có chỉ "
    "định của bác sĩ, kể cả khi bạn nghĩ việc sử dụng thuốc chính là "
    "nguyên nhân của những triệu chứng khô mắt đang mắc phải.",
)

CONTACT_LENS_FOLLOWUP = QuestionSet(
    questions=("Câu 12: Bạn có sử dụng kính áp tròng không?",),
    keys=("kính áp tròng",),
)
CONTACT_LENS_TIPS: tuple[str, ...] = (
    "Sử dụng kính áp tròng theo đúng chỉ định và hướng dẫn của bác sĩ.",
    "Vệ sinh sạch sẽ kính áp tròng trước và sau khi đeo.",
)

BLOOD_THINNER_FOLLOWUP = QuestionSet(
    questions=(
        "Câu 12: Bạn có đang sử dụng thuốc chống đông để điều trị bệnh "
        "(VD: các bệnh về tim mạch) không?",
    ),
    keys=("thuốc chống đông",),
)
BLOOD_THINNER_TIPS: tuple[str, ...] = (
    "Báo cáo với bác sĩ chuyên khoa đang trực tiếp điều trị để điều "
    "chỉnh, thay đổi liều lượng cho phù hợp hoặc có thể cân nhắc việc "
    "chuyển thuốc điều trị khác nếu cần.",
)
