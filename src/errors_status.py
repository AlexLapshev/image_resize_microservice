from aiohttp.web_response import json_response


class BaseError:
    def __init__(self, error_msg: str, status: int):
        self.error_msg = error_msg
        self.status = status


class PostError(BaseError):
    def __init__(self, error_field: str, error_msg: str, status: int):
        super().__init__(error_msg, status)
        self.error_field = error_field

    def create_response_error(self) -> json_response():
        return json_response({"error_field": self.error_field, "error_msg": self.error_msg}, status=self.status)


class GetError(BaseError):
    def __init__(self, error_msg: str, status: int, error_image_id: str = 'no id') -> json_response:
        super().__init__(error_msg, status)
        self.error_image_id = error_image_id

    def create_response_error(self) -> json_response():
        return json_response({"error_msg": self.error_msg, "error_image_id": self.error_image_id},
                             status=self.status)

