from flask import jsonify
from . import api

@api.route('/status')
def status():
    return jsonify({'status': 'operational'}) 