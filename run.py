"""
Application Launcher.
Provides easy execution of the Streamlit application, experiments, and tests.
"""

import sys
import os
import subprocess

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


def run_app():
    """Launch the Streamlit web application."""
    main_py = os.path.join(PROJECT_ROOT, "app", "main.py")
    cmd = [sys.executable, "-m", "streamlit", "run", main_py]
    print(f"Launching Streamlit application from: {main_py}")
    subprocess.run(cmd)


def run_experiments():
    """Execute the full master experiment suite."""
    exp_py = os.path.join(PROJECT_ROOT, "experiments", "run_all_experiments.py")
    cmd = [sys.executable, exp_py]
    print(f"Running experiments from: {exp_py}")
    subprocess.run(cmd)


def run_tests():
    """Run pytest automated test suite."""
    test_py = os.path.join(PROJECT_ROOT, "tests", "test_full_suite.py")
    cmd = [sys.executable, "-m", "pytest", test_py, "-v"]
    print(f"Executing test suite: {test_py}")
    subprocess.run(cmd)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ["test", "tests"]:
            run_tests()
        elif arg in ["exp", "experiments", "benchmark"]:
            run_experiments()
        else:
            run_app()
    else:
        run_app()
