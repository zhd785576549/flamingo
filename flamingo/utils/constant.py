class HttpStatus:
    HTTP_OK = 200
    HTTP_PAGE_NOT_FOUND = 404
    HTTP_METHOD_DENIED = 405
    HTTP_INTERVAL_ERROR = 500


class ContentType:
    CT_FROM_DATA = "multipart/form-data"
    CT_JSON = "application/json"
    CT_FORM_URLENCODED = "application/x-www-form-urlencoded"


class RequestMethod:
    RM_POST = "POST"
    RM_GET = "GET"
    RM_PUT = "PUT"
    RM_DELETE = "DELETE"
    RM_HEAD = "HEAD"
    RM_OPTION = "OPTION"
