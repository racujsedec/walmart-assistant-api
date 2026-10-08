import os
def setup_tracing(app):
 if os.getenv('OTEL_ENABLED')!='true':return
 from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
 FastAPIInstrumentor.instrument_app(app)
