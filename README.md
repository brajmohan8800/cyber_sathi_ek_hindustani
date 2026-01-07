# Cyber Sathi Help 🇮🇳

## Ethical Hacking Learning Platform for Educational Purpose

### Features:
- 📚 Learning Modules (6 comprehensive modules)
- 🔧 Educational Tools (8 practical tools)
- 🎯 Practice Challenges (Beginner to Advanced)
- 📖 Tutorials & Guides
- 👨‍🏫 Live Safe Demos
- 📊 Progress Tracker

- ### templetes
- facebook
- instagram
- github
- googel
- also you can add and modify the templete 

### Installation:

# 🚀 cyber_sathi_ek_hindustani

A Python-based educational security testing tool.  
**Use only on systems you own or have explicit permission to test.**

> ⚠️ **Important:**  
> Always turn **Mobile Hotspot / Wi-Fi ON** before running Ngrok.  
> Ngrok often fails on mobile data due to ISP restrictions.

---

### 📦 Requirements

- Android Device  
- Termux (F-Droid recommended)  
- Python 3.x  
- Active Internet connection (Wi-Fi / Hotspot)

---

### 🔧 Ngrok Installation on Termux

Follow these steps carefully. Copy each block and run in Termux.

```bash
# 1. Update Termux & install wget
apt update && apt upgrade -y
apt install wget -y

# 2. Download Ngrok (ARM64)
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-arm64.tgz

# 3. Extract Ngrok
tar -xvzf ngrok-v3-stable-linux-arm64.tgz

# 4. Make Ngrok executable
chmod +x ngrok

# 5. Move Ngrok to system PATH
mv ngrok $PREFIX/bin/

# 6. Verify Ngrok installation
ngrok version

# 7. Add your Ngrok auth token (replace YOUR_NGROK_AUTH_TOKEN)
ngrok config add-authtoken YOUR_NGROK_AUTH_TOKEN

# 8. Test Ngrok
ngrok http 80


---

### install project

```bash
# Install Python 3.x first
# Then install dependencies:
pip install -r requirements.txt

# Run the tool:

python main.py


