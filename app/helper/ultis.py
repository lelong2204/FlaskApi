from flask import jsonify


def response(msg, status=True, code=200, data=None):
	return jsonify(msg=msg, status=status, code=code, data=data)
