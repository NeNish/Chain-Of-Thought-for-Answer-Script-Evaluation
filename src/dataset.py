from __future__ import annotations

import pandas as pd
import torch
from torch.utils.data import Dataset


class HateSpeechDataset(Dataset):
    def __init__(self, csv_file: str, tokenizer, text_col: str, label_col: str, max_length: int):
        self.df = pd.read_csv(csv_file)
        self.tokenizer = tokenizer
        self.text_col = text_col
        self.label_col = label_col
        self.max_length = max_length

    def __len__(self) -> int:
        return len(self.df)

    def __getitem__(self, idx: int) -> dict[str, torch.Tensor]:
        row = self.df.iloc[idx]
        encoded = self.tokenizer(
            str(row[self.text_col]),
            truncation=True,
            padding="max_length",
            max_length=self.max_length,
            return_tensors="pt",
        )
        item = {k: v.squeeze(0) for k, v in encoded.items()}
        item["labels"] = torch.tensor(int(row[self.label_col]), dtype=torch.long)
        return item
