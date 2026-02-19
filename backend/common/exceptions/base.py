from rest_framework.exceptions import APIException


# -----------------------------------------------------------------------------------------------
# this is the contract exception class to be used in the project.
# -----------------------------------------------------------------------------------------------
class BaseAPIException(APIException):
    # inilizing the default message.
    status_code = 400
    default_code = "API_ERROR"
    default_message = "An unexpected error occurred"

    def __init__(self, *, message=None, code=None, status_code=None, details=None):
        if status_code is not None:
            self.status_code = status_code

        self.code = code or self.default_code
        self.message = message or self.default_message
        self.details = details or {}
        super().__init__(
            detail=self.message,
            code=self.code,
        )
