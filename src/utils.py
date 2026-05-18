from __future__ import annotations

import json
import os
import random
from dataclasses import asdict, dataclass

import numpy as np
import torch


@dataclass
class TrainConfig:
    seed: int
    run_name: str
    model_name: str
    num_labels: int
    max_length: int
    batch_size: int
    eval_batch_size: int
    learning_rate: float
    weight_decay: float
    epochs: int
    warmup_ratio: float
    gradient_accumulation_steps: int
    fp16: bool
    train_file: str
    valid_file: str
    text_col: str
    label_col: str
    output_root: str


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def save_json(obj: dict, path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)


def config_to_dict(config: TrainConfig) -> dict:
    return asdict(config)
