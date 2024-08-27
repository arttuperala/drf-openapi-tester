from __future__ import annotations

from typing import TYPE_CHECKING

from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from test_project.api.swagger.auto_schemas import get_snake_cased_response

if TYPE_CHECKING:
    from rest_framework.request import Request


class SnakeCasedResponse(APIView):
    renderer_classes = [JSONRenderer]

    @extend_schema(
        responses={
            200: inline_serializer(
                name="SnakeCaseSerializer",
                many=True,
                fields={"this_is_snake_case": serializers.CharField()},
            )
        }
    )
    @get_snake_cased_response()
    def get(self, request: Request, version: int, **kwargs) -> Response:
        return Response({"this_is_snake_case": "test"}, 200)
