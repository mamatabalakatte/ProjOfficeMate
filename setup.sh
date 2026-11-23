#!/bin/bash
set -e

echo "=========================================================="
echo "🏢 OfficeMate 2.0 – Setup & Initialization Script"
echo "=========================================================="

# 1. Create Python 3.12 Virtual Environment if needed
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment in .venv..."
    python3.12 -m venv .venv || python3 -m venv .venv
fi

# 2. Upgrade pip and install requirements
echo "Installing dependencies from requirements.txt..."
./.venv/bin/pip install --upgrade pip
./.venv/bin/pip install -r requirements.txt

# 3. Initialize & Seed Database
echo "Initializing SQLite database with WAL mode and seed data..."
./.venv/bin/python -m db.seed_data

# 4. Train NLP Baseline & Deep Learning Bi-LSTM Models
echo "Training TF-IDF Baseline & Bidirectional LSTM models..."
./.venv/bin/python -m nlp.train_models || (./.venv/bin/python -m nlp.tfidf_baseline && ./.venv/bin/python -m nlp.bilstm_model)

# 5. Evaluate models and generate real test metrics
echo "Evaluating models on held-out test partitions..."
./.venv/bin/python -m nlp.evaluator

echo "=========================================================="
echo "✅ Setup Complete! OfficeMate 2.0 is ready to run."
echo "   Run frontend: ./run_frontend.sh"
echo "   Run backend:  ./run_backend.sh"
echo "   Run tests:    ./.venv/bin/pytest tests/ -v"
echo "=========================================================="
