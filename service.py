"""
Background service for PyRaksha (Briefcase-compatible)
Handles SOS triggers while the app is running
"""

import threading
import time
from src.services.sos_service import SOSService


def sos_background_loop():
    """
    Runs continuously in the background to check for SOS triggers.
    This only works while the app is open.
    """
    sos_service = SOSService.get_instance()
    while True:
        try:
            # Check for any active SOS events
            active_sos = sos_service.get_active_sos()
            if active_sos:
                # You can trigger notifications or UI updates here
                print("Active SOS detected!")
        except Exception as e:
            print(f"Background SOS error: {e}")
        time.sleep(60)  # Run every 60 seconds


# Start the background thread as daemon
threading.Thread(target=sos_background_loop, daemon=True).start()
print("PyRaksha background thread started")
