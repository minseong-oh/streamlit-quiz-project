# JSON 데이터 로더
import json
from pathlib import Path

import streamlit as st

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


@st.cache_data(show_spinner=False)
def load_questions():
    with (DATA_DIR / "questions.json").open(encoding="utf-8") as f:
        return json.load(f)["questions"]


@st.cache_data(show_spinner=False)
def load_types():
    with (DATA_DIR / "types.json").open(encoding="utf-8") as f:
        return json.load(f)
