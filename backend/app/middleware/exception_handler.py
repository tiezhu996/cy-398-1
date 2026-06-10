from rest_framework.views import exception_handler
from app.constants.errors import ERRORS

def standard_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return response
    response.data = {
        "success": False,
        "code": getattr(exc, "default_code", "VALIDATION_FAILED"),
        "message": response.data if isinstance(response.data, str) else ERRORS.get("VALIDATION_FAILED"),
        "detail": response.data,
    }
    return response
