"""
PyRaksha Mobile App - Entry Point
Women Safety Platform
"""

from src.app import PyRakshaApp


def main() -> None:
    """Launch the PyRaksha mobile application."""
    app = PyRakshaApp()
    app.run()


if __name__ == "__main__":
    main()
