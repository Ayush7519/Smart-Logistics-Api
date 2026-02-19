from django.utils import timezone
from rest_framework.response import Response


# -----------------------------------------------------------------------------------------------
# here we customize the response data so that its standard through whole project.
# -----------------------------------------------------------------------------------------------
def success_response(*, data=None, status_code=200, request=None, meta=None):
    base_meta = {
        "request_id": getattr(request, "request_id", None),
        "timestamp": timezone.now().isoformat(),
        **(meta or {}),
    }

    if meta:
        base_meta.update(meta)

    return Response(
        {
            "success": True,
            "data": data,
            "error": None,
            "meta": base_meta,
        },
        status=status_code,
    )
