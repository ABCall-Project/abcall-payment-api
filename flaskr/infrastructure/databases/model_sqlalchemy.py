from sqlalchemy import Column,ForeignKey, String, Numeric, DateTime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

Base = declarative_base()

class InvoiceModelSqlAlchemy(Base):
    __tablename__ = 'invoice'

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(PG_UUID(as_uuid=True), nullable=True)
    invoice_id = Column(String(50), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    tax = Column(Numeric(10, 2), nullable=False)
    plan_id = Column(PG_UUID(as_uuid=True), nullable=True)
    status = Column(PG_UUID(as_uuid=True), nullable=True) 
    total_amount = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    generation_date = Column(DateTime(timezone=True), nullable=False)
    start_at = Column(DateTime(timezone=True), nullable=False)
    end_at = Column(DateTime(timezone=True), nullable=False)
    plan_amount = Column(Numeric(10, 2), nullable=True)
    issues_amount = Column(Numeric(10, 2), nullable=True)


class InvoiceDetailModelSqlAlchemy(Base):
    __tablename__ ='invoice_detail'
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    detail = Column(String(255), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    tax = Column(Numeric(10, 2), nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    issue_id = Column(PG_UUID(as_uuid=True), nullable=True)
    chanel_plan_id = Column(PG_UUID(as_uuid=True), nullable=True)
    invoice_id = Column(PG_UUID(as_uuid=True),ForeignKey('invoice.id'), nullable=True)
    plan = relationship("InvoiceModelSqlAlchemy")
    issue_date = Column(DateTime(timezone=True), nullable=True)