import traceback
from django.utils.deprecation import MiddlewareMixin
from common.middleware.logging_helper import _create_audit_log


# -----------------------------------------------------------------------------------------------
# this is the middleware for the global logging.
# -----------------------------------------------------------------------------------------------
class AuditLogMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        # here we create the logs after the execution of the views.
        status_code = response.status_code

        # here we skip if the request is done by the admin or database health checkup.
        if request.path.startswith("/admin/"):
            return response

        # taking out the user.
        user = getattr(request, "user", None)

        # this is for the 4XX error (client )
        if 400 <= status_code < 500:
            _create_audit_log(
                level="WARNING",
                action="HTTP_CLIENT_ERROR",
                message=f"{request.method} {request.path} returned {status_code}",
                request=request,
                user=user,
                extra_data={"status_code": status_code},
            )

        elif status_code >= 500:
            _create_audit_log(
                level="WARNING",
                action="HTTP_CLIENT_ERROR",
                message=f"{request.method} {request.path} returned {status_code}",
                request=request,
                user=user,
                extra_data={"status_code": status_code},
            )

        return response

    def process_exception(self, request, exception):
        user = getattr(request, "user", None)

        _create_audit_log(
            level="ERROR",
            action="UNHANDLED_EXCEPTION",
            message=str(exception),
            request=request,
            user=user,
            extra_data={
                "traceback": traceback.format_exc(),
                "path": request.path,
                "method": request.method,
            },
        )

        return None
