from __future__ import annotations

from typing import Iterable

import streamlit as st
from PIL import Image

from eye_screening.content import Condition

CARD_IMAGE_SIZE: tuple[int, int] = (200, 127)

_CUSTOM_CSS = """
<style>
.font1bold { font-size: 30px; font-weight: bold; color: #177233; }
.font1 { font-size: 20px; color: #177233; }
.font1urgent { font-size: 20px; color: #177233; font-weight: bold; }
.font2 { font-size: 20px; color: #004280; }
.font2urgent { font-size: 20px; color: #004280; font-weight: bold; }
.font2bold { font-size: 30px; font-weight: bold; color: #004280; }
</style>
"""


def inject_custom_css() -> None:
    st.markdown(_CUSTOM_CSS, unsafe_allow_html=True)


def _p(container: "st.delta_generator.DeltaGenerator", css_class: str, text: str) -> None:
    container.markdown(f'<p class="{css_class}">{text}</p>', unsafe_allow_html=True)


def render_condition_card(
    container: "st.delta_generator.DeltaGenerator",
    condition: Condition,
    image: Image.Image | None = None,
) -> None:
    _p(container, "font1bold", condition.title_vi)
    if image is not None:
        container.image(image.resize(CARD_IMAGE_SIZE))
    _p(container, "font1urgent", f"• {condition.description_vi}")
    if condition.causes_vi:
        _p(container, "font1urgent", "• Nguyên nhân:")
        for cause in condition.causes_vi:
            _p(container, "font1", f"- {cause}")


def render_guidance(
    do_col: "st.delta_generator.DeltaGenerator",
    dont_col: "st.delta_generator.DeltaGenerator",
    do_items: Iterable[str],
    dont_items: Iterable[str],
    watch_col: "st.delta_generator.DeltaGenerator | None" = None,
    watch_items: Iterable[str] | None = None,
    urgent_watch_items: Iterable[str] | None = None,
) -> None:
    _p(do_col, "font2bold", "✔ THỰC HIỆN")
    for item in do_items:
        _p(do_col, "font2", f"• {item}")

    _p(dont_col, "font2bold", "✘ HẠN CHẾ")
    for item in dont_items:
        _p(dont_col, "font2", f"• {item}")

    if watch_col is not None:
        _p(watch_col, "font2bold", "ⓘ THEO DÕI")
        if watch_items:
            _p(watch_col, "font2", "Hãy đi khám nếu:")
            for item in watch_items:
                _p(watch_col, "font2", f"• {item}")
        if urgent_watch_items:
            _p(watch_col, "font2urgent", "Cần đi bệnh viện gấp nếu:")
            for item in urgent_watch_items:
                _p(watch_col, "font2urgent", f"• {item}")
