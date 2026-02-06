"""
PyRaksha Mobile App - Entry Point
Women Safety Platform
"""

import sys
import traceback

try:
    from src.app import PyRakshaApp

    def main() -> None:
        """Launch the PyRaksha mobile application."""
        try:
            print("Starting PyRaksha App...")
            app = PyRakshaApp()
            app.run()
        except Exception as e:
            print(f"CRITICAL ERROR in app.run(): {e}")
            traceback.print_exc()
            sys.exit(1)

    if __name__ == "__main__":
        main()

except Exception as e:
    print(f"CRITICAL ERROR during import: {e}")
    traceback.print_exc()
    sys.exit(1)
