from time import strftime, gmtime
from constants import *


class Response(object):
    def __init__(self, method, code):
        self.method = method
        self.code = code
        self.headers = {}
        # rfc: https://tools.ietf.org/html/rfc2616#section-4.5
        self._general_header()
        # rfc: https://tools.ietf.org/html/rfc2616#section-6.2
        self._response_header()
        self.data = ""

    def set_data(self, data):
        # rfc: https://tools.ietf.org/html/rfc2616#section-14.13
        self.data = data
        self.headers["Content-Length"] = len(data)

    def set_content_type(self, ct):
        # rfc: https://tools.ietf.org/html/rfc2616#section-14.17
        self.headers["Content-Type"] = ct

    def _general_header(self):
        self.headers["Date"] = strftime("%a, %d %b %Y %H:%M:%S GMT", gmtime())
        self.headers["Connection"] = "close"

    def _response_header(self):
        self.headers["Server"] = SERVER_VERSION

    def _get_status_line(self):
        # rfc: https://tools.ietf.org/html/rfc2616#section-6.1
        return "{} {} {}\r\n".format(PROTOCOL_VERSION, self.code, STATUS_CODES[self.code])

    def _get_headers(self):
        return CRLF.join("{}: {}".format(k, v) for k, v in self.headers.items())

    def __str__(self):
        if self.method == "GET":
            return "".join((self._get_status_line(),
                            self._get_headers(),
                            HTTP_HEAD_TERMINATOR,
                            self.data))
        else:
            return "".join((self._get_status_line(),
                            self._get_headers(),
                            HTTP_HEAD_TERMINATOR))
