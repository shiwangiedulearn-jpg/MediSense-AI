from pathlib import Path
import streamlit as st


def load_css(*files):
    css = ""

    for file in files:
        css += Path(file).read_text(encoding="utf-8") + "\n"

    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True
    )


def load_js(file):
    js = Path(file).read_text(encoding="utf-8")

    st.components.v1.html(
        f"<script>{js}</script>",
        height=0,
    )