from flask import jsonify


def ok(data=None, http_status=200):
    return jsonify({
        'success': True,
        'data': data
    }), http_status


def fail(error: str, http_status: int):
    return jsonify({
        'success': False,
        'error': error
    }), http_status
