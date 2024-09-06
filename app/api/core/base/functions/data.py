import re


def replace_with_null(obj: dict or list, char):
    """
    Recursively traverses a data structure (nested dictionaries and lists) and replaces any
    string matching a specified character with None.

    Parameters:
        obj (dict or list): The dictionary to traverse and modify.
        char (str): The character or string that, if matched, will result in setting
                    the dictionary value to None.

    Returns:
        None: Modifies the dictionary in place.

    Description:
        The function works recursively to explore nested dictionaries and lists. For every string
        that matches 'char', that string is replaced with None. This modification affects the
        original dictionary due to the mutability of dictionary objects in Python.
    """
    # for k, v in obj.items():
    #     if isinstance(v, dict):
    #         replace_with_null(v, char)
    #
    #     elif isinstance(v, list):
    #         for index, list_val in enumerate(v):
    #             if isinstance(list_val, dict) or isinstance(list_val, list):
    #                 replace_with_null(list_val, char)
    #             else:
    #                 v[index] = None if list_val == char else v[index]
    #
    #     else:
    #         obj[k] = None if obj[k] == char else obj[k]

    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, dict):
                replace_with_null(v, char)
            elif isinstance(v, list):
                for index, list_val in enumerate(v):
                    if isinstance(list_val, dict) or isinstance(list_val, list):
                        replace_with_null(list_val, char)
                    else:
                        v[index] = None if list_val == char else list_val
            else:
                obj[k] = None if v == char else v
    elif isinstance(obj, list):
        for index, item in enumerate(obj):
            if isinstance(item, dict) or isinstance(item, list):
                replace_with_null(item, char)
            else:
                obj[index] = None if item == char else item


def pop_if_in(obj, key):
    """
    Removes a key from a dictionary and returns its value if the key is present.

    Parameters:
        obj (dict): The dictionary from which to remove the key.
        key (str): The key to remove.

    Returns:
        The value associated with 'key' if it exists in the dictionary; otherwise, None.

    Description:
        This function checks if a specified 'key' is in the dictionary. If it is, the key-value
        pair is removed from the dictionary and the value is returned. If the key is not present,
        the function returns None.
    """
    if key in obj:
        return obj.pop(key)
    return None


def contains_invalid_characters(s):
    """
    Determines if a given string contains any characters that are not alphanumeric, hyphens,
    or underscores.

    Parameters:
        s (str): The string to check for invalid characters.

    Returns:
        bool: True if the string contains invalid characters, otherwise False.

    Description:
        This function uses a regular expression to search for any characters in the string 's'
        that are not letters (a-z, A-Z), digits (0-9), hyphens (-), or underscores (_). If any such
        characters are found, the function returns True. Otherwise, it returns False.
    """
    pattern = re.compile(r"[^a-zA-Z0-9-_]")
    return bool(pattern.search(s))
