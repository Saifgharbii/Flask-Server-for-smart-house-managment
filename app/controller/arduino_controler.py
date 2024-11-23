from flask_socketio import SocketIO
import serial
import time

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