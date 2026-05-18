from __future__ import annotations

import argparse
import os

import pandas as pd
import torch
from sklearn.metrics import classification_report, confusion_matrix
from torch.utils.data import DataLoader
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from .dataset import HateSpeechDataset
from .utils import ensure_dir, save_json


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_dir", required=True)
    parser.add_argument("--test_file", required=True)
    parser.add_argument("--output_dir", required=True)
    parser.add_argument("--text_col", default="text")
    parser.add_argument("--label_col", default="label")
    parser.add_argument("--max_length", type=int, default=256)
    parser.add_argument("--batch_size", type=int, default=32)
    args = parser.parse_args()

    ensure_dir(args.output_dir)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    tokenizer = AutoTokenizer.from_pretrained(args.model_dir)
    model = AutoModelForSequenceClassification.from_pretrained(args.model_dir).to(device)

    ds = HateSpeechDataset(args.test_file, tokenizer, args.text_col, args.label_col, args.max_length)
    loader = DataLoader(ds, batch_size=args.batch_size, shuffle=False)

    model.eval()
    preds, labels = [], []
    with torch.no_grad():
        for batch in loader:
            labels.extend(batch["labels"].tolist())
            batch = {k: v.to(device) for k, v in batch.items()}
            out = model(**batch)
            preds.extend(out.logits.argmax(dim=1).cpu().tolist())

    report = classification_report(labels, preds, output_dict=True)
    cm = confusion_matrix(labels, preds)
    save_json(report, os.path.join(args.output_dir, "classification_report.json"))
    pd.DataFrame(cm).to_csv(os.path.join(args.output_dir, "confusion_matrix.csv"), index=False)

    raw_df = pd.read_csv(args.test_file)
    raw_df["pred"] = preds
    raw_df.to_csv(os.path.join(args.output_dir, "predictions.csv"), index=False)


if __name__ == "__main__":
    main()
