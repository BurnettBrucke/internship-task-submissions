from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    ConsoleSpanExporter,
    SimpleSpanProcessor,
)


def configure_tracing() -> None:
    resource = Resource.create(
        {
            "service.name": "gateway-service",
        }
    )

    provider = TracerProvider(
        resource=resource,
    )

    provider.add_span_processor(
        SimpleSpanProcessor(
            ConsoleSpanExporter()
        )
    )

    trace.set_tracer_provider(provider)


def get_tracer():
    return trace.get_tracer(
        "day8.gateway"
    )