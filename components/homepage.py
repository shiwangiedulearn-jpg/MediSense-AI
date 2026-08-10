from pathlib import Path
import streamlit.components.v1 as components


def show_homepage():

    html = Path("assets/html/home.html").read_text(encoding="utf-8")

    css = ""

    css += Path("assets/css/home.css").read_text(encoding="utf-8")
    css += Path("assets/css/aurora.css").read_text(encoding="utf-8")
    css += Path("assets/css/cards.css").read_text(encoding="utf-8")
    css += Path("assets/css/buttons.css").read_text(encoding="utf-8")
    css += Path("assets/css/animations.css").read_text(encoding="utf-8")
    components.html(
        f"""
<!DOCTYPE html>

<html>

<head>

<style>

{css}

</style>

<script src="https://cdn.jsdelivr.net/npm/ogl/dist/ogl.min.js"></script>

</head>

<body>

{html}

<script>

{Path("assets/js/aurora.js").read_text(encoding="utf-8")}

</script>

</body>

</html>

""",
        height=820,
        scrolling=False,
    )