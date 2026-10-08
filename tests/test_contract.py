from app.rag.chunk import chunk_text
from app.rag.retrieve import search_policy
from app.schemas.tools import OrderInput,OrderResult
from app.rag.fusion import reciprocal_rank_fusion
import pytest
def test_order_id_rejects_injection():
 with pytest.raises(Exception):OrderInput(order_id='12345 OR 1=1')
def test_no_pii_in_result():
 raw={'order_id':'12345','status':'SHIPPED','customer_name':'private'}
 out=OrderResult(order_id=raw['order_id'],status=raw['status']).model_dump()
 assert 'customer_name' not in out
def test_chunk_overlap():assert chunk_text('abcdefghij',6,2)==['abcdef','efghij']
def test_policy_evidence():assert search_policy('delayed shipment refund approval')[0]['id'].startswith('policy-')
def test_rrf():assert reciprocal_rank_fusion([['a','b'],['b','a']])==['a','b'] or reciprocal_rank_fusion([['a','b'],['b','a']])==['b','a']
