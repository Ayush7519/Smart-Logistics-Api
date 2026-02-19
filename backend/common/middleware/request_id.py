import logging
import uuid

# -----------------------------------------------------------------------------------------------
# integrating the log data here.
# -----------------------------------------------------------------------------------------------
logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------------------------------
# here we create the custome request ids.
# -----------------------------------------------------------------------------------------------
class RequestIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.request_id = str(uuid.uuid4())
        response = self.get_response(request)
        response["X-Request-ID"] = request.request_id

        # here we send the data in the log.
        logging.info(
            "Request Completed",
            extra={
                "request_id": request.request_id,
                "extra": {
                    "methos": request.method,
                    "path": request.path,
                },
            },
        )

        return response
