"""Erreurs JSON homogènes pour toute l'API."""

from __future__ import annotations

from http import HTTPStatus

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

ERROR_KEYS = {
    400: "bad_request",
    401: "unauthorized",
    403: "forbidden",
    404: "not_found",
    405: "method_not_allowed",
    413: "payload_too_large",
    415: "unsupported_media_type",
    429: "rate_limited",
    500: "internal_error",
}

GENERIC_MESSAGES = {
    404: "This endpoint does not exist.",
    405: "This method is not allowed for this endpoint.",
    413: "The request body is too large.",
    415: "The request content type is not supported.",
    429: "Too many requests. Try again later.",
    500: "An unexpected error occurred.",
}


class ApiError(Exception):
    """Erreur métier rendue en JSON avec un code HTTP explicite."""

    def __init__(
        self,
        error: str,
        message: str,
        status: int = 400,
        fields: dict[str, str] | None = None,
    ) -> None:
        super().__init__(message)
        self.error = error
        self.message = message
        self.status = status
        self.fields = fields


def _payload(error: str, message: str, fields: dict[str, str] | None = None) -> dict:
    body: dict = {"error": error, "message": message}
    if fields:
        body["fields"] = fields
    return body


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(ApiError)
    def handle_api_error(error: ApiError):
        return jsonify(_payload(error.error, error.message, error.fields)), error.status

    @app.errorhandler(HTTPException)
    def handle_http_error(error: HTTPException):
        status = error.code or 500
        key = ERROR_KEYS.get(status, "http_error")
        message = GENERIC_MESSAGES.get(status)
        if message is None:
            known = status in HTTPStatus._value2member_map_
            message = HTTPStatus(status).phrase if known else "Error"
        response = jsonify(_payload(key, message))
        response.status_code = status
        return response

    @app.errorhandler(Exception)
    def handle_unexpected_error(error: Exception):
        app.logger.exception("unhandled_exception")
        return jsonify(_payload("internal_error", GENERIC_MESSAGES[500])), 500
