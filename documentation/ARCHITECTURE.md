# System Architecture Documentation

## High-Level Overview
```mermaid
graph TD
    A[Web/Mobile Client] --> B[Flask API Server]
    B --> C{Controllers}
    C --> D[Firebase Firestore]
    C --> E[Arduino Hardware]
    C --> F[GHI AI Model]
    D --> G[(Real-time Database)]
    E --> H[Physical Devices]
    F --> I[Energy Management]
```

## 1. Component Architecture

### 1.1 Presentation Layer
```mermaid
flowchart LR
    Web[Web Client] --> API
    Mobile[Mobile App] --> API
    API[Flask API] -->|WebSocket| RealTime[Real-time Updates]
    style Web fill:#f9f,stroke:#333
    style Mobile fill:#9f9,stroke:#333
```

- **Web Client**: React-based dashboard
- **Mobile App**: Native iOS/Android applications
- **WebSocket**: Bi-directional communication channel

### 1.2 Application Layer
```mermaid
classDiagram
    class FlaskApp {
        +APIRoutes
        +WebSocketHandlers
        +Configuration
        +FirebaseAdapter
    }
    
    class Controllers {
        +DeviceController
        +EnergyController
        +ArduinoManager
        +AIModel
    }
    
    FlaskApp --> Controllers : Uses
```

### 1.3 Data Layer
```mermaid
erDiagram
    HOUSE ||--o{ ROOM : contains
    ROOM ||--o{ DEVICE : has
    USER ||--o{ HOUSE : owns
    ENERGY ||--o{ TRANSACTION : records
    
    HOUSE {
        string id PK
        string address
        float solar_capacity
    }
    
    DEVICE {
        string id PK
        string type
        string status
    }
```

## 2 Development Setup

```mermaid
graph LR
    DevClient --> Flask
    Flask --> FirebaseEmulator[(Firebase Emulator)]
    Flask --> Arduino[Local Arduino]
```

## 3. Core Flows

### 3.1 Device Control Flow
```mermaid
sequenceDiagram
    Client->>+API: POST /devices/{room}/lights
    API->>Controller: Validate request
    Controller->>Arduino: Send serial command
    Arduino->>Controller: Return ACK
    Controller->>Firebase: Update device status
    Firebase-->>Client: Real-time update
    API-->>Client: HTTP 200 response
```

### 3.2 Energy Management Flow
```mermaid
sequenceDiagram
    Arduino->>Server: Sensor data (every 5s)
    Server->>Firebase: Store raw data
    Firebase->>EnergyController: Trigger analysis
    EnergyController->>AIModel: Get forecast
    AIModel-->>EnergyController: 7-day prediction
    EnergyController->>Firebase: Update strategy
    EnergyController->>Arduino: Send adjustments
```

## 4. Key Architectural Decisions

1. **Real-time First Design**
   - WebSocket for instant updates
   - Firebase listener for DB changes
   - 5-second sensor polling cycle

2. **Modular Controller System**
   ```python
   class DeviceController(ABC):
       @abstractmethod
       def handle_command(self, command): pass
   
   class LightController(DeviceController):
       def handle_command(self, cmd):
           # Implementation specific to lights
   ```

3. **AI/ML Integration**
   - LSTM model for solar predictions
   - Separate model-serving thread
   - Daily retraining pipeline

4. **Security Layers**
   ```mermaid
   graph TD
       Request --> Auth[OAuth2 Authentication]
       Auth --> RateLimit[Rate Limiting]
       RateLimit --> Validation[Input Validation]
       Validation --> Controller
   ```

## 5. Scalability Considerations

| Component        | Scaling Strategy                | Tools/Techniques               |
|------------------|---------------------------------|--------------------------------|
| API Server       | Horizontal scaling              | Kubernetes, Gunicorn workers   |
| Database         | Sharding                        | Firebase regional deployments  |
| AI Model         | Batch processing                | TF Serving, GPU acceleration   |
| Arduino Network  | Edge computing                  | MQTT message broker            |

## 6. Technology Stack

| Layer            | Technologies                    |
|------------------|---------------------------------|
| Frontend         | React, Flutter, WebSocket       |
| Backend          | Flask, Firebase, Socket.IO      |
| Hardware         | Arduino UNO, ESP32 sensors      |
| AI/ML            | TensorFlow, Keras, Pandas       |
