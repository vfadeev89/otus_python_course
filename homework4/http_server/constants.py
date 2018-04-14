REQUEST_QUEUE_SIZE = 5
BUFFER_SIZE = 1024

PROTOCOL_VERSION = "HTTP/1.1"
ALLOWED_METHODS = ("GET", "HEAD")
SERVER_VERSION = "Otus Http Server"
INDEX_FILE = "index.html"
CRLF = "\r\n"
HTTP_HEAD_TERMINATOR = CRLF * 2

OK = 200
BAD_REQUEST = 400
FORBIDDEN = 403
NOT_FOUND = 404
NOT_ALLOWED = 405

STATUS_CODES = {
    OK: "OK",
    FORBIDDEN: "Forbidden",
    BAD_REQUEST: "Bad Request",
    NOT_FOUND: "Not Found",
    NOT_ALLOWED: "Method Not Allowed"
}

CONTENT_TYPE = {
    "text": "text/plain",
    "html": "text/html",
    "css": "text/css",
    "js": "application/javascript",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
    "gif": "image/gif",
    "swf": "application/x-shockwave-flash"
}
