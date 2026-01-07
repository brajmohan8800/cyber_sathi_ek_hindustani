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

## 🚀 cyber_sathi_ek_hindustani

A Python-based educational security testing tool.  
⚠️ Use only on systems you own or have explicit permission to test.

> IMPORTANT  
> Ngrok use karte waqt **Mobile Hotspot / Wi‑Fi ON hona zaroori hai**.  
> Sirf mobile data par ngrok aksar connect nahi hota.

---

### 📦 Requirements

- Android phone
- Termux (F‑Droid version recommended)
- Python 3.x
- Active Internet (Wi‑Fi / Hotspot)

---

### 📥 Step 1: Install Required Packages (One Time)

```bash
apt update && apt upgrade -y
apt install git wget python -y
```
---
### 📂 Step 2: Clone This Repository

```bash

git clone https://github.com/brajmohan8800/cyber_sathi_ek_hindustani.git

```
### 🌐 Step 3: Install Ngrok on Termux
Download the Ngrok binary for ARM64 devices:

```bash
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-arm64.tgz
```
### Extract the archive:

```bash
tar -xvzf ngrok-v3-stable-linux-arm64.tgz
```

### Make Ngrok executable:

```bash
chmod +x ngrok
```

### Move Ngrok to Termux system path:

```bash
mv ngrok $PREFIX/bin/
```

### Verify installation:

```bash
ngrok version
```

### 🔑 Step 4: Add Your Ngrok Auth Token
Open a browser and visit:
https://dashboard.ngrok.com/signup
Login or create a free account.
Copy your Authtoken from the dashboard.
Add it in Termux:

```bash
ngrok config add-authtoken YOUR_NGROK_AUTH_TOKEN
```

Now go to your directory cyber_sathi_........

🛠 Step 6: Install Project Dependencies

```bash
pip install -r requirements.txt
```

▶️ Step 7: Run the Tool

```bash
python main.py
```

⚠️ Notes
Always keep Hotspot/Wi-Fi ON while using the tool.

🛑 Disclaimer
This project is strictly for educational purposes only.
The developer is not responsible for misuse.

