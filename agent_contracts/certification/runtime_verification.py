import asyncio
from collections import defaultdict

from confluent_kafka import Consumer
from loguru import logger

from agent_contracts.certification.config import RuntimeVerificationConfig
from agent_contracts.certification.proto import parse_span
from agent_contracts.certification.workers import certify_span
from agent_contracts.core.datatypes.trace.semcov import (
    RELARI_TRACER,
    ResourceAttributes,
)
from agent_contracts.core.utils.telemetry import telemetry_event
from agent_contracts.core.utils.trace_attributes import get_attribute_value


def preprocess(span_data: dict):
    spans_by_trace_id = defaultdict(list)
    for resource in span_data["resourceSpans"]:
        x = get_attribute_value(resource["resource"], "service.name")
        if x != RELARI_TRACER:
            continue
        for scope in resource["scopeSpans"]:
            for span in scope["spans"]:
                span["resource"] = resource["resource"]
                span["attributes"].append(
                    {"key": "otel.scope.name", "value": scope["scope"]["name"]}
                )
                spans_by_trace_id[span["traceId"]].append(span)
    return spans_by_trace_id


@telemetry_event(name="start_certification_server")
def start_certification_server():
    consumer = Consumer(RuntimeVerificationConfig.kafka.to_confluent_config())
    consumer.subscribe([RuntimeVerificationConfig.kafka.topic])
    try:
        logger.info("Waiting for messages, press Ctrl+C to stop.")
        while True:
            msg = consumer.poll(0.05)
            span_data, format_type = parse_span(msg)
            if span_data:
                logger.info(f"Received msg, type: {format_type}")
                spans_by_trace_id = preprocess(span_data)
                for trace_id, spans in spans_by_trace_id.items():
                    certification_enabled = any(
                        [
                            get_attribute_value(
                                span["resource"],
                                ResourceAttributes.CERTIFICATION_ENABLED,
                            )
                            for span in spans
                        ]
                    )
                    if certification_enabled:
                        if RuntimeVerificationConfig.debug:
                            asyncio.run(certify_span(trace_id, spans))
                        else:
                            certify_span.send(trace_id, spans)
                    else:
                        logger.info(f"[{trace_id}] Certification disabled, skipping...")
    except KeyboardInterrupt:
        logger.info("Quitting...")
    finally:
        consumer.close()


def main():
    start_certification_server()


if __name__ == "__main__":
    main()
