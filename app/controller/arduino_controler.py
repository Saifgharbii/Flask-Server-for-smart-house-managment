from flask_socketio import SocketIO
import serial
import time
from contextlib import contextmanager
# Initialize serial connection to Arduino

arduino = serial.Serial(
            port="COM5",
            baudrate=9600,
            timeout=0.05,
            write_timeout=1
        )

print(arduino.is_open)

time.sleep(2)  # Wait for the connection to stabilize




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
                    #print(f"Data received from Arduino: {data}")
                    # Emit the data to connected clients via Socket.IO
                    #socketio.emit('arduino_data', {'data': data})
                    return data
            except Exception as e:
                print(f"Error reading from Arduino: {e}")  
                return {}