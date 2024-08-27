"""Exceptions Module"""


class DocumentationError(AssertionError):
    """Custom exception raised when package tests fail."""


class CaseError(DocumentationError):
    """Custom exception raised when items are not cased correctly."""

    def __init__(self, key: str, case: str, expected: str) -> None:
        super().__init__(
            f"The response key `{key}` is not properly {case}. Expected value: {expected}"
        )


class MissingKeyError(DocumentationError):
    """Custom exception raised when properties are missing from response."""

    def __init__(self, missing_key: str, reference: str = "init"):
        self.key = missing_key
        super().__init__(
            f'The following property is missing in the response data: "{self.key}"\n\n'
            f"Reference: {reference}.object:key:{self.key}\n\n"
            f"Hint: Remove the key from your OpenAPI docs, or include it in your API response"
        )


class OpenAPISchemaError(Exception):
    """Custom exception raised for invalid schema specifications."""


class UndocumentedSchemaSectionError(OpenAPISchemaError):
    """Subset of OpenAPISchemaError, raised when we cannot find a single schema section."""
