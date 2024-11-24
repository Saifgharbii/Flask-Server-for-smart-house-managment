from flask import jsonify, request
from ..controller import device_controller,arduino_controler
from ..models import Light, Door, AC_Fan, FireDetector
from flask import Blueprint

bp = Blueprint('api', __name__)
@bp.route('/devices/<room_id>/lights', methods=['POST'])
def control_light(room_id):
    data = request.get_json()
    action = data.get('action')
    light = Light(room_id=room_id)
    
    if action == 'on':
        result = device_controller.LampController.lamp_on(light)
    elif action == 'off':
        result = device_controller.LampController.lamp_off(light)
    elif action == 'schedule':
        duration = data.get('duration')
        result = device_controller.LampController.lamp_schedule(light, duration)
    else:
        return jsonify({'error': 'Invalid action'}), 400
        
    return jsonify(result)

@bp.route('/devices/<room_id>/doors', methods=['POST'])
def control_door(room_id):
    data = request.get_json()
    action = data.get('action')
    door = Door(room_id=room_id)
    
    if action == 'open':
        result = device_controller.DoorController.open_door(door)
    elif action == 'close':
        result = device_controller.DoorController.close_door(door)
    else:
        return jsonify({'error': 'Invalid action'}), 400
        
    return jsonify(result)

@bp.route('/devices/<room_id>/ac', methods=['POST'])
def control_ac(room_id):
    data = request.get_json()
    action = data.get('action')
    ac = AC_Fan(room_id=room_id)
    
    if action == 'activate':
        result = device_controller.AC_Fan.activate_ac_fan(ac)
    elif action == 'deactivate':
        result = device_controller.AC_Fan.desactivate_ac_fan(ac)
    else:
        return jsonify({'error': 'Invalid action'}), 400
        
    return jsonify(result)
