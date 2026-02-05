"""
Background service for PyRaksha
Handles SOS triggers when app is in background
"""

from jnius import autoclass
from time import sleep

PythonService = autoclass("org.kivy.android.PythonService")
PythonService.mService.setAutoRestartService(True)

print("PyRaksha background service started")

# Keep service alive
while True:
    sleep(60)  # Sleep for 60 seconds
    # Service stays alive to handle widget clicks
