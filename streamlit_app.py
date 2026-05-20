"""Entrypoint do dashboard para Streamlit Community Cloud.

Adiciona src/ ao sys.path e executa o dashboard. Mantém o código real
em src/imobia/viz/dashboard.py para preservar o src-layout do projeto.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

# Executa o dashboard real
exec(compile((ROOT / "src/imobia/viz/dashboard.py").read_text(), "dashboard.py", "exec"))
