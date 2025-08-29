# DriveBy - Mobile Cluster Management System

[![Build Android APK](https://github.com/YOUR_USERNAME/driveby/actions/workflows/build-android.yml/badge.svg)](https://github.com/YOUR_USERNAME/driveby/actions/workflows/build-android.yml)

DriveBy is a comprehensive mobile cluster management system designed for network monitoring and device coordination. This project includes both server-side Python components and a mobile Android application.

## 🚀 Features

- **Mobile Dashboard**: Android app for remote monitoring and control
- **Server Management**: Python-based server for handling multiple device connections
- **Network Analysis**: Advanced network scanning and monitoring capabilities
- **Privacy Protection**: Built-in privacy and security features
- **Cross-Platform**: Works on Android, Linux, Windows, and macOS

## 📱 Android APK

The Android APK is automatically built using GitHub Actions whenever code is pushed to the main branch.

### Download APK
- **Latest Release**: Check the [Releases](https://github.com/YOUR_USERNAME/driveby/releases) page for the latest APK
- **Development Build**: Download from [GitHub Actions](https://github.com/YOUR_USERNAME/driveby/actions) artifacts

### Manual Build
If you want to build the APK manually:

```bash
cd android_app
pip install buildozer cython kivy
buildozer android debug
```

## 🛠️ Installation

### Server Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/driveby.git
   cd driveby
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements_2024b.txt
   ```

3. **Run the server**:
   ```bash
   python3 start.py
   ```

### Android App Installation

1. **Download the APK** from the releases page
2. **Enable "Install from unknown sources"** in Android settings
3. **Install the APK** by tapping on it
4. **Grant permissions** when prompted

## 📋 Requirements

### Server Requirements
- Python 3.8+
- Linux/Windows/macOS
- Network connectivity

### Android Requirements
- Android 5.0+ (API level 21)
- Internet permission
- Storage permissions (for logging)

## 🔧 Configuration

### Server Configuration
Edit `config.json` to configure server settings:

```json
{
  "server": {
    "host": "0.0.0.0",
    "port": 8080,
    "data_port": 8081
  },
  "security": {
    "api_key": "your-secure-api-key",
    "encryption": true
  }
}
```

### Android App Configuration
1. Open the DriveBy app
2. Enter your server IP and port (e.g., `192.168.1.100:8080`)
3. Enter your API key
4. Tap "Connect to Server"

## 🏗️ Project Structure

```
driveby/
├── android_app/           # Android application source
│   ├── main.py           # Main Android app
│   ├── buildozer.spec    # Build configuration
│   └── ...
├── .github/workflows/    # GitHub Actions
│   └── build-android.yml # APK build workflow
├── server/               # Server components
│   ├── data_server.py    # Data collection server
│   ├── phone_host.py     # Mobile device handler
│   └── ...
├── security/             # Security modules
├── docs/                 # Documentation
└── requirements_2024b.txt # Python dependencies
```

## 🔒 Security Features

- **Encrypted Communication**: All data transmission is encrypted
- **API Key Authentication**: Secure API key-based authentication
- **Privacy Protection**: Built-in privacy protection mechanisms
- **Network Security**: Advanced network security bypass capabilities

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This software is for educational and authorized testing purposes only. Users are responsible for complying with all applicable laws and regulations.

## 🐛 Issues

If you encounter any issues:

1. Check the [Issues](https://github.com/YOUR_USERNAME/driveby/issues) page
2. Create a new issue with detailed information
3. Include logs and system information

## 📞 Support

- **Documentation**: Check the `docs/` folder
- **Issues**: GitHub Issues page
- **Discussions**: GitHub Discussions

## 🔄 Automatic Builds

This repository uses GitHub Actions to automatically:
- Build Android APKs on every push
- Run tests and code quality checks
- Create releases with downloadable APKs

The APK build process includes:
- Setting up the build environment
- Installing dependencies
- Building the APK with Buildozer
- Uploading artifacts
- Creating releases

---

**Note**: Replace `YOUR_USERNAME` with your actual GitHub username in all URLs and badges.

