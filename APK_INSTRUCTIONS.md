# DriveBy Android APK

Yes! The DriveBy system can now be packaged as an Android APK for easy installation and use on mobile devices.

## Building the APK

### Quick Build (Recommended)

**Linux/macOS:**
```bash
./build_android_apk.sh
```

**Windows:**
```bash
build_android_apk.bat
```

### Manual Build

```bash
cd android_app
python build_apk.py
```

## Installation

1. **Build the APK** using one of the methods above
2. **Transfer APK** to your Android device (`DriveBy-debug.apk`)
3. **Enable Unknown Sources** in Android Settings → Security
4. **Install APK** by tapping on it
5. **Grant Permissions** when prompted (all permissions needed for full functionality)

## APK Features

### Complete DriveBy Functionality
- **Network Cluster Management** - Manage devices connecting to your hotspot
- **50+ Security Bypasses** - All Windows, macOS, Linux, Android bypasses included
- **Real-time Monitoring** - Live dashboard with device status
- **Auto-deployment** - Automatically deploy payloads to connecting devices
- **Privacy Protection** - Quantum-resistant encryption and advanced privacy
- **Background Service** - Runs continuously even when app is minimized

### Mobile-Optimized Interface
- **Material Design** - Modern Android UI with dark theme
- **Touch-friendly** - Optimized for mobile interaction
- **Real-time Updates** - Live status updates every 5 seconds
- **Status Cards** - Network, security, and device status at a glance
- **System Logs** - Real-time log output with timestamps

### Advanced Security Features
- **Windows Bypasses**: EDR unhooking, AMSI bypass, Windows Defender evasion
- 🤖 **Android Bypasses**: Root hiding, SafetyNet bypass, Play Protect evasion
- **macOS Bypasses**: Gatekeeper bypass, TCC bypass, XProtect evasion
- 🐧 **Linux Bypasses**: SELinux bypass, container escape, namespace evasion
- **Cross-platform**: VM detection evasion, AI/ML evasion, steganography

## Requirements

### Build Requirements
- Python 3.8+
- Java JDK 8+ (for release builds)
- 4GB+ RAM (for building)
- 10GB+ free disk space

### Runtime Requirements
- Android 5.0+ (API 21+)
- 2GB+ RAM
- 500MB+ storage space
- WiFi hotspot capability

## Usage

1. **Launch DriveBy** from your Android app drawer
2. **Start Service** by tapping "Start DriveBy"
3. **Enable Hotspot** on your Android device
4. **Connect Devices** to your hotspot
5. **Monitor Activity** through the real-time dashboard
6. **Run Security Bypasses** as needed

## Documentation

- **Complete Build Guide**: `android_app/README_APK.md`
- **Troubleshooting**: See build guide for common issues
- **Security Features**: `SECURITY_BYPASS.md`
- **Privacy Protection**: `PRIVACY_PROTECTION.md`

## Benefits of APK Version

### Convenience
- **One-tap Installation** - No complex setup required
- **Background Operation** - Runs continuously without user intervention
- **Boot Startup** - Automatically starts when device boots
- **Mobile Dashboard** - Full control from your phone

### Performance
- **Optimized for Mobile** - Efficient resource usage on Android
- **Native Integration** - Uses Android APIs for better performance
- **Battery Optimized** - Designed to minimize battery drain

### Security
- **Isolated Environment** - Runs in Android app sandbox
- **Permission Control** - Fine-grained permission management
- **Secure Storage** - Uses Android secure storage APIs

The DriveBy APK provides the complete home network cluster management experience in a convenient, mobile-optimized package!
