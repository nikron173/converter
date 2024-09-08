import urllib.parse
from typing import Dict, Tuple
from email.message import Message


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


def get_length_and_content_type(header: Message) -> Tuple[int, str]:
    length = int(header.get('Content-Length', 0))
    if not length:
        raise Exception('Content-Length - не задан header')
    content_type = header.get('Content-Type', None)
    if not content_type:
        raise Exception('Content-Type - не задан в header')
    return length, content_type
