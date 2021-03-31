from flask import jsonify


def custom_response(msg, status=True, code=200, data=None):
	return jsonify(msg=msg, status=status, code=code, data=data)
