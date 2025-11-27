set -e
python3 -m venv .venv || true
source .venv/bin/activate
pip install -r requirements.txt
func start