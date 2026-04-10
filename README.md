# 🤖 JARVIS AI Assistant - Ultimate Version

**The most advanced AI assistant with face detection, smart automation, and intelligent web integration!**

## 🚀 Features

### 🎯 Core Features
- **AI Chat Assistant** powered by Google Gemini
- **Face Detection** with personalized greetings ("Hello Muhammad Hasnain!")
- **Smart Google Search** with auto-click functionality
- **Voice Commands** (when PyAudio is available)
- **Advanced GUI Interface** with modern design

### 🔍 Enhanced Search Capabilities
- **Auto-click TradingView**: `"search google for tradingview"` → Opens TradingView automatically
- **Smart Search**: Multiple command variations work
- **Application Search**: Find and open any installed software

### ⚡ Smart Automations
- **Trading Routine**: Opens all trading apps and websites
- **Morning Routine**: Start your day with essential apps
- **Work Setup**: Productivity workspace configuration
- **Entertainment Mode**: Setup for relaxation
- **System Cleanup**: Performance optimization

### 🖥️ Application Control
- **50+ Applications**: Chrome, Firefox, VS Code, TradingView, Spotify, etc.
- **System Control**: Volume, desktop, lock PC, settings
- **Web Integration**: Direct access to websites and services

## 🛠️ Installation

1. **Clone/Download** the project
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment**:
   - Edit `.env` file with your Google AI API key
   - Ensure camera is available for face detection

## 🚀 Quick Start

### Method 1: Ultimate Launcher (Recommended)
```bash
python jarvis_launcher.py
```
This starts ALL components:
- Django Server
- Face Detection
- GUI Interface

### Method 2: Individual Components

**Django Server:**
```bash
python manage.py runserver
```

**Face Detection & Voice Listener:**
```bash
python simple_listener.py
```

**GUI Interface:**
```bash
python gui/jarvis_gui.py
```

## 📖 Commands Guide

### 🔍 Search Commands
- `"search google for tradingview"` → Searches and auto-clicks TradingView
- `"open google"` → Opens Google homepage
- `"search for python tutorial on google"` → Natural language search

### ⚡ Automation Commands
- `"list automations"` → Shows all available automations
- `"quick trading"` → Starts trading routine
- `"morning routine"` → Starts morning setup
- `"work mode"` → Configures workspace
- `"entertainment mode"` → Setup for relaxation

### 🖥️ Application Commands
- `"open tradingview"` → Opens TradingView (local app or web)
- `"open chrome"` → Opens Chrome browser
- `"open vs code"` → Opens Visual Studio Code
- `"open spotify"` → Opens Spotify
- `"open notepad"` → Opens Notepad

### 🎛️ System Commands
- `"volume up"` / `"volume down"` → Control volume
- `"mute"` → Mute audio
- `"show desktop"` → Minimize all windows
- `"lock pc"` → Lock computer
- `"open settings"` → Open system settings

## 🌐 Access Points

1. **Web Interface**: http://127.0.0.1:8000
2. **GUI Application**: Modern desktop interface
3. **Voice Commands**: "Hey Jarvis..." (when enabled)
4. **Face Detection**: Automatic greeting system

## 🎨 GUI Features

The modern GUI interface includes:
- **Real-time Chat** with Jarvis AI
- **Quick Command Buttons** for common tasks
- **Status Monitoring** of all components
- **Face Detection Toggle**
- **Voice Control** (coming soon)
- **Settings Panel** (coming soon)

## 🧠 Smart Features

### Auto-Click Technology
When you search for TradingView or other specific apps, Jarvis automatically:
1. Opens Google search
2. Waits for results to load
3. Clicks the first relevant result
4. Opens the application/website

### Face Detection
- **Personal Greeting**: "Hello Muhammad Hasnain!"
- **Smart Cooldown**: Won't spam greetings
- **Background Operation**: Runs continuously
- **Visual Feedback**: Shows detected faces

### AI-Powered Automation
- **Multi-step Sequences**: Complex task automation
- **Error Handling**: Graceful fallbacks
- **Scheduled Tasks**: Time-based automation
- **Custom Commands**: Create your own automations

## 📱 Supported Applications

### 📊 Trading & Finance
- TradingView, MetaTrader (MT4/MT5)

### 🌐 Web Browsers
- Chrome, Firefox, Edge, Brave, Opera

### 💬 Communication
- Discord, Slack, Teams, Zoom, Skype, Telegram

### 💻 Development
- VS Code, Sublime Text, Notepad++, PyCharm

### 🎵 Media & Entertainment
- Spotify, VLC, YouTube, Netflix

### 📄 Productivity
- Word, Excel, PowerPoint, Outlook

### 🎨 Graphics
- Photoshop, Illustrator, Paint

### 🎮 Gaming
- Steam, Epic Games Launcher

## 🔧 Configuration

### Environment Variables (.env)
```
AI_API_KEY=your_google_gemini_api_key
DJANGO_SECRET_KEY=your_django_secret_key
DEBUG=True
```

### Customization
- Add new applications in `api/utils.py`
- Create custom automations in `automation/smart_automation.py`
- Modify face detection settings in `face_detection.py`

## 🚨 Troubleshooting

### Common Issues

1. **PyAudio Installation Failed**
   - Use `simple_listener.py` instead of `listener.py`
   - Or install PyAudio manually: `pip install pyaudio`

2. **Camera Not Working**
   - Check camera permissions
   - Ensure no other app is using the camera

3. **Django Server Won't Start**
   - Check if port 8000 is available
   - Run `python manage.py migrate` first

4. **Auto-Click Not Working**
   - Ensure browser is in focus
   - Check screen resolution compatibility

## 🎯 Tips & Tricks

1. **Voice Commands**: Start commands with "Hey Jarvis" or "Jarvis"
2. **Quick Access**: Use the GUI for frequently used commands
3. **Batch Operations**: Use automations for multi-step tasks
4. **Keyboard Shortcuts**: GUI supports Enter to send commands
5. **Face Detection**: Works best in good lighting conditions

## 🌟 Advanced Features

### Coming Soon
- 🎤 Full voice control with PyAudio
- 🌍 Multi-language support
- 📊 System monitoring dashboard
- 🔧 Custom automation builder
- ☁️ Cloud sync for settings
- 📱 Mobile app companion

### Experimental Features
- 🧠 AI-powered command prediction
- 🤖 Smart context awareness
- 📈 Performance analytics
- 🔌 Plugin system

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section
2. Ensure all dependencies are installed
3. Verify camera and microphone permissions
4. Check the logs in `listener.log` and `face_detection.log`

## 🎉 Enjoy Your Jarvis Assistant!

You now have the most advanced AI assistant with:
- 🤖 Intelligent conversation
- 👤 Personal face recognition
- 🔍 Smart web automation
- ⚡ Powerful automations
- 🖥️ Beautiful interface
- 🎵 Voice interaction
- 📊 Trading integration

**Jarvis is ready to serve you, Muhammad Hasnain!** 🚀
