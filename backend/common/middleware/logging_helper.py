import logging
from core.models.base import AuditLog

# -----------------------------------------------------------------------------------------------
# connecting the logs.
# -----------------------------------------------------------------------------------------------
logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------------------------------
# this is the log manager for the log save in the database.
# -----------------------------------------------------------------------------------------------
def _create_audit_log(request, action, message, level, user=None, extra_data=None):
    AuditLog.objects.create(
        user=user,
        action=action,
        message=message,
        level=level,
        ip_address=request.META.get("REMOTE_ADDR"),
        metadata=extra_data or {},
    )


# # -----------------------------------------------------------------------------------------------
# # this is the log manager for the success log.
# # -----------------------------------------------------------------------------------------------
# def log_sucess(request, action, message, user=None, extra_data=None):
#     play_load = {
#         "action": action,
#         "ip_address": request.META.get("REMOTE_ADDR"),
#     }
#     if user:
#         play_load.update(
#             {
#                 "user_id": user.id,
#                 "email": user.email,
#             },
#         )

#     if extra_data:
#         play_load.update(extra_data)

#     logger.info(message, extra=play_load)
#     _create_audit_log(
#         request,
#         action,
#         message,
#         "INFO",
#         user,
#         extra_data,
#     )


# # # -----------------------------------------------------------------------------------------------
# # # this is the manager for the log warning.
# # # -----------------------------------------------------------------------------------------------
# # def log_warning(request, action, message, user=None, extra_data=None):
# #     play_load = {
# #         "action": action,
# #         "ip_address": request.Meta.get("REMOTE_ADDR"),
# #     }
# #     if user:
# #         play_load.update(
# #             {
# #                 "user_id": user.id,
# #                 "email": user.email,
# #             },
# #         )
# #     if extra_data:
# #         play_load.update(extra_data)

# #     logger.warning(
# #         message,
# #         extra=play_load,
# #     )
# #     _create_audit_log(
# #         request,
# #         action,
# #         message,
# #         "WARNING",
# #         user,
# #         extra_data,
# #     )


# # # -----------------------------------------------------------------------------------------------
# # # this is the manager for the error logs.
# # # -----------------------------------------------------------------------------------------------
# # def log_error(request, action, message, error=None, user=None, extra_data=None):
# #     payload = {
# #         "action": action,
# #         "ip_address": request.META.get("REMOTE_ADDR"),
# #     }

# #     if user:
# #         payload.update(
# #             {
# #                 "user_id": user.id,
# #                 "email": user.email,
# #             }
# #         )

# #     if error:
# #         payload["error"] = str(error)

# #     if extra_data:
# #         payload.update(extra_data)

# #     logger.error(
# #         message,
# #         extra=payload,
# #     )

# #     _create_audit_log(
# #         request,
# #         action,
# #         message,
# #         "ERROR",
# #         user,
# #         extra_data,
# #     )
