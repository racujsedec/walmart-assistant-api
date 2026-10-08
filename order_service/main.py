import os
from datetime import date
from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy import create_engine, String, Date, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./orders.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}, pool_pre_ping=True)
class Base(DeclarativeBase): pass
class Order(Base):
    __tablename__ = "orders"
    order_id: Mapped[str] = mapped_column(String(30), primary_key=True)
    status: Mapped[str] = mapped_column(String(30))
    estimated_delivery: Mapped[date] = mapped_column(Date)
    customer_name: Mapped[str] = mapped_column(String(100))
    delivery_address: Mapped[str] = mapped_column(String(200))
Base.metadata.create_all(engine)
with Session(engine) as session:
    if session.get(Order, "12345") is None:
        session.add(Order(order_id="12345", status="SHIPPED", estimated_delivery=date(2026,10,9), customer_name="Demo Customer", delivery_address="Example address"))
        session.commit()
app = FastAPI(title="Example Order Service")
def service_auth(authorization: str | None = Header(default=None)):
    if authorization != "Bearer " + os.getenv("ORDER_API_TOKEN", "local-demo-token"):
        raise HTTPException(401, "Unauthorized service")
@app.get("/orders/{order_id}", dependencies=[Depends(service_auth)])
def read_order(order_id: str):
    with Session(engine) as session:
        order = session.execute(select(Order).where(Order.order_id == order_id)).scalar_one_or_none()
        if order is None: raise HTTPException(404, "Order not found")
        # Deliberately broad internal API contract to demonstrate minimization at tool boundary.
        return {"order_id": order.order_id, "status": order.status, "estimated_delivery": order.estimated_delivery.isoformat(), "customer_name": order.customer_name, "delivery_address": order.delivery_address}
