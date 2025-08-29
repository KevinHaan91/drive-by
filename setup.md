# DriveBy - Home Network Cluster Management System

## Overview

DriveBy is a home network cluster management system that automatically deploys input monitoring to devices connecting to your Android phone's hotspot. This system is designed for managing your own devices in a controlled home lab environment.

## Features

- **Automatic Device Detection**: Monitors devices connecting to your phone's hotspot
- **Cross-Platform Support**: Works with Windows, Linux, macOS, and Android devices
- **Web-Based Deployment**: Automatic script deployment via web interface
- **Real-Time Data Collection**: Collects and stores input data from cluster devices
- **Dashboard Interface**: Web dashboard for monitoring connected devices and data

## System Requirements

### Android Phone (Host)
- Android device with hotspot capability
- Termux app installed
- Python 3.7+ (via Termux)
- Network access for connected devices

### Target Devices
- **Windows**: PowerShell 5.0+, Administrator privileges recommended
- **Linux/macOS**: Python 3.6+, pip, terminal access
- **Android**: Termux app, Python environment

## Installation

### 1. Setup Android Host (Your Phone)

1. **Install Termux**:
 ```bash
 # Download Termux from F-Droid or Google Play Store
 # Open Termux and update packages
 pkg update && pkg upgrade
 ```

2. **Install Python and Dependencies**:
 ```bash
 pkg install python python-pip git
 pip install flask requests psutil netifaces python-nmap scapy watchdog cryptography colorama rich click
 ```

3. **Clone/Download DriveBy**:
 ```bash
 # If using git
 git clone <repository-url> DriveBy
 cd DriveBy

 # Or download and extract the files to ~/DriveBy/
 ```

4. **Install Python Requirements**:
 ```bash
 pip install -r requirements.txt
 ```

### 2. Configure the System

1. **Edit Configuration** (optional):
 ```bash
 nano config.json
 ```

 Key settings:
 - `server.port`: Web server port (default: 8080)
 - `server.data_port`: Data collection port (default: 8081)
 - `network.scan_interval`: Device scan frequency in seconds
 - `network.hotspot_range`: Your hotspot IP range

2. **Setup Storage Directory**:
 ```bash
 mkdir -p collected_data
 chmod 755 collected_data
 ```

### 3. Enable Hotspot on Your Phone

1. Go to Settings > Network & Internet > Hotspot & Tethering
2. Enable "Portable Wi-Fi hotspot"
3. Note the network name and password
4. Note the hotspot IP address (usually 192.168.43.1)

## Usage

### Starting the System

1. **Start the Main Host Service**:
 ```bash
 python phone_host.py
 ```

 This will:
 - Start monitoring for new device connections
 - Launch the web server for automatic deployment
 - Display the auto-installation URL

2. **Start the Data Collection Server** (in another terminal):
 ```bash
 python data_server.py
 ```

 This will:
 - Start the data collection endpoint
 - Launch the web dashboard
 - Store incoming keystroke data

### Connecting Devices to Your Cluster

1. **Connect Device to Hotspot**:
 - Connect your target device to your phone's hotspot
 - The device should automatically get an IP address

2. **Automatic Deployment**:
 - The device will be detected automatically
 - Open a web browser on the target device
 - Navigate to: `http://192.168.43.1:8080` (or your hotspot IP)
 - The auto-installation page will load and detect the device type

3. **Follow Installation Instructions**:
 - **Windows**: Download and run the PowerShell script as administrator
 - **Linux/Mac**: Download the Python script and run with appropriate permissions
 - **Android**: Install Termux and run the Android monitoring script

### Monitoring and Data Collection

1. **Web Dashboard**:
 - Access: `http://192.168.43.1:8081/dashboard`
 - View connected devices
 - Monitor data collection status
 - Browse collected keystroke data

2. **Status Endpoint**:
 - Host status: `http://192.168.43.1:8080/status`
 - Data server status: `http://192.168.43.1:8081/status`

3. **Data Storage**:
 - Data stored in: `collected_data/`
 - Organized by client IP address
 - JSON format with timestamps

## File Structure

```
DriveBy/
├── phone_host.py # Main Android host service
├── data_server.py # Data collection server
├── config.json # Configuration file
├── requirements.txt # Python dependencies
├── setup.md # This file
├── TODO.md # Implementation progress
├── payloads/ # Device-specific scripts
│ ├── windows_monitor.ps1
│ ├── linux_monitor.py
│ └── android_monitor.py
├── web/ # Web interface files
│ └── autorun.html
└── collected_data/ # Data storage directory
 ├── connections.log
 ├── daily_summary_*.log
 └── [client-ip]/
 └── keystrokes_*.json
```

## Security Considerations

**Important**: This system is designed for managing your own devices in a controlled home lab environment.

### Recommended Security Measures:

1. **Network Isolation**:
 - Use a dedicated hotspot for cluster devices
 - Isolate from your main home network
 - Consider using a separate phone/device for hosting

2. **Access Control**:
 - Enable authentication in config.json
 - Set strong API keys
 - Limit allowed device MAC addresses

3. **Data Protection**:
 - Encrypt stored data
 - Implement secure data transmission
 - Regular data cleanup/rotation

4. **Monitoring**:
 - Monitor system logs
 - Track device connections
 - Alert on suspicious activity

## Troubleshooting

### Common Issues:

1. **Devices Not Detected**:
 - Check hotspot is enabled and devices are connected
 - Verify IP range in config.json matches hotspot range
 - Check network interface name in configuration

2. **Web Interface Not Loading**:
 - Verify phone_host.py is running
 - Check firewall settings on Android
 - Ensure correct IP address and port

3. **Data Not Collecting**:
 - Verify data_server.py is running
 - Check client scripts have network access
 - Review client script logs for errors

4. **Permission Issues**:
 - Windows: Run PowerShell as administrator
 - Linux/Mac: May need sudo for input device access
 - Android: Grant Termux necessary permissions

### Debug Mode:

Enable debug logging by modifying the scripts:
```python
# Add to phone_host.py or data_server.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Log Files:

- Connection logs: `collected_data/connections.log`
- Daily summaries: `collected_data/daily_summary_*.log`
- Client data: `collected_data/[client-ip]/`

## Advanced Configuration

### Custom Payloads:

You can modify the payload scripts in the `payloads/` directory to customize behavior:

- `windows_monitor.ps1`: Windows PowerShell script
- `linux_monitor.py`: Linux/macOS Python script
- `android_monitor.py`: Android Termux script

### Network Configuration:

For different network setups, modify `config.json`:

```json
{
 "network": {
 "interface": "wlan0",
 "scan_interval": 5,
 "hotspot_range": "192.168.43.0/24"
 }
}
```

### Data Storage:

Customize data storage settings:

```json
{
 "data": {
 "storage_path": "collected_data",
 "log_format": "json",
 "max_file_size": "10MB"
 }
}
```

## Legal and Ethical Use

This system is intended for:
- Managing your own devices
- Home lab and educational purposes
- Authorized security testing
- Research in controlled environments

**Important**: Ensure you have proper authorization before deploying on any device. Unauthorized keystroke logging may violate privacy laws and regulations.

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review log files for error messages
3. Verify network connectivity and permissions
4. Test with a single device first before scaling

## License

This project is for educational and authorized use only. Users are responsible for compliance with applicable laws and regulations.
