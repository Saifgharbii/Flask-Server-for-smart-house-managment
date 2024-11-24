#arduino_controller.py
from flask_socketio import SocketIO
import serial
import time
import threading

# Initialize serial connection to Arduino
arduino = serial.Serial('/dev/ttyUSB0', 9600)  # Update with your Arduino port
time.sleep(2)  # Wait for the connection to stabilize

# Socket.IO instance (shared with Flask app)
socketio = SocketIO()

class ArduinoController:
    @staticmethod
    def send_to_arduino(message):
        """
        Send a string message to the Arduino via serial communication.
        """
        try:
            # Send the string to the Arduino
            arduino.write(message.encode('utf-8'))
            print(f"Message sent to Arduino: {message}")
            return {"status": "success", "message": "Message sent to Arduino."}
        except Exception as e:
            print(f"Error: {e}")
            return {"status": "error", "message": str(e)}

    @staticmethod
    def handle_socket_event(data):
        """
        Handle incoming Socket.IO event to send a message to the Arduino.
        """
        message = data.get('message', '')
        if not message:
            return {"status": "error", "message": "No message provided."}
        
        # Call the send_to_arduino method to send the message
        return ArduinoController.send_to_arduino(message)
    
    @staticmethod
    def read_from_arduino():
        """
        Background thread to read data from Arduino and send it to connected clients.
        """
        while True:
            try:
                # Read data from the Arduino
                data = arduino.readline().decode('utf-8').strip()
                if data:  # If valid data is received
                    print(f"Data received from Arduino: {data}")
                    # Emit the data to connected clients via Socket.IO
                    socketio.emit('arduino_data', {'data': data})
                    return data
            except Exception as e:
                print(f"Error reading from Arduino: {e}")  
                return {}

#device_controller.py
from typing import Dict, Any
from ..models import device, FirebaseManager , Light, Window, Door, CleaningRobot, Battery, FireDetector,AC_Fan
from arduino_controler import ArduinoController

firebase_manager = FirebaseManager()

class DevicesController :
    
    class LampController :
        @staticmethod
        def lamp_schedule(lamp : Light, duration: int):
            """
            Schedule the lamp to turn on/off after a specific duration.
            """
            message = f"schedule_duration_{duration}_for_room_{lamp.room_name}"
            ArduinoController.send_to_arduino(message)
            return {"status": "success", "message": "Lamp scheduled successfully."}

        @staticmethod
        def lamp_on(lamp : Light):
            """
            Turn on the lamp in a specific room.
            """
            message = f"make_light_on_{lamp.room_name}"
            ArduinoController.send_to_arduino(message)
            return {"status": "success", "message": f"Lamp in room {lamp.room_name} turned on."}

        @staticmethod
        def lamp_off(lamp : Light):
            """
            Turn off the lamp in a specific room.
            """
            message = f"make_light_off_{lamp.room_name}"
            ArduinoController.send_to_arduino(message)
            return {"status": "success", "message": f"Lamp in room {lamp.room_name} turned off."}
    class DoorController :
        @staticmethod
        def open_door(door : Door) :
            """
            open a door of a specific room.
            """
            message = f"open_door_{door.room_name}"
            ArduinoController.send_to_arduino(message)
            return {"status": "success", "message": f"door in room {door.room_name} is opend."}
        @staticmethod
        def close_door(door: Door):
            """
            Close a door of a specific room.
            """
            message = f"close_door_{door.room_name}"
            ArduinoController.send_to_arduino(message)
            return {"status": "success", "message": f"Door in room {door.room_name} is closed."}
    class AC_Fan :
        @staticmethod
        def activate_ac_fan(ac : AC_Fan) :
            """
            Activate an AC fan of a room
            """
            message = f"activate_AC_{ac.room_name}"
            ArduinoController.send_to_arduino(message)
            return {"status": "success", "message": f"AC in room {ac.room_name} is activated."}
        @staticmethod
        def desactivate_ac_fan(ac : AC_Fan) :
            """
            Disactivate an AC fan of a room
            """
            message = f"disactivate_AC_{ac.room_name}"
            ArduinoController.send_to_arduino(message)
            return {"status": "success", "message": f"AC in room {ac.room_name} is disactivated."}
 
