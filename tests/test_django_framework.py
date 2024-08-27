from __future__ import annotations

from typing import TYPE_CHECKING

from django.urls import reverse
from rest_framework.test import APITestCase

from openapi_tester import SchemaTester
from tests.utils import TEST_ROOT

if TYPE_CHECKING:
    from rest_framework.response import Response

schema_tester = SchemaTester(
    schema_file_path=str(TEST_ROOT) + "/schemas/sample-schemas/content_types.yaml"
)


class BaseAPITestCase(APITestCase):
    """Base test class for api views including schema validation"""

    @staticmethod
    def assertResponse(response: Response, **kwargs) -> None:
        """helper to run validate_response and pass kwargs to it"""
        schema_tester.validate_response(response=response, **kwargs)


class PetsAPITests(BaseAPITestCase):
    def test_get_pet_by_id(self):
        response = self.client.get(
            reverse(
                "get-pet",
                kwargs={
                    "petId": 1,
                },
            ),
            content_type="application/vnd.api+json",
        )
        assert response.status_code == 200
        self.assertResponse(response)
