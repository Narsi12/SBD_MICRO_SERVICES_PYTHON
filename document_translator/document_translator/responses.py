import json
from datetime import date
from django.http import HttpResponse

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)

class SuccessResponse(Exception):
    def __init__(self, code, status, message, **extra_fields):
        self.code = code
        self.status = status
        self.message = message
        self.extra_fields = extra_fields

    def to_json_dict(self):
        result = {
                "code": self.code,
                "status": self.status,
                "message": self.message,
                }
        result.update(self.extra_fields)
        return result

    def to_json(self):
        return json.dumps(self.to_json_dict(),cls=CustomJSONEncoder)

    def http_response(self, status=None):
        response = HttpResponse(
            self.to_json(),
            status=status,
            content_type="application/json")
        return response