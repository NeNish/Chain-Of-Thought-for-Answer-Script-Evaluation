# Multilingual Transformer Model for Hate Speech Detection in Code-Mixed Languages

A full project for hate-speech detection on **code-mixed South Asian languages**:
- **Tanglish** (Tamil + English)
- **Hinglish** (Hindi + English)
- **Kanglish** (Kannada + English)

This repository includes:
- Data schema and preprocessing pipeline
- Transformer fine-tuning (XLM-RoBERTa / IndicBERT-ready)
- End-to-end training and evaluation scripts
- Error analysis and confusion matrix generation
- Reproducible experiment configuration

## 1) Project structure

```text
.
├── README.md
├── requirements.txt
├── pyproject.toml
├── configs
│   └── train_xlmr.yaml
├── data
│   ├── raw
│   │   └── README.md
│   └── processed
│       └── .gitkeep
├── src
│   ├── data_utils.py
│   ├── preprocess.py
│   ├── dataset.py
│   ├── model.py
│   ├── train.py
│   ├── evaluate.py
│   └── utils.py
└── notebooks
    └── error_analysis_template.md
```

## 2) Problem definition

Binary classification:
- `0` → non-hate
- `1` → hate

Input format expected in CSV:
- `text` (string)
- `label` (integer 0/1)
- `language` (one of `tanglish`, `hinglish`, `kanglish`)

## 3) Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 4) Data preparation

Place raw files in `data/raw/` with this naming convention:
- `train.csv`
- `valid.csv`
- `test.csv`

Then preprocess:

```bash
python -m src.preprocess \
  --input_dir data/raw \
  --output_dir data/processed \
  --max_text_len 256
```

## 5) Training

```bash
python -m src.train --config configs/train_xlmr.yaml
```

Outputs:
- `artifacts/<run_name>/best_model/`
- `artifacts/<run_name>/metrics.json`
- `artifacts/<run_name>/training_log.csv`

## 6) Evaluation

```bash
python -m src.evaluate \
  --model_dir artifacts/xlmr_codemix_hatespeech/best_model \
  --test_file data/processed/test_clean.csv \
  --output_dir artifacts/xlmr_codemix_hatespeech/eval
```

Saved outputs:
- `classification_report.json`
- `confusion_matrix.csv`
- `predictions.csv`

## 7) Baseline and extension ideas

- Replace `xlm-roberta-base` with `ai4bharat/IndicBERTv2-MLM-only`
- Add class-weighted loss for imbalance
- Add language-aware multitask head (`hate` + `language`)
- Apply focal loss and compare macro-F1

## 8) Ethics and safety

This model is a research baseline and may produce harmful errors. Always include:
- Human review before moderation actions
- Bias audits across language groups
- Appeals / override workflow

## 9) Citation

If you use this project, cite the repository and model cards for the pretrained backbone.
