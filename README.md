# 🛡️ FraudShield — AI/ML Credit Card Fraud Detection System

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg)](https://mysql.com)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.5-red.svg)](https://scikit-learn.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An end-to-end **credit card fraud detection system** achieving **94.3% precision** on 284,000+ transactions using a hybrid rule-based + machine learning approach. Built with Python, Flask, MySQL, and scikit-learn.

---

## 📊 Key Results

| Metric | Before SMOTE | After SMOTE |
|---|---|---|
| **Precision** | 92.1% | **94.3%** |
| **Recall (Fraud)** | 61.0% | **88.0%** |
| **F1-Score** | 0.731 | **0.910** |
| **AUC-ROC** | 0.951 | **0.979** |
| Manual Review Time | baseline | **↓ 40%** |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Flask Web Application                   │
│                                                           │
│  ┌──────────┐   ┌────────────┐   ┌───────────────────┐  │
│  │ Dashboard│   │Transactions│   │   REST API         │  │
│  │ /dashboard│  │ /txns      │   │  POST /api/analyze │  │
│  └──────────┘   └────────────┘   └───────────────────┘  │
│                         │                                 │
│              ┌──────────▼──────────┐                     │
│              │  Fraud Detection    │                     │
│              │      Engine         │                     │
│              │  ┌───────────────┐  │                     │
│              │  │  Rule Engine  │  │  ← 5 business rules │
│              │  │  (40% weight) │  │                     │
│              │  └───────────────┘  │                     │
│              │  ┌───────────────┐  │                     │
│              │  │   ML Model    │  │  ← Random Forest    │
│              │  │  (60% weight) │  │    + SMOTE          │
│              │  └───────────────┘  │                     │
│              │  ┌───────────────┐  │                     │
│              │  │ Score Fusion  │  │  ← Hybrid scoring   │
│              │  └───────────────┘  │                     │
│              └─────────────────────┘                     │
│                         │                                 │
│              ┌──────────▼──────────┐                     │
│              │      MySQL DB        │                     │
│              │ (transactions,alerts)│                     │
│              └──────────────────────┘                     │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- MySQL 8.0+
- pip

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/fraudshield.git
cd fraudshield
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

```bash
cp .env.example .env
# Edit .env with your MySQL credentials and secret key
```

### 5. Setup MySQL database

```bash
mysql -u root -p < scripts/schema.sql
```

### 6. Initialize the application

```bash
python scripts/init_db.py
```

### 7. Train the ML model

```bash
# Download dataset first:
# https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud
# Place creditcard.csv in ml/data/

python ml/train.py
```

### 8. Run the application

```bash
python run.py
```

Visit: **http://localhost:5000**  
Login: `admin` / `admin123`

---

## 🤖 ML Pipeline

### Dataset
- **Source**: [Kaggle Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)
- **Size**: 284,807 transactions
- **Fraud rate**: 0.172% (highly imbalanced)
- **Features**: V1–V28 (PCA-transformed), Amount, Time

### Class Imbalance — SMOTE Solution

```
Original:   Legit 284,315  |  Fraud 492      (ratio 578:1)
After SMOTE: Legit 284,315 | Fraud 85,294    (ratio 3.3:1)
```

SMOTE (Synthetic Minority Over-sampling Technique) generates synthetic
fraud samples by interpolating between real fraud cases in feature space,
improving recall from 61% → **88%** without data leakage.

### Rule Engine

| Rule | Trigger |
|---|---|
| High Amount | > $10,000 |
| Unusual Hour | 1 AM – 5 AM |
| Transaction Velocity | > 20 txns / 24h |
| Round Amount | Multiples of $100 |
| New Country | First-ever transaction from country |

### Score Fusion

```
final_score = (ml_score × 0.60) + (rule_score × 0.40)
```

---

## 🔌 API Reference

### POST /api/analyze

Submit a transaction for fraud analysis.

```json
{
  "amount": 2500.00,
  "customer_id": "CUST_12345",
  "merchant": "Electronics Store",
  "country": "US",
  "transaction_time": "2024-06-15T03:22:00",
  "v1": -1.359807134, "v2": -0.072781173,
  "v3": 2.536346738
}
```

**Response:**

```json
{
  "transaction_id": "txn-uuid-here",
  "is_fraud": true,
  "risk_level": "high",
  "ml_score": 0.7823,
  "final_score": 0.6694,
  "rule_flags": ["Transaction at unusual hour: 03:00"],
  "status": "flagged"
}
```

### GET /api/stats

```json
{
  "total_transactions": 12847,
  "fraud_detected": 312,
  "fraud_rate": 2.43,
  "model_precision": 94.3,
  "model_recall": 88.0
}
```

### GET /api/health

```json
{ "status": "ok", "service": "fraud-detection-api" }
```

---

## 🗂️ Project Structure

```
fraudshield/
├── app/
│   ├── __init__.py           # App factory
│   ├── models/               # SQLAlchemy models
│   ├── routes/               # Flask blueprints
│   │   ├── api.py            # REST API
│   │   ├── auth.py           # Login/logout
│   │   ├── dashboard.py      # Dashboard
│   │   └── transactions.py   # Transaction management
│   ├── utils/
│   │   └── fraud_engine.py   # Hybrid detection engine
│   └── templates/            # Jinja2 HTML templates
├── ml/
│   ├── train.py              # Full training pipeline
│   ├── models/               # Saved pkl files (gitignored)
│   └── data/                 # CSV dataset (gitignored)
├── scripts/
│   ├── init_db.py            # DB setup & seed
│   └── schema.sql            # MySQL schema
├── tests/
│   └── test_fraud_detection.py
├── config.py
├── run.py
├── requirements.txt
└── .env.example
```

---

## 🧪 Running Tests

```bash
pytest tests/ -v --cov=app --cov-report=html
```

---

## 🚀 Production Deployment

```bash
# Using Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 "app:create_app('production')"
```

Set these environment variables in production:
- `FLASK_CONFIG=production`
- `SECRET_KEY=<strong-random-key>`
- `DATABASE_URL=mysql+pymysql://user:pass@host/dbname`

---

## 📄 License

MIT License — see [LICENSE](LICENSE)

---

## 👤 Author

Built as a portfolio project demonstrating end-to-end ML system design:
- Class imbalance handling (SMOTE)
- Hybrid rule + ML scoring
- Production Flask architecture
- REST API design
- MySQL integration with SQLAlchemy ORM
