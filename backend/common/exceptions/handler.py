import uuid
import logging
from rest_framework.views import exception_handler
from common.exceptions.base import BaseAPIException
from rest_framework.response import Response
from django.utils import timezone

logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------------------------------
# this is the custome exception handeler.
# -----------------------------------------------------------------------------------------------
def custom_exception_handler(exc, context):

    response = exception_handler(exc, context)
    request = context.get("request")
    request_id = getattr(request, "request_id", str(uuid.uuid4))

    # creating the base_meta data.
    base_meta = {
        "request_id": request_id,
        "timestamp": timezone.now().isoformat(),
    }

    if isinstance(exc, BaseAPIException):
        logger.warning(
            "Handled application exception",
            extra={
                "request_id": request_id,
                "extra": exc.detail,
            },
        )

        return Response(
            {
                "success": False,
                "data": None,
                "error": {
                    "message": exc.message,
                    "code": exc.code,
                    "details": exc.details,
                },
                "meta": base_meta,
            },
            status=exc.status_code,
        )

    # Handle DRF-known exceptions (ValidationError, NotAuthenticated, etc.)
    if response is not None:
        logger.warning(
            "DRF exception",
            extra={
                "request_id": request_id,
                "extra": response.data,
            },
        )
        return Response(
            {
                "success": "false",
                "data": None,
                "error": {
                    "message": "Request failed",
                    "code": "request_error",
                    "details": response.data,
                },
                "meta": base_meta,
            },
            status=response.status_code,
        )

    logger.exception(
        "Unhandled server error",
        extra={"request_id": request_id},
    )
    # Handle unhandled / server errors (500)
    return Response(
        {
            "success": False,
            "data": None,
            "error": {
                "message": "Internal server error",
                "code": "server_error",
                "details": None,
            },
            "meta": base_meta,
        },
        status=500,
    )
