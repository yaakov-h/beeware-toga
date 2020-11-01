import re
from typing import Optional, Union, List, Callable
from string import ascii_uppercase, ascii_lowercase, digits

INTEGER_REGEX = r"^[0-9]+$"
NUMBER_REGEX = r"^[-]?(\d+|\d*\.\d+|\d+.\d*)$"
EMAIL_REGEX = (
    r"^[a-zA-Z][a-zA-Z0-9\.]*[a-zA-Z0-9]@[a-zA-Z][a-zA-Z0-9]*(\.[a-zA-Z0-9]+)+$"
)


class BooleanValidator:

    def __init__(
        self,
        is_valid_method: Callable[[str], bool],
        error_message: str,
        allow_empty: bool = True
    ):
        self.is_valid_method = is_valid_method
        self.error_message = error_message
        self.allow_empty = allow_empty

    def __call__(self, input_string: str):
        if self.allow_empty and input_string == "":
            return None
        return None if self.is_valid_method(input_string) else self.error_message


class CountValidator:

    def __init__(
        self,
        count_method: Callable[[str], int],
        count: Optional[int],
        expected_existence: str,
        expected_non_existence: str,
        expected_count: str,
        allow_empty: bool = True,
    ):
        self.count_method = count_method
        self.count = count
        self.expected_existence = expected_existence
        self.expected_non_existence = expected_non_existence
        self.expected_count = expected_count
        self.allow_empty = allow_empty

    def __call__(self, input_string: str):
        if self.allow_empty and input_string == "":
            return None
        actual_count = self.count_method(input_string)
        if actual_count == 0 and self.count != 0:
            return self.expected_existence
        if actual_count != 0 and self.count == 0:
            return self.expected_non_existence
        if self.count is not None and actual_count != self.count:
            return self.expected_count
        return None


def min_length(
    length: int, error_message: Optional[str] = None, allow_empty: bool = True
):
    if error_message is None:
        error_message = "Input is too short (length should be at least {})".format(
            length
        )
    return BooleanValidator(
        is_valid_method=lambda a: len(a) >= length,
        error_message=error_message,
        allow_empty=allow_empty,
    )


def max_length(
    length: int, error_message: Optional[str] = None, allow_empty: bool = True
):
    if error_message is None:
        error_message = "Input is too long (length should be at most {})".format(length)
    return BooleanValidator(
        is_valid_method=lambda a: len(a) <= length,
        error_message=error_message,
        allow_empty=allow_empty,
    )


def length_between(
    min_value: int,
    max_value: int,
    error_message: Optional[str] = None,
    allow_empty: bool = True,
):
    return combine(
        min_length(min_value, error_message=error_message, allow_empty=allow_empty),
        max_length(max_value, error_message=error_message, allow_empty=allow_empty),
    )


def startswith(
    substrings: Union[str, List[str]],
    error_message: Optional[str] = None,
    allow_empty: bool = True,
):
    if error_message is None:
        error_message = 'Input should start with "{}"'.format(substrings)
    return BooleanValidator(
        lambda a: a.startswith(substrings),
        error_message=error_message,
        allow_empty=allow_empty,
    )


def endswith(
    substrings: Union[str, List[str]],
    error_message: Optional[str] = None,
    allow_empty: bool = True,
):
    if error_message is None:
        error_message = 'Input should end with "{}"'.format(substrings)
    return BooleanValidator(
        lambda a: a.endswith(substrings),
        error_message=error_message,
        allow_empty=allow_empty,
    )


def contains(
    substrings: Union[str, List[str]],
    count: Optional[int] = None,
    error_message: Optional[str] = None,
    allow_empty: bool = True,
):
    if isinstance(substrings, str):
        substrings = [substrings]

    if error_message is not None:
        expected_non_existence = expected_count = expected_existence = error_message
    else:
        if len(substrings) == 1:
            substrings_string = '"{}"'.format(substrings[0])
        else:
            substrings_string = ", ".join(
                '"{}"'.format(substring) for substring in substrings[:-1]
            ) + ' or "{}"'.format(substrings[-1])
        expected_existence = "Input should contain {}".format(substrings_string)
        expected_non_existence = "Input should not contain {}".format(substrings_string)
        expected_count = "Input should contain {} exactly {} times".format(
            substrings_string, count
        )

    return CountValidator(
        count_method=lambda a: sum(a.count(substring) for substring in substrings),
        count=count,
        expected_existence=expected_existence,
        expected_non_existence=expected_non_existence,
        expected_count=expected_count,
        allow_empty=allow_empty,
    )


def not_contains(
    substring: str, error_message: Optional[str] = None, allow_empty: bool = True
):
    return contains(
        substring, count=0, error_message=error_message, allow_empty=allow_empty
    )


def match_regex(
    regex_string, error_message: Optional[str] = None, allow_empty: bool = True
):
    if error_message is None:
        error_message = "Input should match regex: {}".format(regex_string)
    return BooleanValidator(
        is_valid_method=lambda a: bool(re.search(regex_string, a)),
        error_message=error_message,
        allow_empty=allow_empty,
    )


def contains_uppercase(
    count: Optional[int] = None,
    error_message: Optional[str] = None,
    allow_empty: bool = True,
):
    if error_message is not None:
        expected_non_existence = expected_count = expected_existence = error_message
    else:
        expected_existence = "Input should contain at least one uppercase character"
        expected_non_existence = "Input should not contain uppercase characters"
        expected_count = "Input should contain exactly {} uppercase characters".format(
            count
        )

    return CountValidator(
        count_method=lambda a: len([char for char in a if char in ascii_uppercase]),
        count=count,
        expected_existence=expected_existence,
        expected_non_existence=expected_non_existence,
        expected_count=expected_count,
        allow_empty=allow_empty,
    )


def contains_lowercase(
    count: Optional[int] = None,
    error_message: Optional[str] = None,
    allow_empty: bool = True,
):
    if error_message is not None:
        expected_non_existence = expected_count = expected_existence = error_message
    else:
        expected_existence = "Input should contain at least one lowercase character"
        expected_non_existence = "Input should not contain lowercase characters"
        expected_count = "Input should contain exactly {} lowercase characters".format(
            count
        )

    return CountValidator(
        count_method=lambda a: len([char for char in a if char in ascii_lowercase]),
        count=count,
        expected_existence=expected_existence,
        expected_non_existence=expected_non_existence,
        expected_count=expected_count,
        allow_empty=allow_empty,
    )


def contains_digit(
    count: Optional[int] = None,
    error_message: Optional[str] = None,
    allow_empty: bool = True,
):
    if error_message is not None:
        expected_non_existence = expected_count = expected_existence = error_message
    else:
        expected_existence = "Input should contain at least one digit"
        expected_non_existence = "Input should not contain digits"
        expected_count = "Input should contain exactly {} digits".format(count)

    return CountValidator(
        count_method=lambda a: len([char for char in a if char in digits]),
        count=count,
        expected_existence=expected_existence,
        expected_non_existence=expected_non_existence,
        expected_count=expected_count,
        allow_empty=allow_empty,
    )


def contains_special(
    count: Optional[int] = None,
    error_message: Optional[str] = None,
    allow_empty: bool = True,
):
    if error_message is not None:
        expected_non_existence = expected_count = expected_existence = error_message
    else:
        expected_existence = "Input should contain at least one special character"
        expected_non_existence = "Input should not contain specials characters"
        expected_count = "Input should contain exactly {} special characters".format(
            count
        )

    return CountValidator(
        count_method=lambda a: len(
            [char for char in a if not char.isalpha() and not char.isdigit()]
        ),
        count=count,
        expected_existence=expected_existence,
        expected_non_existence=expected_non_existence,
        expected_count=expected_count,
        allow_empty=allow_empty,
    )


def integer(error_message: Optional[str] = None, allow_empty: bool = True):
    if error_message is None:
        error_message = "Input should be an integer"
    return match_regex(
        INTEGER_REGEX, error_message=error_message, allow_empty=allow_empty
    )


def number(error_message: Optional[str] = None, allow_empty: bool = True):
    if error_message is None:
        error_message = "Input should be a number"
    return match_regex(
        NUMBER_REGEX, error_message=error_message, allow_empty=allow_empty
    )


def email(error_message: Optional[str] = None, allow_empty: bool = True):
    if error_message is None:
        error_message = "Input should be a valid email address"
    return match_regex(EMAIL_REGEX, error_message=error_message, allow_empty=allow_empty)


def combine(*validators):
    """Use this method to combine multiple validators."""

    def combined_validator(input_string):
        for validator in validators:
            error_message = validator(input_string)
            if error_message is not None:
                return error_message
        return None

    return combined_validator

