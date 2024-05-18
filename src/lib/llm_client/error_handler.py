import requests

class ErrorHandler:
    @staticmethod
    def handle_exception(e: Exception) -> dict:
        if isinstance(e, requests.exceptions.HTTPError):
            return ErrorHandler.handle_http_error(e)
        elif isinstance(e, requests.exceptions.ConnectionError):
            return {
                "status": "error",
                "type": "APIConnectionError",
                "message": "Check your network settings, proxy configuration, SSL certificates, or firewall rules.",
            }
        elif isinstance(e, requests.exceptions.Timeout):
            return {
                "status": "error",
                "type": "APITimeoutError",
                "message": "Request timed out. Retry your request after a brief wait.",
            }
        else:
            return {
                "status": "error",
                "type": "UnexpectedError",
                "message": str(e),
            }

    @staticmethod
    def handle_http_error(e: requests.exceptions.HTTPError) -> dict:
        error_map = {
            401: ("AuthenticationError", "Invalid, expired, or revoked API key."),
            400: ("BadRequestError", "Malformed request or missing parameters."),
            404: ("NotFoundError", "Resource not found."),
            429: ("RateLimitError", "Rate limit exceeded."),
            500: ("InternalServerError", "Server error. Retry later."),
        }
        error_type, message = error_map.get(e.response.status_code, ("HTTPError", "An HTTP error occurred."))
        return {"status": "error", "type": error_type, "message": message}





    # def _handle_exception(self, e: Exception) -> Dict[str, str]:
    #     if isinstance(e, requests.exceptions.HTTPError):
    #         return self._handle_http_error(e)
    #     elif isinstance(e, requests.exceptions.ConnectionError):
    #         return {
    #             "status": "error",
    #             "type": "APIConnectionError",
    #             "message": "Check your network settings, proxy configuration, SSL certificates, or firewall rules.",
    #         }
    #     elif isinstance(e, requests.exceptions.Timeout):
    #         return {
    #             "status": "error",
    #             "type": "APITimeoutError",
    #             "message": "Request timed out. Retry your request after a brief wait.",
    #         }
    #     else:
    #         return {
    #             "status": "error",
    #             "type": "UnexpectedError",
    #             "message": str(e),
    #         }

    # def _handle_http_error(self, e: requests.exceptions.HTTPError) -> Dict[str, str]:
    #     error_map = {
    #         401: ("AuthenticationError", "Invalid, expired, or revoked API key."),
    #         400: ("BadRequestError", "Malformed request or missing parameters."),
    #         404: ("NotFoundError", "Resource not found."),
    #         429: ("RateLimitError", "Rate limit exceeded."),
    #         500: ("InternalServerError", "Server error. Retry later."),
    #     }
    #     error_type, message = error_map.get(
    #         e.response.status_code, ("HTTPError", "An HTTP error occurred.")
    #     )
    #     return {"status": "error", "type": error_type, "message": message}
