from __future__ import annotations

import argparse
import os

import pandas as pd

from .data_utils import clean_text, validate_df


def preprocess_file(input_path: str, output_path: str, max_text_len: int) -> None:
    df = pd.read_csv(input_path)
    validate_df(df)
    df["text"] = df["text"].astype(str).map(clean_text)
    df = df[df["text"].str.len() > 0].copy()
    df["text"] = df["text"].str.slice(0, max_text_len * 6)
    df.to_csv(output_path, index=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", required=True)
    parser.add_argument("--output_dir", required=True)
    parser.add_argument("--max_text_len", type=int, default=256)
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    for split in ["train", "valid", "test"]:
        inp = os.path.join(args.input_dir, f"{split}.csv")
        out = os.path.join(args.output_dir, f"{split}_clean.csv")
        preprocess_file(inp, out, args.max_text_len)
        print(f"Processed {inp} -> {out}")


if __name__ == "__main__":
    main()
