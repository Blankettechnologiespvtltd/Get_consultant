def success_response(data=None, message="Success"):
    return {
        "status": True,
        "message": message,
        "data": data
    }


def error_response(message="Error", errors=None):
    return {
        "status": False,
        "message": message,
        "errors": errors
    }