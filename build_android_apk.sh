#!/bin/bash

# DriveBy Android APK Build Script
# Simple script to build the DriveBy Android APK

set -e

echo " DriveBy Android APK Builder"
echo "=============================="

# Check if we're in the right directory
if [ ! -f "phone_host.py" ]; then
 echo " Error: Please run this script from the DriveBy project root directory"
 exit 1
fi

# Check Python installation
if ! command -v python3 &> /dev/null; then
 echo " Error: Python 3 is required but not installed"
 exit 1
fi

echo " Python 3 found: $(python3 --version)"

# Check if android_app directory exists
if [ ! -d "android_app" ]; then
 echo " Error: android_app directory not found"
 exit 1
fi

echo " Android app directory found"

# Install required Python packages
echo " Installing required packages..."
pip3 install --user buildozer cython kivy kivymd plyer

# Navigate to android app directory
cd android_app

# Make build script executable
chmod +x build_apk.py

# Build the APK
echo " Building DriveBy APK..."
python3 build_apk.py

# Check if APK was created
if [ -f "../DriveBy-debug.apk" ]; then
 echo ""
 echo " SUCCESS! DriveBy APK has been built successfully!"
 echo " APK Location: DriveBy-debug.apk"
 echo ""
 echo " Installation Instructions:"
 echo "1. Transfer DriveBy-debug.apk to your Android device"
 echo "2. Enable 'Install from unknown sources' in Android settings"
 echo "3. Install the APK by tapping on it"
 echo "4. Grant all requested permissions for full functionality"
 echo ""
 echo " For detailed instructions, see android_app/README_APK.md"
else
 echo ""
 echo " Build failed - APK not found"
 echo " Check the build logs above for error details"
 echo " See android_app/README_APK.md for troubleshooting"
 exit 1
fi
