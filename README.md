# Git Actions Demo — Learner Guide

## 🚀 Overview

This repository is a small hands-on demo to teach you how to structure a simple Python project, include a trained model artifact, and add GitHub Actions workflows for CI. Use this repository to practice creating files, running code locally, and implementing CI/CD.

---

## 📁 Repo layout (what’s present)

* `.github/workflows/` — folder for GitHub Actions workflow YAML files
* `.vscode/` — optional editor settings (workspace settings, recommended extensions)
* `src/` — project source code (training, inference, utilities)
* `requirements.txt` — Python dependencies
* `model.joblib` — serialized trained model artifact
* `metrics.json` — evaluation metrics for the model
* `README.md` — this document

---

## ✍️ What each file/folder is for (learner-friendly)

### `.github/workflows/`

**Purpose:** store GitHub Actions workflows. Each `.yml` file here defines a CI job (e.g., install dependencies, run tests, run training, build package).
**Suggested workflows for learners:**

* `ci.yml` — installs dependencies, runs tests and linters, maybe a small smoke-test script
* `package.yml` — builds a wheel or sdist
* `push-model.yml` — (advanced) when tests pass, package `model.joblib` as a release artifact (or upload to artifact store)
  **What to teach:**
* Use `actions/checkout@v4`
* Use caching of pip dependencies
* Use job matrices (different python versions)
* Use secrets safely

---

### `.vscode/`

**Purpose:** share recommended VS Code settings (e.g., formatting, linting, python interpreter)
**Learner tasks:**

* Populate `.vscode/settings.json` with things like:

  ```json
  {
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true
  }
  ```
* Add `.vscode/extensions.json` recommending extensions: e.g.

  ```json
  {
    "recommendations": [
      "ms-python.python",
      "ms-python.vscode-pylance",
      "editorconfig.editorconfig"
    ]
  }
  ```

---

### `src/`

**Purpose:** contain all source code.
**Suggested file-structure (learners should create if missing):**

```
src/
├─ data/                     # optional: sample csvs or data loader stubs  
├─ __init__.py  
├─ train.py                  # training script: load data -> train -> save model & metrics  
├─ predict.py                # inference script: load model -> predict on sample input  
├─ utils.py                  # helper functions (data loading, preprocessing)  
├─ evaluate.py               # functions to compute metrics & dump metrics.json  
└─ tests/
    ├─ test_predict.py       # unit tests for predict / utils  
    └─ test_train_smoke.py   # quick smoke-test for training pipeline  
```

**Examples of what to teach inside files:**
`train.py` (high-level):

```python
# src/train.py
import joblib
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import json

def main():
    X, y = load_iris(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
    m = RandomForestClassifier(n_estimators=10, random_state=42)
    m.fit(X_train, y_train)
    joblib.dump(m, "model.joblib")

    acc = m.score(X_test, y_test)
    with open('metrics.json', 'w') as f:
        json.dump({"accuracy": acc}, f)

if __name__ == "__main__":
    main()
```

`predict.py`:

```python
# src/predict.py
import joblib
import numpy as np

def main():
    model = joblib.load("model.joblib")
    sample = np.array([[5.1, 3.5, 1.4, 0.2]])
    pred = model.predict(sample)
    print(f"Prediction: {pred[0]}")
    # exit 1 on unexpected scenario
    if pred[0] != 0:
        raise RuntimeError("Unexpected class for the test sample")

if __name__ == "__main__":
    main()
```

`evaluate.py`:

```python
# src/evaluate.py
import json
from sklearn.metrics import accuracy_score

def compute_metrics(y_true, y_pred):
    return {"accuracy": accuracy_score(y_true, y_pred)}

def save_metrics(metrics: dict, filepath="metrics.json"):
    with open(filepath, "w") as f:
        json.dump(metrics, f)

# Example usage in train script
```

Unit test (`tests/test_predict.py`):

```python
# src/tests/test_predict.py
import subprocess
import sys

def test_predict_runs_successfully():
    result = subprocess.run([sys.executable, "src/predict.py"], capture_output=True, text=True)
    assert result.returncode == 0, f"Predict script failed: {result.stderr}"
```

---

### `requirements.txt`

**Purpose:** pinned dependencies for local setup + CI
**Learner tasks:**

* Use reproducible versions (e.g., `scikit-learn==1.2.2`, `joblib==1.3.1`, `pytest==7.3.2`)
* Locally install via:

  ```bash
  pip install -r requirements.txt
  ```

---

### `model.joblib`

**Purpose:** serialized model artifact (binary) — used for inference without retraining
**Teaching points:**

* In real-projects, you *do not* commit large models; instead use model registry / artifact store
* For learning demo this is acceptable
* In `predict.py` you will load this with `joblib.load("model.joblib")`

---

### `metrics.json`

**Purpose:** store evaluation metrics (accuracy, precision, recall, etc) produced by training
**What learners should practice:**

* `train.py` or `evaluate.py` should write metrics JSON
* In CI you can read `metrics.json` and fail workflow if metric < threshold

---

## 🧭 Step-by-step: How to create files & run locally

1. **Clone the repo**

   ```bash
   git clone https://github.com/varunchach/git_actions_demo.git
   cd git_actions_demo
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate    # Linux/Mac
   # On Windows PowerShell:
   # .venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Create the `src/` skeleton (if missing)**
   Create folders/files exactly as suggested above.

5. **Run a quick test**

   ```bash
   python src/train.py
   python src/predict.py
   cat metrics.json
   ```

6. **Write unit tests**

   ```bash
   pip install pytest
   pytest -q
   ```

---

## ⚙️ Example GitHub Actions CI (`.github/workflows/ci.yml`)

```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.10, 3.11]
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - name: Cache pip
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run tests
        run: |
          pytest -q
      - name: Smoke predict
        run: |
          python src/predict.py
```

---

## ✅ Best practices & learning checks

* **Don’t commit large binary artifacts** in real projects (use model registry / storage)
* **Pin dependencies** in `requirements.txt` for reproducibility
* **Keep tests fast** — CI should run quick smoke-tests, heavy training belongs scheduled or separate pipeline
* **Use metrics gating**: optionally fail PRs if `metrics.json` shows degraded performance

---

## 🧩 Suggested exercises for learners

1. Implement `train.py` and write `metrics.json`
2. Add `predict.py` and a test that uses the model to predict a known input
3. Create `ci.yml` workflow that runs tests and smoke predict
4. Modify workflow to run on a schedule and store `metrics.json` as an artifact
5. Replace `model.joblib` with a minimal model registry call (or upload artifact from workflow)

---

## 📌 Final notes

This README is tailored to the files present in the repository root layout above. If you add more scripts or folders, update this guide accordingly.

---
