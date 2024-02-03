from requests import get as http_get
from json import loads as json_load, JSONDecodeError
from .openapi import OpenAPIv3Parser
from .swagger import SwaggerParser
from .parser import BaseParser
from ..utils import is_valid_url


def create_parser(fpath_or_url: str, spec: dict = None) -> SwaggerParser | OpenAPIv3Parser:
    '''returns parser based on doc file'''
    if fpath_or_url and is_valid_url(fpath_or_url):
        res = http_get(fpath_or_url)
        if res.status_code != 200:
            raise ValueError(
                f"server returned status code {res.status_code} offat expects 200 status code"
            )
        try:
            spec = json_load(res.text)
            fpath_or_url = None
        except JSONDecodeError as e:
            raise ValueError("Invalid json data spec file url")

    parser = BaseParser(file_or_url=fpath_or_url, spec=spec)
    if parser.is_v3:
        return OpenAPIv3Parser(file_or_url=fpath_or_url, spec=spec)

    return SwaggerParser(fpath_or_url=fpath_or_url, spec=spec)