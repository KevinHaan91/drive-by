#!/usr/bin/env python3
"""
DriveBy Android App
Main application entry point for mobile dashboard
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.logger import Logger
import requests
import json
import threading
import time

class DriveByApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.server_url = ""
        self.connected = False
        self.monitoring = False
        
    def build(self):
        """Build the main app interface"""
        self.title = "DriveBy Mobile Dashboard"
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        title = Label(
            text='DriveBy Mobile Dashboard',
            size_hint_y=None,
            height=60,
            font_size=24,
            bold=True
        )
        main_layout.add_widget(title)
        
        # Status display
        self.status_label = Label(
            text='Status: Ready',
            size_hint_y=None,
            height=40,
            font_size=16
        )
        main_layout.add_widget(self.status_label)
        
        # Server configuration section
        server_section = BoxLayout(orientation='vertical', size_hint_y=None, height=120, spacing=5)
        
        server_section.add_widget(Label(text='Server Configuration:', size_hint_y=None, height=30, font_size=18))
        
        server_input_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        server_input_layout.add_widget(Label(text='Server:', size_hint_x=None, width=80))
        self.server_input = TextInput(
            text='192.168.1.100:8080',
            multiline=False,
            size_hint_y=None,
            height=40
        )
        server_input_layout.add_widget(self.server_input)
        server_section.add_widget(server_input_layout)
        
        # API Key input
        api_input_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        api_input_layout.add_widget(Label(text='API Key:', size_hint_x=None, width=80))
        self.api_input = TextInput(
            text='driveby-default-key',
            multiline=False,
            password=True,
            size_hint_y=None,
            height=40
        )
        api_input_layout.add_widget(self.api_input)
        server_section.add_widget(api_input_layout)
        
        main_layout.add_widget(server_section)
        
        # Control buttons section
        button_section = BoxLayout(orientation='vertical', size_hint_y=None, height=200, spacing=10)
        
        # Connect button
        self.connect_btn = Button(
            text='Connect to Server',
            size_hint_y=None,
            height=50,
            font_size=16
        )
        self.connect_btn.bind(on_press=self.toggle_connection)
        button_section.add_widget(self.connect_btn)
        
        # Start monitoring button
        self.monitor_btn = Button(
            text='Start Monitoring',
            size_hint_y=None,
            height=50,
            font_size=16,
            disabled=True
        )
        self.monitor_btn.bind(on_press=self.toggle_monitoring)
        button_section.add_widget(self.monitor_btn)
        
        # Test connection button
        test_btn = Button(
            text='Test Connection',
            size_hint_y=None,
            height=50,
            font_size=16
        )
        test_btn.bind(on_press=self.test_connection)
        button_section.add_widget(test_btn)
        
        # View logs button
        logs_btn = Button(
            text='View Logs',
            size_hint_y=None,
            height=50,
            font_size=16
        )
        logs_btn.bind(on_press=self.view_logs)
        button_section.add_widget(logs_btn)
        
        main_layout.add_widget(button_section)
        
        # Log display area
        log_section = BoxLayout(orientation='vertical', spacing=5)
        log_section.add_widget(Label(text='Activity Log:', size_hint_y=None, height=30, font_size=18))
        
        # Scrollable log area
        scroll = ScrollView()
        self.log_label = Label(
            text='DriveBy Mobile Dashboard initialized.\nReady to connect to server.',
            text_size=(None, None),
            halign='left',
            valign='top',
            font_size=12
        )
        scroll.add_widget(self.log_label)
        log_section.add_widget(scroll)
        
        main_layout.add_widget(log_section)
        
        # Start status update timer
        Clock.schedule_interval(self.update_status, 1.0)
        
        return main_layout
    
    def log_message(self, message):
        """Add a message to the log display"""
        timestamp = time.strftime("%H:%M:%S")
        new_log = f"[{timestamp}] {message}"
        current_text = self.log_label.text
        self.log_label.text = f"{current_text}\n{new_log}"
        Logger.info(f"DriveBy: {message}")
    
    def toggle_connection(self, instance):
        """Toggle connection to server"""
        if not self.connected:
            self.connect_to_server()
        else:
            self.disconnect_from_server()
    
    def connect_to_server(self):
        """Connect to the DriveBy server"""
        server = self.server_input.text.strip()
        if not server:
            self.log_message("Error: Please enter a server address")
            return
        
        self.server_url = f"http://{server}"
        self.log_message(f"Connecting to {self.server_url}...")
        self.status_label.text = f'Connecting to {server}...'
        
        # Test connection in background thread
        threading.Thread(target=self._test_connection_thread, daemon=True).start()
    
    def _test_connection_thread(self):
        """Test connection in background thread"""
        try:
            response = requests.get(f"{self.server_url}/status", timeout=5)
            if response.status_code == 200:
                Clock.schedule_once(lambda dt: self._connection_success(), 0)
            else:
                Clock.schedule_once(lambda dt: self._connection_failed(f"Server returned status {response.status_code}"), 0)
        except requests.exceptions.RequestException as e:
            Clock.schedule_once(lambda dt: self._connection_failed(str(e)), 0)
    
    def _connection_success(self):
        """Handle successful connection"""
        self.connected = True
        self.status_label.text = 'Connected to server'
        self.connect_btn.text = 'Disconnect'
        self.monitor_btn.disabled = False
        self.log_message("Successfully connected to server")
    
    def _connection_failed(self, error):
        """Handle connection failure"""
        self.connected = False
        self.status_label.text = 'Connection failed'
        self.connect_btn.text = 'Connect to Server'
        self.monitor_btn.disabled = True
        self.log_message(f"Connection failed: {error}")
    
    def disconnect_from_server(self):
        """Disconnect from server"""
        self.connected = False
        self.monitoring = False
        self.status_label.text = 'Disconnected'
        self.connect_btn.text = 'Connect to Server'
        self.monitor_btn.text = 'Start Monitoring'
        self.monitor_btn.disabled = True
        self.log_message("Disconnected from server")
    
    def toggle_monitoring(self, instance):
        """Toggle monitoring state"""
        if not self.monitoring:
            self.start_monitoring()
        else:
            self.stop_monitoring()
    
    def start_monitoring(self):
        """Start monitoring"""
        if not self.connected:
            self.log_message("Error: Not connected to server")
            return
        
        self.monitoring = True
        self.status_label.text = 'Monitoring active'
        self.monitor_btn.text = 'Stop Monitoring'
        self.log_message("Monitoring started")
        
        # Start monitoring thread
        threading.Thread(target=self._monitoring_thread, daemon=True).start()
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.monitoring = False
        self.status_label.text = 'Connected (monitoring stopped)'
        self.monitor_btn.text = 'Start Monitoring'
        self.log_message("Monitoring stopped")
    
    def _monitoring_thread(self):
        """Background monitoring thread"""
        while self.monitoring and self.connected:
            try:
                # Send heartbeat to server
                data = {
                    'device_id': 'android_mobile',
                    'timestamp': time.time(),
                    'status': 'active'
                }
                
                response = requests.post(
                    f"{self.server_url}/heartbeat",
                    json=data,
                    timeout=5
                )
                
                if response.status_code == 200:
                    Clock.schedule_once(lambda dt: self.log_message("Heartbeat sent successfully"), 0)
                else:
                    Clock.schedule_once(lambda dt: self.log_message(f"Heartbeat failed: {response.status_code}"), 0)
                    
            except Exception as e:
                Clock.schedule_once(lambda dt: self.log_message(f"Monitoring error: {str(e)}"), 0)
            
            time.sleep(30)  # Send heartbeat every 30 seconds
    
    def test_connection(self, instance):
        """Test connection to server"""
        server = self.server_input.text.strip()
        if not server:
            self.log_message("Error: Please enter a server address")
            return
        
        self.log_message(f"Testing connection to {server}...")
        threading.Thread(target=self._test_connection_only, args=(server,), daemon=True).start()
    
    def _test_connection_only(self, server):
        """Test connection without connecting"""
        try:
            url = f"http://{server}/status"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                Clock.schedule_once(lambda dt: self.log_message(f"✓ Connection test successful to {server}"), 0)
            else:
                Clock.schedule_once(lambda dt: self.log_message(f"✗ Connection test failed: HTTP {response.status_code}"), 0)
        except Exception as e:
            Clock.schedule_once(lambda dt: self.log_message(f"✗ Connection test failed: {str(e)}"), 0)
    
    def view_logs(self, instance):
        """View detailed logs"""
        self.log_message("Viewing logs... (Feature coming soon)")
    
    def update_status(self, dt):
        """Update status periodically"""
        if self.connected and self.monitoring:
            # Update status with current time
            current_time = time.strftime("%H:%M:%S")
            self.status_label.text = f'Monitoring active - {current_time}'

if __name__ == '__main__':
    DriveByApp().run()

