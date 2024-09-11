import urllib.parse
from http.client import BAD_REQUEST
from typing import Dict, Tuple, List
from email.message import Message
from src.error.application_error import ApplicationError


def get_dict_query_url(query: str) -> Dict[str, str]:
    data = {}
    for parameter in query.split('&'):
        key, value = parameter.split('=')
        data[key] = urllib.parse.quote(value)
    return data


def get_dict_form(data: str) -> Dict[str, str]:
    dict_data = {}
    for parameter in data.split('&'):
        key, value = parameter.split('=')
        dict_data[key] = urllib.parse.unquote(value)
    return dict_data


def get_length_and_content_type(header: Message) -> Tuple[int, List[str]]:
    length = int(header.get('Content-Length', 0))
    if not length:
        raise ApplicationError('Content-Length - не задан header', BAD_REQUEST)
    content_types = header.get('Content-Type', None)
    if content_types:
        content_types = [type.strip() for type in header.get('Content-Type', None).split(';')]
    if not content_types:
        raise ApplicationError('Content-Type - не задан в header', BAD_REQUEST)
    return length, content_types
