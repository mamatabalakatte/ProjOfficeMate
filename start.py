"""
OfficeMate 2.0 Unified Process Launcher
Launches Flask REST API (Port 5000) and Streamlit Frontend (Port 8501) concurrently.
"""

import subprocess
import sys
import time
import os
import signal

def main():
    venv_python = os.path.join(os.path.dirname(__file__), ".venv", "bin", "python")
    venv_streamlit = os.path.join(os.path.dirname(__file__), ".venv", "bin", "streamlit")

    if not os.path.exists(venv_python):
        venv_python = sys.executable
        venv_streamlit = "streamlit"

    print("=" * 60)
    print("🏢 Starting OfficeMate 2.0 – The Intelligent Virtual Workplace")
    print("=" * 60)

    # 1. Start Flask API in background
    print("\n[1/2] Launching Flask REST API on http://127.0.0.1:5000 ...")
    api_proc = subprocess.Popen(
        [venv_python, "-m", "api.app"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    time.sleep(2)

    # 2. Start Streamlit Frontend
    print("[2/2] Launching Streamlit Virtual Workplace on http://127.0.0.1:8501 ...")
    try:
        streamlit_proc = subprocess.Popen(
            [venv_streamlit, "run", "app.py", "--server.port", "8501"],
            stdout=sys.stdout,
            stderr=sys.stderr
        )
        streamlit_proc.wait()
    except KeyboardInterrupt:
        print("\nStopping OfficeMate 2.0 services...")
    finally:
        api_proc.terminate()
        try:
            streamlit_proc.terminate()
        except Exception:
            pass
        print("All processes stopped cleanly.")

if __name__ == "__main__":
    main()
