import os
import urllib

from response import Response
from constants import *


class Request(object):
    def __init__(self, method, url, version, headers):
        self.method = method
        self.url = url
        self.version = version
        self.headers = headers
        self.valid = False

    @staticmethod
    def create_request(data):
        lines = data.splitlines()
        try:
            request_line = lines[0]
            method, url, version = Request._parse_request_line(request_line)
            headers = {}
            for line in lines[1:]:
                if not line:
                    break
                k, v = Request._parse_header(line)
                headers[k] = v
            request = Request(method, url, version, headers)
            request.valid = True
        except:
            request = Request(None, None, None, None)
        return request

    @staticmethod
    def _parse_request_line(line):
        # rfc: https://tools.ietf.org/html/rfc2616#section-5.1
        parts = [element.strip() for element in line.split()]
        return parts[0], parts[1], parts[2]

    @staticmethod
    def _parse_header(line):
        parts = [element.strip() for element in line.split(":")]
        return parts[0], parts[1]


class RequestHandler(object):
    def __init__(self, request, document_root):
        self.request = request
        self.document_root = document_root
        self.filename = None
        self.response = self._handle_request()

    def is_file_exists(self):
        return os.path.exists(self.filename)

    def _handle_request(self):
        if not self.request.valid:
            return Response(None, BAD_REQUEST)
        if not self.is_method_allowed():
            return Response(self.request.method, NOT_ALLOWED)
        code = self._check_resource()
        if code != OK:
            return Response(self.request.method, code)
        data = self._read_file()
        response = Response(self.request.method, code)
        response.set_content_type(self._get_content_type())
        response.set_data(data)
        return response

    def _check_resource(self):
        file_path = self.request.url.split("?")[0].strip("/")
        file_path = urllib.unquote(file_path).decode("utf-8")
        filename = os.path.realpath(os.path.join(self.document_root, file_path))
        longest_prefix = os.path.commonprefix([self.document_root, filename])
        if longest_prefix != self.document_root:
            return FORBIDDEN
        if os.path.isdir(filename):
            filename = os.path.join(filename, INDEX_FILE)
            possible_error = FORBIDDEN
        else:
            possible_error = NOT_FOUND
        if not os.path.exists(filename):
            return possible_error
        self.filename = filename
        return OK

    def _get_content_type(self):
        _, ext = os.path.splitext(self.filename)
        if ext:
            return CONTENT_TYPE.get(ext.strip("."), CONTENT_TYPE["text"])
        return CONTENT_TYPE["text"]

    def _read_file(self):
        with open(self.filename, mode="rb") as f:
            return f.read()

    def is_method_allowed(self):
        return self.request.method in ALLOWED_METHODS
