[app]

# App Information
title = PyRaksha
package.name = pyraksha
package.domain = org.pyraksha

# Source Configuration
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
source.include_patterns = assets/*,src/**/*

# Version
version = 1.0.1

# Requirements - Python packages needed
requirements = python3,kivy==2.3.0,kivymd==1.2.0,plyer==2.1.0,pyjnius==1.6.1,pillow==10.3.0,android

# Orientation
orientation = portrait
fullscreen = 0

# Icon and Splash Screen
icon.filename = %(source.dir)s/assets/icon.png
presplash.filename = %(source.dir)s/assets/splash.png

# Android Permissions
# INTERNET - API calls to backend
# ACCESS_FINE_LOCATION - GPS tracking for SOS
# ACCESS_COARSE_LOCATION - Approximate location
# ACCESS_NETWORK_STATE - Check network connectivity
# SEND_SMS - Future SMS alerts (not implemented yet)
# READ_PHONE_STATE - Required for some Android features
# VIBRATE - Vibration feedback for SOS trigger
# WAKE_LOCK - Keep screen awake during SOS
# FOREGROUND_SERVICE - Background SOS monitoring
# POST_NOTIFICATIONS - Show SOS notifications
# RECEIVE_BOOT_COMPLETED - Auto-start background service
android.permissions = INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,ACCESS_NETWORK_STATE,SEND_SMS,READ_PHONE_STATE,VIBRATE,WAKE_LOCK,FOREGROUND_SERVICE,POST_NOTIFICATIONS,RECEIVE_BOOT_COMPLETED

# Android API Levels
android.api = 31
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.arch = armeabi-v7a

# Background Service
# This enables the background SOS monitoring service
services = sos_background:service.py

# App metadata (optional)
# android.meta_data = com.google.android.geo.API_KEY=YOUR_API_KEY_HERE

[buildozer]

# Buildozer Configuration
log_level = 2
warn_on_root = 1