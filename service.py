"""
Background service for PyRaksha
SIMPLIFIED VERSION - No threading to avoid crashes
"""

import time


# Simple service that just logs
# Advanced features disabled until app is stable
def main():
    """
    Background service entry point
    This is called when the service starts
    """
    print("PyRaksha background service started")

    # Simple loop that does minimal work
    # This prevents crashes from complex threading
    while True:
        try:
            # Just sleep - don't do complex operations
            # Real SOS monitoring will be handled by the main app
            time.sleep(60)
            print("Background service tick")
        except Exception as e:
            print(f"Service error: {e}")
            time.sleep(60)


if __name__ == "__main__":
    main()
