import os
from sqlalchemy import create_engine,Column,String,select
from sqlalchemy.orm import DeclarativeBase,Session
from fastapi import FastAPI,HTTPException
class Base(DeclarativeBase):pass
class Order(Base):
 __tablename__='orders'
 order_id=Column(String,primary_key=True);status=Column(String);estimated_delivery=Column(String);customer_name=Column(String);delivery_address=Column(String)
engine=create_engine(os.getenv('DATABASE_URL','sqlite:///./orders_demo.db'),connect_args={'check_same_thread':False} if os.getenv('DATABASE_URL','sqlite:///./orders_demo.db').startswith('sqlite') else {})
Base.metadata.create_all(engine)
with Session(engine) as s:
 if s.get(Order,'12345') is None:s.add(Order(order_id='12345',status='SHIPPED',estimated_delivery='2026-10-12',customer_name='PRIVATE DEMO NAME',delivery_address='PRIVATE DEMO ADDRESS'));s.commit()
app=FastAPI(title='Synthetic Order Service')
@app.get('/orders/{order_id}')
def get_order(order_id:str):
 with Session(engine) as s:
  row=s.execute(select(Order).where(Order.order_id==order_id)).scalar_one_or_none()
  if row is None:raise HTTPException(404,'Order not found')
  return {'order_id':row.order_id,'status':row.status,'estimated_delivery':row.estimated_delivery,'customer_name':row.customer_name,'delivery_address':row.delivery_address}
