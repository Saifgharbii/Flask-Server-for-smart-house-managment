
# Smart Home Energy Management System

[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![Firebase](https://img.shields.io/badge/Firebase-FFCA28?logo=firebase&logoColor=white)](https://firebase.google.com)
[![Flask](https://img.shields.io/badge/Flask-2.0%2B-lightgrey?logo=flask)](https://flask.palletsprojects.com/)

A comprehensive IoT solution for smart home energy management featuring real-time device control, energy optimization, and solar forecasting using LSTM AI models.

## Key Features

- 🏠 **Real-time Device Control**  
  Manage lights, doors, and AC units through REST API and WebSocket interfaces
- 🔋 **Smart Energy Distribution**  
  Priority-based energy allocation between solar, batteries, and grid
- ☀️ **Solar Radiation Forecasting**  
  LSTM neural network for 7-day GHI predictions
- 🔥 **Firebase Integration**  
  Real-time data synchronization and storage
- 📶 **Arduino Communication**  
  Bi-directional serial communication with IoT devices
- 📊 **Energy Analytics**  
  Historical consumption/production tracking and insights

## Project Structure

```
smart-home-energy-system/
├── app/                   # Core application module
│   ├── api/               # REST API endpoints
│   ├── controller/        # Business logic controllers
│   ├── models/            # Data models and DB integration
│   ├── __init__.py        # App factory and configuration
│   └── db_init.py         # Firebase initialization
├── run.py                 # Application entry point
├── requirements.txt       # Python dependencies
├── arduino_data_example.json  # Sample sensor data format
└── credentials/           # Security files (gitignored)
    └── firebase-creds.json
````

## Installation

### Prerequisites
- Python 3.9+
- Firebase project credentials
- Arduino connected on COM5 (Windows) or /dev/ttyACM0 (Linux)

### Setup Steps

1. Clone repository:
   ```bash
   git clone https://github.com/Saifgharbii/Flask-Server-for-smart-house-managment.git
   cd Flask-Server-for-smart-house-managment
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/MacOS
   venv\Scripts\activate     # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure Firebase:
   - Place credentials in `credentials/firebase-creds.json`
   - Initialize database:
     ```python
     from app.db_init import init_firebase
     init_firebase(app)
     ```

5. Start the server:
   ```bash
   python run.py
   ```

## Usage

### API Examples

**Turn On Living Room Lights:**
```bash
curl -X POST http://localhost:5000/api/v1/devices/living_room/lights \
     -H "Content-Type: application/json" \
     -d '{"action": "on"}'
```

**Close Garage Door:**
```bash
curl -X POST http://localhost:5000/api/v1/devices/garage/doors \
     -H "Content-Type: application/json" \
     -d '{"action": "close"}'
```

**Get Solar Forecast:**
```bash
curl -X GET http://localhost:5000/api/v1/forecast
```

### WebSocket Interface
Connect to `ws://localhost:5000` for real-time updates:
```javascript
const socket = io('http://localhost:5000');

// Send command
socket.emit('command', 'make_light_on_kitchen');

// Receive sensor data
socket.on('arduino_data', (data) => {
    console.log('Sensor Update:', data);
});
```

## Documentation

- [API Reference](./documentation/API.md)
- [System Architecture](./documentation/ARCHITECTURE.md)
- [Data Models](./documentation/DATA_MODELS.md)

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/improvement`)
5. Open Pull Request

