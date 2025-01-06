from typing import Any, Dict, List

class BaseValidator:
    """
    Base Validator class for set up the environment for Validation
    """

    def validate(self, data):
        raise NotImplementedError("This method should be implemented by subclasses")

class JSONValidator(BaseValidator):
    """
    JSONValidator is responsible for validating JSON data to ensure that no fields have null values.

    Attributes:
        optional_fields (List[str]): A list of field paths where null checks are optional.
    """

    def __init__(self, optional_fields=None):
        """
        Initialize the JSONValidator with optional fields if required.

        :param optional_fields: A list of field paths to exclude from null validation.
        If None, all fields are validated.
        """
        self.optional_fields = optional_fields or []

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate the JSON for null values.

        This method checks for null values in the provided JSON data. If any fields
        contain null values and are not in the optional fields list, their paths
        are recorded as invalid fields.

        :param data: The input JSON data as a dictionary.
        :return: A dictionary containing the validation status and details. If invalid
        fields are found, the "status" is "error" and the "invalid_fields" list contains
        their paths. Otherwise, the "status" is "success".
        """

        invalid_fields = []
        self._validate(data, path="", invalid_fields=invalid_fields)

        if invalid_fields:
            return {
                "status": "error",
                "invalid_fields": invalid_fields
            }
        else:
            return {"status": "success"}

    def _validate(self, data, path, invalid_fields):
        """
        Recursively validate the JSON for null values.

        This method traverses the JSON structure recursively, checking each field for
        null values.

        :param data: The current data to validate (dict, list, or primitive type).
        :param path: The current path in the JSON hierarchy (e.g., "user.address.city").
        :param invalid_fields: A list to collect the paths of fields with null values.
        """

        if data is None:
            if path not in self.optional_fields:
                invalid_fields.append(path)
        elif isinstance(data, dict):
            for key, value in data.items():
                new_path = f"{path}.{key}" if path else key
                self._validate(value, new_path, invalid_fields)
        elif isinstance(data, list):
            for index, value in enumerate(data):
                new_path = f"{path}[{index}]"
                self._validate(value, new_path, invalid_fields)
