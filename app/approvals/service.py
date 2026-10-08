import sqlite3,os,uuid
from pathlib import Path
from fastapi import HTTPException
from app.security.authorization import require_permission,can_view_order
DB=os.getenv('APPROVAL_DB','approvals_demo.sqlite')
def _connect():
 c=sqlite3.connect(DB,timeout=10);c.execute('CREATE TABLE IF NOT EXISTS approvals (id TEXT PRIMARY KEY, order_id TEXT NOT NULL, amount REAL NOT NULL, status TEXT NOT NULL, owner TEXT NOT NULL, refund_id TEXT)');return c
def propose_refund(order_id:str,principal:dict)->dict:
 if not can_view_order(principal,order_id):raise HTTPException(403,'Not entitled')
 action={'id':str(uuid.uuid4()),'order_id':order_id,'amount':5.0,'currency':'USD','status':'PENDING'}
 with _connect() as c:c.execute('INSERT INTO approvals(id,order_id,amount,status,owner) VALUES(?,?,?,?,?)',(action['id'],order_id,action['amount'],'PENDING',principal['id']))
 return action
def confirm_refund(approval_id:str,principal:dict,idempotency_key:str)->dict:
 require_permission(principal,'refunds:approve')
 if idempotency_key!=f'{approval_id}:confirm:v1':raise HTTPException(400,'Invalid idempotency key')
 with _connect() as c:
  c.execute('BEGIN IMMEDIATE')
  row=c.execute('SELECT order_id,status,owner,refund_id FROM approvals WHERE id=?',(approval_id,)).fetchone()
  if not row:raise HTTPException(404,'Approval not found')
  order_id,status,owner,refund_id=row
  if owner!=principal['id'] or not can_view_order(principal,order_id):raise HTTPException(403,'Not entitled')
  if status=='APPROVED_DEMO_ONLY':return {'status':status,'refund_id':refund_id}
  if status!='PENDING':raise HTTPException(409,'Action not pending')
  refund_id=f'demo-refund-{approval_id}'
  c.execute('UPDATE approvals SET status=?,refund_id=? WHERE id=?',('APPROVED_DEMO_ONLY',refund_id,approval_id))
  return {'status':'APPROVED_DEMO_ONLY','refund_id':refund_id}
