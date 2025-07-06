URL Categorizer
An extensible tool for real-time URL classification with hybrid detection methods.
🚀 Features

FastAPI REST API with interactive documentation
Live blacklists integration (Steven Black's hosts, URLHaus malware)
ML fallback using zero-shot transformer with customizable categories
Modern Tkinter GUI with live API logs and single-click launch
Easy local and batch processing capabilities

🔧 How it Works
Hybrid Classification System:

Combines blacklist lookups with ML content analysis
API-first design for web integration and automation
Modern GUI that shows API logs and auto-launches services
Live blacklist updates from trusted sources

📸 Screenshot
[Add screenshot here]
🚀 Quick Start
Prerequisites

Python 3.7+
pip package manager

Installation & Usage
1. Install Dependencies
bashpip install -r requirements.txt
2. Run the GUI (Recommended)
bashpython gui_app.py
What happens:

API automatically starts in the background
All FastAPI logs are visible in the GUI
"Categorize" button enables when API is ready
Enter any URL and click "Categorize" to see results

3. Manual API Usage (Optional)
For server/cloud deployments or API-only usage:
bashuvicorn main:app --reload
API Documentation: http://localhost:8000/docs
📡 API Endpoints
Categorize URL
httpPOST /categorize
Content-Type: application/json

{
  "url": "https://example.com"
}
Health Check
httpGET /health
