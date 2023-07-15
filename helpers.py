import re


def try_parse_strength(strength):
    """
    Attempts to parse the given string into a float. Will let
    error bubble up if `strength` is not convertible into float.
    """
    cleaned_strength = re.sub(r"[^0-9.]", r"", strength)
    return float(cleaned_strength)
