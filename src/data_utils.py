from __future__ import annotations

import re

import pandas as pd

WHITESPACE_RE = re.compile(r"\s+")
URL_RE = re.compile(r"https?://\S+|www\.\S+", flags=re.IGNORECASE)
MENTION_RE = re.compile(r"@\w+")
HASHTAG_RE = re.compile(r"#(\w+)")


def clean_text(text: str) -> str:
    text = str(text)
    text = URL_RE.sub(" <URL> ", text)
    text = MENTION_RE.sub(" <USER> ", text)
    text = HASHTAG_RE.sub(r" \1 ", text)
    text = text.strip()
    text = WHITESPACE_RE.sub(" ", text)
    return text


def validate_df(df: pd.DataFrame, text_col: str = "text", label_col: str = "label") -> None:
    missing_cols = {text_col, label_col} - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing required columns: {sorted(missing_cols)}")

    if not df[label_col].isin([0, 1]).all():
        raise ValueError("Label column must contain only 0 or 1.")
