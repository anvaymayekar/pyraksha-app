[app]

# App Information
title = PyRaksha
package.name = pyraksha
package.domain = org.pyraksha

# Source Configuration
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,json
source.include_patterns = assets/*,src/**/*.py

# Version
version = 1.0.1

# Requirements - Python packages needed
# CRITICAL FIX: Removed python-dotenv (not needed and causes issues)
# CRITICAL FIX: Added proper android dependencies
requirements = python3,kivy==2.3.0,kivymd==1.2.0,plyer==2.1.0,pyjnius,pillow,android

# Orientation
orientation = portrait
fullscreen = 0

# Icon and Splash Screen (optional - comment out if files don't exist)
# icon.filename = %(source.dir)s/assets/icon.png
# presplash.filename = %(source.dir)s/assets/splash.png

# Android Permissions
android.permissions = INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,ACCESS_NETWORK_STATE,VIBRATE,WAKE_LOCK,FOREGROUND_SERVICE,POST_NOTIFICATIONS

# Android API Levels
# CRITICAL FIX: Use compatible API levels
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.arch = arm64-v8a

# CRITICAL FIX: Disable background service for now (causing crashes)
# services = sos_background:service.py

# Add these for better stability
android.gradle_dependencies = 
android.add_src = 
android.add_jars = 
android.add_libs_armeabi = 
android.add_libs_armeabi_v7a = 
android.add_libs_arm64_v8a = 
android.add_libs_x86 = 
android.add_libs_mips = 

# Blacklist and whitelist configuration
android.whitelist = lib-dynload/termios.so

# Copy library instead of using linking
android.copy_libs = 1

[buildozer]

# Buildozer Configuration
log_level = 2
warn_on_root = 1