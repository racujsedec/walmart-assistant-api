import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"backend"))
from app.schemas import ChatRequest, OrderInput, OrderResult
from pydantic import ValidationError
import pytest

def test_valid_request():
    assert ChatRequest(message="Where is order 12345?",conversation_id="abc").message.startswith("Where")
def test_empty_question_rejected():
    with pytest.raises(ValidationError): ChatRequest(message="",conversation_id="abc")
def test_bad_order_id_rejected():
    with pytest.raises(ValidationError): OrderInput(order_id="DROP TABLE orders")
def test_result_excludes_private_fields():
    raw={"order_id":"12345","status":"SHIPPED","estimated_delivery":"2026-10-09","customer_name":"Demo Customer"}
    result=OrderResult(**raw).model_dump()
    assert "customer_name" not in result
