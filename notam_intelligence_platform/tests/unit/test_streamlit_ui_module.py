"""Smoke test for Streamlit UI module import path."""


def test_ui_module_path_exists() -> None:
    from pathlib import Path

    assert Path("app/ui_streamlit.py").exists()
