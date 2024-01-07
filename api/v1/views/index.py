from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def get_status():
    """ Returns a JSON response for the status """
    return jsonify({"status": "OK"})
