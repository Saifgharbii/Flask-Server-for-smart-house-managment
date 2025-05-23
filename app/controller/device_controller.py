
from typing import Dict, Any
from ..models import device, FirebaseManager , Light, Window, Door, CleaningRobot, Battery, FireDetector,AC_Fan
from .arduino_controler import ArduinoController

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
 
    # class FireDetectorController :
    #     @staticmethod
    #     def launch_alarm(fire_detector :FireDetector) :
    #         if fire_detector.status :
    #             #launch alarm
    #             """
    #             open a door of a specific room.
    #             """
    #             message = f"launch_alarm_{fire_detector.room_name}"
    #             ArduinoController.send_to_arduino(message)
    #             return {"status": "success", "message": f"there is a fire in room {fire_detector.room_name} ."}