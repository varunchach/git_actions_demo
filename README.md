# 🧠 GitHub Actions — Python Publish Workflow (Iris Classification CI/CD)

## 🚀 Overview  
This repository demonstrates a **complete Continuous Integration (CI) setup** using **GitHub Actions** for a simple Iris Classification ML project.  
The workflow automatically:
- Installs dependencies  
- Trains the model  
- Runs tests  
- Uploads model artifacts and evaluation metrics  

It ensures your project is **tested and versioned** on every push to the GitHub repository.

---

## ⚙️ Learning Goals
By completing this demo, you will learn:
1. How to automate Python training pipelines using **GitHub Actions**  
2. How to test ML code automatically in a workflow  
3. How to save and version ML artifacts (`model.joblib` and `metrics.json`)  

---

## 📁 Repository Layout
```

git_actions_demo/
├─ .github/
│  └─ workflows/
│       └─ python-publish.yml       # GitHub Actions workflow file
├─ src/
│  ├─ train.py                      # model training script
│  ├─ test_model.py                 # unit test for model
│  └─ predict.py                    # inference script (optional)
├─ model.joblib                     # trained model artifact (created after run)
├─ metrics.json                     # evaluation metrics (created after run)
├─ requirements.txt                 # Python dependencies
└─ README.md

````

---

## 🧩 Step-by-Step — Local Implementation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/varunchach/git_actions_demo.git
cd git_actions_demo
````

---

### 2️⃣ Create and Activate Virtual Environment

```bash
python -m venv venv
.\venv\Scripts\activate         # Windows
# source venv/bin/activate      # Mac/Linux
```

---

### 3️⃣ Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 4️⃣ Run Training and Tests Locally

Train the model manually:

```bash
python src/train.py
```

Run tests:

```bash
python src/test_model.py
```

Check that `model.joblib` and `metrics.json` are created in the repo root.
If both appear successfully, your project is ready for CI/CD automation.

```bash
python -m pytest -v 
```
---

## ☁️ GitHub Actions — Server Implementation

### 🧠 About the Workflow

When you push any changes to GitHub, the following workflow (`python-publish.yml`) executes automatically.

---

### 📜 Workflow File — `.github/workflows/python-publish.yml`

```yaml
name: MLOps Iris Classification

on: [push]

jobs:
  train-and-test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v5
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Train model
      run: python src/train.py
    
    - name: Run tests
      run: python src/test_model.py
    
    - name: Upload model artifact
      uses: actions/upload-artifact@v4
      with:
        name: iris-model
        path: model.joblib
    
    - name: Upload metrics
      uses: actions/upload-artifact@v4
      with:
        name: metrics
        path: metrics.json
```

---

## 🧭 How It Works

| Step | Action                   | Description                                                                                           |
| ---- | ------------------------ | ----------------------------------------------------------------------------------------------------- |
| 1    | **Checkout Repository**  | Pulls your repo code into GitHub runner                                                               |
| 2    | **Set up Python**        | Installs the specified Python version (3.9 here)                                                      |
| 3    | **Install Dependencies** | Installs all required libraries from `requirements.txt`                                               |
| 4    | **Train Model**          | Executes `src/train.py` to train and save the model (`model.joblib`)                                  |
| 5    | **Run Tests**            | Runs `src/test_model.py` to validate model logic or metrics                                           |
| 6    | **Upload Artifacts**     | Saves generated files (`model.joblib`, `metrics.json`) as downloadable artifacts from the Actions tab |

---

## 📦 Artifacts in GitHub

After the workflow completes:

* Go to your **repository → Actions → MLOps Iris Classification → Artifacts**
* Download:

  * `iris-model` → contains the trained model file
  * `metrics` → contains evaluation metrics JSON

These artifacts are automatically uploaded by GitHub Actions.

---

## ✅ End-to-End Sequence

| Step | Action                                     | Where it Happens    |
| ---- | ------------------------------------------ | ------------------- |
| 1    | Clone repo & test scripts locally          | Local               |
| 2    | Commit changes to `main` branch            | Local               |
| 3    | GitHub Action auto-triggers on push        | GitHub Server       |
| 4    | Workflow installs dependencies & runs code | GitHub Cloud Runner |
| 5    | Model + metrics are uploaded as artifacts  | GitHub Cloud        |

---

## 🧠 Best Practices

* Test all scripts locally before committing.
* Keep workflows versioned under `.github/workflows/`.
* Use descriptive workflow names (`python-publish.yml`, `ml-ci.yml`, etc.).
* Store large models externally (e.g., DVC, S3) in production pipelines.
* Keep dependencies minimal for faster CI runs.

---

## 🧾 Summary

This repository demonstrates a **CI workflow** for a machine learning project using **GitHub Actions**.
On every push:

* The code installs dependencies
* Trains an Iris classification model
* Runs test validations
* Uploads model and metrics artifacts

This automates your ML lifecycle, making your project **reproducible, testable, and production-ready**.

---

```
```
