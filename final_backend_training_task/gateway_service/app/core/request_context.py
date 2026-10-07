from contextvars import ContextVar


request_id_ctx: ContextVar[str | None] = ContextVar(
    "request_id",
    default=None,
)

correlation_id_ctx: ContextVar[str | None] = ContextVar(
    "correlation_id",
    default=None,
)


def get_request_id() -> str | None:
    return request_id_ctx.get()


def get_correlation_id() -> str | None:
    return correlation_id_ctx.get()