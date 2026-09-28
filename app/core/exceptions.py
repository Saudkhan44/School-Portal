from fastapi import HTTPException, status


class AppException(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        code: str | None = None,
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.code = code or "app_exception"
        super().__init__(message)


class NotFoundError(AppException):
    def __init__(self, message: str, code: str = "not_found") -> None:
        super().__init__(message=message, status_code=status.HTTP_404_NOT_FOUND, code=code)


class ValidationError(AppException):
    def __init__(self, message: str, code: str = "validation_error") -> None:
        super().__init__(message=message, status_code=status.HTTP_400_BAD_REQUEST, code=code)


class UnauthorizedError(AppException):
    def __init__(self, message: str = "Unauthorized", code: str = "unauthorized") -> None:
        super().__init__(message=message, status_code=status.HTTP_401_UNAUTHORIZED, code=code)


class ForbiddenError(AppException):
    def __init__(self, message: str = "Forbidden", code: str = "forbidden") -> None:
        super().__init__(message=message, status_code=status.HTTP_403_FORBIDDEN, code=code)


def http_exception_to_app_exception(exc: HTTPException) -> AppException:
    return AppException(
        message=exc.detail if isinstance(exc.detail, str) else str(exc.detail),
        status_code=exc.status_code,
        code="http_exception",
    )
