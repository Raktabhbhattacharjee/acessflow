"""Context variables for request lifecycle tracking."""

from contextvars import ContextVar

# Store request_id across async task contexts
request_id_context: ContextVar[str] = ContextVar("request_id", default=None)
