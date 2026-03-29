import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def run_example(path):
    return subprocess.run(
        [sys.executable, path],
        check=True,
        capture_output=True,
        cwd=REPO_ROOT,
        text=True,
    )


def test_basic_usage_example_runs():
    result = run_example("examples/basic_usage.py")

    assert "Quantum search probabilities" in result.stdout
    assert "Quantum walk mean distance" in result.stdout


def test_random_graph_workflow_example_runs():
    result = run_example("examples/random_graph_workflow.py")

    assert "Quantum search probabilities" in result.stdout
    assert "Quantum walk mean square distance" in result.stdout
