from rest_framework.response import Response


def success_response(data=None, message="Success", status_code=200):
    return Response(
        {
            "status": status_code,
            "message": message,
            "data": data,
        },
        status=status_code,
    )


def error_response(message="Error", details=None, status_code=400):
    flat_details = flatten_errors(details) if details else None
    return Response(
        {
            "status": status_code,
            "message": message,
            "details": flat_details,
        },
        status=status_code,
    )


def flatten_errors(errors):
    if isinstance(errors, dict):
        messages = []
        for field, msgs in errors.items():
            if isinstance(msgs, list):
                for msg in msgs:
                    if msg == "This field is required.":
                        messages.append(f"{field} field is required")
                    else:
                        messages.append(f"{field}: {msg}")
            else:
                messages.append(f"{field}: {msgs}")
        return "; ".join(messages)

    elif isinstance(errors, list):
        return "; ".join(str(msg) for msg in errors)

    return str(errors)
