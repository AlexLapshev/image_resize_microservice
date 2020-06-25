from aiohttp.web_response import json_response


class Errors:

    error_status = {
        400: 'incorrect field name',
        404: 'image_id not found'
    }

    @classmethod
    def web_response(cls, error: int) -> json_response():
        return json_response({"error": Errors.error_status[error]}, status=error)