from flask import Blueprint, jsonify, request
from datetime import datetime ,time
from typing import Dict, Any
from ..models import device, FirebaseManager , Light, Window, Door, CleaningRobot, Battery
from arduino_controler import ArduinoController

firebase_manager = FirebaseManager()

class DevicesController :
    @staticmethod
    def lamp_shudle(lamp ,Duration) :
        message = f"estana duration {Duration} for room {lamp.room_id}"
        ArduinoController.send_to_arduino(message)
    @staticmethod 
    def lamp_on(lamp) :
        message = f"make_light_on_{lamp.room_id}"
        ArduinoController.send_to_arduino(message)
    @staticmethod
    def lamp_on(lamp) :
        message = f"make_light_off_{lamp.room_id}"
        ArduinoController.send_to_arduino(message)
    @staticmethod
    def lamp_on(lamp) :
        message = f"make_light_off_{lamp.room_id}"
        ArduinoController.send_to_arduino(message)