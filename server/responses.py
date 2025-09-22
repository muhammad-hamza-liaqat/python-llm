from rest_framework.response import Response


def success_response(data=None, message=None, status_code=200):
    return Response({
        "status": status_code,
        "message": message or "Successful",
        "data": data or {}
    }, status=status_code)


def error_response(message=None, data=None, status_code=400):
    return Response({
        "status": status_code,
        "message": message or "Request Failed",
        "data": data or {}
    }, status=status_code)
