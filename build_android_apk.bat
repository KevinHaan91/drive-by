@echo off
REM DriveBy Android APK Build Script for Windows
REM Simple script to build the DriveBy Android APK on Windows

echo DriveBy Android APK Builder
echo ==============================

REM Check if we're in the right directory
if not exist "phone_host.py" (
 echo Error: Please run this script from the DriveBy project root directory
 pause
 exit /b 1
)

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
 echo Error: Python is required but not installed
 echo Please install Python from https://python.org
 pause
 exit /b 1
)

echo Python found
python --version

REM Check if android_app directory exists
if not exist "android_app" (
 echo Error: android_app directory not found
 pause
 exit /b 1
)

echo Android app directory found

REM Install required Python packages
echo Installing required packages...
python -m pip install --user buildozer cython kivy kivymd plyer

REM Navigate to android app directory
cd android_app

REM Build the APK
echo Building DriveBy APK...
python build_apk.py

REM Check if APK was created
if exist "..\DriveBy-debug.apk" (
 echo.
 echo SUCCESS! DriveBy APK has been built successfully!
 echo APK Location: DriveBy-debug.apk
 echo.
 echo Installation Instructions:
 echo 1. Transfer DriveBy-debug.apk to your Android device
 echo 2. Enable 'Install from unknown sources' in Android settings
 echo 3. Install the APK by tapping on it
 echo 4. Grant all requested permissions for full functionality
 echo.
 echo For detailed instructions, see android_app\README_APK.md
) else (
 echo.
 echo Build failed - APK not found
 echo Check the build logs above for error details
 echo See android_app\README_APK.md for troubleshooting
)

echo.
echo Press any key to exit...
pause >nul
