from __future__ import annotations

import argparse
import csv
import os

import torch
import yaml
from sklearn.metrics import accuracy_score, f1_score
from torch.optim import AdamW
from torch.utils.data import DataLoader
from tqdm import tqdm
from transformers import AutoTokenizer, get_linear_schedule_with_warmup

from .dataset import HateSpeechDataset
from .model import build_model
from .utils import TrainConfig, config_to_dict, ensure_dir, save_json, set_seed


def evaluate(model, loader, device):
    model.eval()
    preds, labels = [], []
    with torch.no_grad():
        for batch in loader:
            batch = {k: v.to(device) for k, v in batch.items()}
            out = model(**batch)
            pred = out.logits.argmax(dim=1)
            preds.extend(pred.cpu().tolist())
            labels.extend(batch["labels"].cpu().tolist())
    return {
        "accuracy": accuracy_score(labels, preds),
        "macro_f1": f1_score(labels, preds, average="macro"),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()

    with open(args.config, "r", encoding="utf-8") as f:
        cfg = TrainConfig(**yaml.safe_load(f))

    set_seed(cfg.seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    run_dir = os.path.join(cfg.output_root, cfg.run_name)
    best_model_dir = os.path.join(run_dir, "best_model")
    ensure_dir(run_dir)

    tokenizer = AutoTokenizer.from_pretrained(cfg.model_name)
    train_ds = HateSpeechDataset(cfg.train_file, tokenizer, cfg.text_col, cfg.label_col, cfg.max_length)
    valid_ds = HateSpeechDataset(cfg.valid_file, tokenizer, cfg.text_col, cfg.label_col, cfg.max_length)

    train_loader = DataLoader(train_ds, batch_size=cfg.batch_size, shuffle=True)
    valid_loader = DataLoader(valid_ds, batch_size=cfg.eval_batch_size, shuffle=False)

    model = build_model(cfg.model_name, cfg.num_labels).to(device)
    optimizer = AdamW(model.parameters(), lr=cfg.learning_rate, weight_decay=cfg.weight_decay)
    total_steps = len(train_loader) * cfg.epochs
    warmup_steps = int(total_steps * cfg.warmup_ratio)
    scheduler = get_linear_schedule_with_warmup(optimizer, warmup_steps, total_steps)

    best_f1 = -1.0
    log_path = os.path.join(run_dir, "training_log.csv")
    with open(log_path, "w", newline="", encoding="utf-8") as log_f:
        writer = csv.DictWriter(log_f, fieldnames=["epoch", "train_loss", "valid_accuracy", "valid_macro_f1"])
        writer.writeheader()

        for epoch in range(1, cfg.epochs + 1):
            model.train()
            losses = []
            pbar = tqdm(train_loader, desc=f"Epoch {epoch}/{cfg.epochs}")
            for batch in pbar:
                batch = {k: v.to(device) for k, v in batch.items()}
                out = model(**batch)
                loss = out.loss / cfg.gradient_accumulation_steps
                loss.backward()
                losses.append(loss.item())

                optimizer.step()
                scheduler.step()
                optimizer.zero_grad()

                pbar.set_postfix(loss=f"{sum(losses)/len(losses):.4f}")

            metrics = evaluate(model, valid_loader, device)
            row = {
                "epoch": epoch,
                "train_loss": sum(losses) / max(1, len(losses)),
                "valid_accuracy": metrics["accuracy"],
                "valid_macro_f1": metrics["macro_f1"],
            }
            writer.writerow(row)
            print(row)

            if metrics["macro_f1"] > best_f1:
                best_f1 = metrics["macro_f1"]
                ensure_dir(best_model_dir)
                model.save_pretrained(best_model_dir)
                tokenizer.save_pretrained(best_model_dir)

    save_json({"best_valid_macro_f1": best_f1, "config": config_to_dict(cfg)}, os.path.join(run_dir, "metrics.json"))


if __name__ == "__main__":
    main()
