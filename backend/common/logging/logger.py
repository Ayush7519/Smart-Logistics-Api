# this is the format for the log data to be saved in the system.
import logging
import json
from django.utils import timezone


# -----------------------------------------------------------------------------------------------
# now we create the function to create the log data.
# -----------------------------------------------------------------------------------------------
class JsonFormatter(logging.Formatter):
    def format(self, record):
        # here we create the structure for the log data.
        log_record = {
            "level": record.levelname,
            "message": record.message,
            "timestamp": timezone.now().isoformat(),
        }

        # here we integrate the request id for the log data.
        if hasattr(record, "request_id"):
            log_record["request"] = record.request_id

        if hasattr(record, "extra"):
            log_record.update(record.extra)

        # now we change the record into the json format and return.
        return json.dumps(log_record)
