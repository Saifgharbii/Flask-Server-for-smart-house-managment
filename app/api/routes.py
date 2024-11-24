from flask import jsonify, request
from app.api import bp
from app.controllers import DevicesController
from app.models import Light, Door, AC_Fan, FireDetector

@bp.route('/devices/<room_id>/lights', methods=['POST'])
def control_light(room_id):
    data = request.get_json()
    action = data.get('action')
    light = Light(room_id=room_id)
    
    if action == 'on':
        result = DevicesController.LampController.lamp_on(light)
    elif action == 'off':
        result = DevicesController.LampController.lamp_off(light)
    elif action == 'schedule':
        duration = data.get('duration')
        result = DevicesController.LampController.lamp_schedule(light, duration)
    else:
        return jsonify({'error': 'Invalid action'}), 400
        
    return jsonify(result)

@bp.route('/devices/<room_id>/doors', methods=['POST'])
def control_door(room_id):
    data = request.get_json()
    action = data.get('action')
    door = Door(room_id=room_id)
    
    if action == 'open':
        result = DevicesController.DoorController.open_door(door)
    elif action == 'close':
        result = DevicesController.DoorController.close_door(door)
    else:
        return jsonify({'error': 'Invalid action'}), 400
        
    return jsonify(result)

@bp.route('/devices/<room_id>/ac', methods=['POST'])
def control_ac(room_id):
    data = request.get_json()
    action = data.get('action')
    ac = AC_Fan(room_id=room_id)
    
    if action == 'activate':
        result = DevicesController.AC_Fan.activate_ac_fan(ac)
    elif action == 'deactivate':
        result = DevicesController.AC_Fan.desactivate_ac_fan(ac)
    else:
        return jsonify({'error': 'Invalid action'}), 400
        
    return jsonify(result)
