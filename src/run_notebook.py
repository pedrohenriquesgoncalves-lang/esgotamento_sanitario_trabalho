"""Executa o notebook de EDA sem abrir o Jupyter: python -m src.run_notebook"""
from pathlib import Path

import nbformat
from nbclient import NotebookClient

NB = Path(__file__).resolve().parents[1] / "notebooks" / "analise_exploratoria.ipynb"

if __name__ == "__main__":
    nb = nbformat.read(NB, as_version=4)
    NotebookClient(nb, timeout=600, kernel_name="python3", resources={"metadata": {"path": str(NB.parent)}}).execute()
    nbformat.write(nb, NB)
    print("notebook executado:", NB)
