import string
from functools import wraps
from rest_framework.response import Response
from rest_framework import status


def base62_encode(num):
    """
     Encode a number into a base62 string.

    This function encodes a positive integer into a base62 string. Base62 encoding
    uses a combination of lowercase and uppercase letters along with digits (0-9) to
    represent numbers. The resulting string is formed by selecting characters from
    the ASCII alphabet.

    Args:
        num (int): The number to be encoded.

    Returns:
        str: The base62-encoded string representing the input number.
    """
    alphabet = string.ascii_letters + string.digits
    base = len(alphabet)
    encoded = ''
    while num > 0:
        num, remainder = divmod(num, base)
        encoded = alphabet[remainder] + encoded
    return encoded


def generate_short_url(company_name, long_url, given_number):
    """
     Generate a shortened URL and corresponding slug.

    This function generates a shortened URL and a corresponding slug for a given long URL.
    It first hashes the long URL to generate a unique identifier, then encodes the hash
    into a base62 string. The given number is appended to the slug to ensure uniqueness.
    The shortened URL is formed by concatenating the company name with the slug.

    Args:
        company_name (str): The base URL of the company or service.
        long_url (str): The original URL to be shortened.
        given_number (int): A number provided to ensure uniqueness of the slug.

    Returns:
        tuple: A tuple containing the shortened URL and its corresponding slug.
    """
    hash_code = hash(long_url) % (10 ** 10)
    slug = base62_encode(hash_code) + str(given_number)
    short_url = company_name + "/" + slug
    return short_url, slug


def handle_api_exceptions(func):
    """
    Decorator to handle exceptions in API views.

    This decorator is used to wrap API view functions to catch any exceptions that occur
    during their execution. It ensures that exceptions are properly handled and do not
    propagate beyond the view function. If an exception occurs, it returns a JSON response
    with a failure message and the error details, along with an HTTP status code of 400 (Bad Request).
    :param func:
    :return:
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_message = str(e)
            return Response({'message': 'failed', 'error': error_message}, status=status.HTTP_400_BAD_REQUEST)
    return wrapper
