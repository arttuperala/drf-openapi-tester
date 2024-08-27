from __future__ import annotations

from contextlib import suppress
from copy import deepcopy
from pathlib import Path
from typing import TYPE_CHECKING

from rest_framework.response import Response

from tests.schema_converter import SchemaToPythonConverter

if TYPE_CHECKING:
    from typing import Any, Callable, Generator

TEST_ROOT = Path(__file__).resolve(strict=True).parent


def response_factory(
    schema: dict | None, url_fragment: str, method: str, status_code: int | str = 200
) -> Response:
    converted_schema = None
    if schema:
        converted_schema = SchemaToPythonConverter(deepcopy(schema)).result
    response = Response(status=int(status_code), data=converted_schema)
    response.request = {"REQUEST_METHOD": method, "PATH_INFO": url_fragment}  # type: ignore
    if schema:
        response.json = lambda: converted_schema  # type: ignore
    return response


def iterate_schema(schema: dict) -> Generator[tuple[dict | None, Response | None, str], None, None]:
    for url_fragment, path_object in schema["paths"].items():
        for method, method_object in path_object.items():
            if method.lower() != "parameters":
                for status_code, responses_object in method_object["responses"].items():
                    if status_code == "default":
                        continue
                    schema_section = None
                    response = None
                    with suppress(KeyError):
                        if "content" in responses_object:
                            schema_section = responses_object["content"]["application/json"][
                                "schema"
                            ]
                        elif "schema" in responses_object:  # noqa: SIM908
                            schema_section = responses_object["schema"]
                    if schema_section:
                        response = response_factory(
                            schema=schema_section,
                            url_fragment=url_fragment,
                            method=method,
                            status_code=status_code,
                        )
                    yield schema_section, response, url_fragment


def mock_schema(schema) -> Callable:
    def _mocked():
        return schema

    return _mocked


def sort_object(data_object: Any) -> Any:
    """helper function to sort objects"""
    if isinstance(data_object, dict):
        for key, value in data_object.items():
            if isinstance(value, (dict, list)):
                data_object[key] = sort_object(value)
        return dict(sorted(data_object.items()))
    if isinstance(data_object, list) and data_object:
        if not all(isinstance(entry, type(data_object[0])) for entry in data_object):
            return data_object
        if isinstance(data_object[0], (dict, list)):  # pragma: no cover
            return [sort_object(entry) for entry in data_object]
        return sorted(data_object)
    return data_object


def get_schema_content(schema: Path) -> bytes:
    with open(schema, "rb") as schema_file:
        return schema_file.read()
