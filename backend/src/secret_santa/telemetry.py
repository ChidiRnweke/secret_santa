from opentelemetry.sdk.resources import Resource

from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import (
    OTLPLogExporter,
)
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.metrics import set_meter_provider
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
import logging

from secret_santa.config import AppConfig


def configure_telemetry(app_config: AppConfig):
    resource = Resource.create({"service.name": "secret santa"})
    configure_metrics(app_config.telemetry_endpoint, resource)
    configure_logs(app_config.telemetry_endpoint, resource)


def configure_metrics(endpoint: str, telemetry_resource: Resource):
    metric_exporter = OTLPMetricExporter(endpoint=endpoint, insecure=True)
    metric_reader = PeriodicExportingMetricReader(metric_exporter)
    meter_provider = MeterProvider([metric_reader], telemetry_resource)
    set_meter_provider(meter_provider)


def configure_logs(endpoint: str, telemetry_resource: Resource):
    log_exporter = OTLPLogExporter(endpoint=endpoint, insecure=True)

    logger_provider = LoggerProvider(resource=telemetry_resource)

    handler = LoggingHandler(level=logging.DEBUG, logger_provider=logger_provider)
    logging.getLogger("app_logger").addHandler(handler)
    logging.getLogger("app_logger").setLevel(logging.DEBUG)
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))
    set_logger_provider(logger_provider)
