#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export HOME="$DIR"
export STREAMLIT_GATHER_USAGE_STATS=false
export STREAMLIT_SERVER_HEADLESS=true

echo "=========================================================="
echo "🏢 Starting OfficeMate 2.0 – Streamlit Virtual Workplace"
echo "   URL: http://localhost:8501"
echo "=========================================================="
"$DIR/.venv/bin/streamlit" run "$DIR/app.py" --server.port 8501 --server.headless true
