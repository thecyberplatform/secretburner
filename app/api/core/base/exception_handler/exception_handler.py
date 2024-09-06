import copy
import json
from rest_framework.views import exception_handler


def list_values_to_message(list_data):
    """
    Converts a list of string values into a single space-separated string.

    Parameters:
        list_data (list of str): List containing string elements.

    Returns:
        str: A single string composed of all elements joined by a space.
    """
    return " ".join(list_data)


def convert_to_detail_string(data):
    """
    Converts a list of error dictionaries into a formatted string that summarizes the errors.
    Each dictionary may contain a 'field' key and will always contain a 'detail' key.

    Parameters:
        data (list of dict): A list of dictionaries containing error details.

    Returns:
        str: A formatted string summarizing the errors, structured as 'field_name: detail_message'
             if 'field' is present, concatenated with spaces in between.
    """
    result = []

    for obj in data:
        if "field" in obj and "detail" in obj:
            result.append(f"{obj['field']}: {obj['detail']}")

        elif "detail" in obj:
            result.append(obj["detail"])

    return " ".join(result)


def format_and_flatten_data(data, data_key, data_branching):
    """
    Flattens nested dictionary or list structures into a list of dictionaries, each containing
    error details. Useful for restructuring nested API error responses into a more uniform format.

    Parameters:
        data (dict or list): Original nested data structure.
        data_key (str): Current key path to maintain context for nested structures.
        data_branching (bool): Indicates if full path should be maintained in the key names.

    Returns:
        list of dict: Flattened list of error details.
    """
    if isinstance(data, list):
        return [{"detail": list_values_to_message(data)}]

    result = []
    for key, value in data.items():
        new_key = (
            (f"{data_key}_{key}" if data_key else key)
            if data_branching
            else (data_key if data_key else key)
        )

        if isinstance(value, list):
            result.append({"field": new_key, "detail": list_values_to_message(value)})

        elif isinstance(value, dict):
            new_branching = len(value) > 1
            result.extend(format_and_flatten_data(value, new_key, new_branching))

    return result


def format_error_data(error_message="", code=None):
    data = {}

    if code is not None:
        data["code"] = code

    data["detail"] = error_message
    data["errors"] = [{"detail": error_message}]

    content = str.encode(json.dumps(data))

    return data, content


def custom_exception_handler(exc, context):
    """
    Custom exception handler that reformat and standardizes error responses from Django REST Framework.

    Parameters:
        exc: Exception instance that has been raised.
        context: Contextual information about the current execution state.

    Returns:
        Response: Modified Response object with standardized error structure.
    """
    response = exception_handler(exc, context)

    if response is not None:
        original_data = copy.deepcopy(response.data)
        response.data = {}

        if "detail" in original_data:
            response.data["detail"] = str(original_data["detail"])
            response.data["errors"] = [{"detail": response.data["detail"]}]
        else:
            branching = isinstance(original_data, dict) and len(original_data) > 1
            flattened_data = format_and_flatten_data(original_data, "", branching)

            response.data["errors"] = flattened_data
            response.data["detail"] = convert_to_detail_string(flattened_data)

        # Add exception code if available. In most cases this will be "invalid" which is rest_frameworks default
        # validation error code.
        if getattr(exc, "default_code", None):
            response.data["code"] = exc.default_code

    return response
