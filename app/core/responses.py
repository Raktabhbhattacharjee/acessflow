def success_response(data: dict):
    return {
        "status": "success",
        "data": data,
        "error": None
    }


def error_response(message: str):
    return {
        "status": "error",
        "data": None,
        "error": message
    }