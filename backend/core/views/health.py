from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.db import connection
from django.utils.timezone import now
from common.responses import api_response
from common.exceptions.base import BaseAPIException


# -----------------------------------------------------------------------------------------------
# this is the testing of the code.
# -----------------------------------------------------------------------------------------------
class HelathCheckApi(APIView):
    authentication_classes = []
    permission_classes = []

    # this is the function that check the connection witht the database.
    def get(self, request):
        health_status = {
            "status": "ok",
            "timestamp": now(),
            "service": {
                "database": "unknown",
            },
        }

        # database checking.
        try:
            connection.ensure_connection()
            health_status["service"]["database"] = "up"
        except Exception:
            health_status["services"]["database"] = "down"
            health_status["status"] = "degraded"

        http_status = (
            status.HTTP_200_OK
            if health_status["status"] == "ok"
            else status.HTTP_503_SERVICE_UNAVAILABLE
        )
        return api_response.success_response(
            data={
                "http_status": http_status,
                "status": "ok",
            }
        )


# -----------------------------------------------------------------------------------------------
# this is the basic view functions.
# -----------------------------------------------------------------------------------------------
class TestView(APIView):
    def get(self, request):
        return api_response.success_response(
            data={"message": "OK"},
            request=request,
        )
