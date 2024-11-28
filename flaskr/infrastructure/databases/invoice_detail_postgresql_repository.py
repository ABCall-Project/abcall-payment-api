from sqlalchemy import create_engine,extract, func,select, not_
from sqlalchemy.orm import sessionmaker
from typing import List, Optional
from uuid import UUID
from ...domain.models import InvoiceDetail
from ...domain.interfaces import InvoiceDetailRepository
from ...infrastructure.databases.model_sqlalchemy import Base, InvoiceDetailModelSqlAlchemy
from .postgres.db import Session, engine

class InvoiceDetailPostgresqlRepository(InvoiceDetailRepository):
    def __init__(self):
        self.engine = engine
        self.session = Session
        self._create_tables()

    def _create_tables(self):
        Base.metadata.create_all(self.engine)

    def create_invoice_detail(self,invoice_detail: InvoiceDetail):
         with self.session() as session:
            try:
                session.add(self._to_model(invoice_detail))
                session.commit()
            finally:
                session.close()

   
        
    
    def get_factured_issue_ids(self) -> List[UUID]:
        with self.session() as session:
            try:
                factured_issue_ids = (
                    session.query(InvoiceDetailModelSqlAlchemy.issue_id)
                    .filter(InvoiceDetailModelSqlAlchemy.issue_id.isnot(None))
                    .distinct()
                    .all()
                )
                return [issue_id for (issue_id,) in factured_issue_ids]
            finally:
                session.close()
        
    
    def get_by_invoice_details_by_id(self, invoice_id: str):
        with self.session() as session:
            try:
                details_model= session.query(InvoiceDetailModelSqlAlchemy).filter_by(invoice_id=invoice_id).all()
                return [self._from_model(detail_model) for detail_model in details_model]
            finally:
                session.close()

    def _to_model(self, invoice_detail: InvoiceDetail) -> InvoiceDetailModelSqlAlchemy:
        return InvoiceDetailModelSqlAlchemy(
            id=invoice_detail.id,
            detail=invoice_detail.detail,
            amount=invoice_detail.amount,
            tax=invoice_detail.tax,
            total_amount=invoice_detail.total_amount,
            issue_id=invoice_detail.issue_id,
            chanel_plan_id=invoice_detail.chanel_plan_id,
            invoice_id=invoice_detail.invoice_id,
            issue_date=invoice_detail.issue_date
        )

    def _from_model(self, model: InvoiceDetailModelSqlAlchemy) -> InvoiceDetail:
        return InvoiceDetail(
            id=model.id,
            detail=model.detail,
            amount=model.amount,
            tax=model.tax,
            total_amount=model.total_amount,
            issue_id=model.issue_id,
            chanel_plan_id=model.chanel_plan_id,
            invoice_id=model.invoice_id,
            issue_date=model.issue_date
        )
    

    def get_total_amount_by_invoice_id(self, invoice_id: UUID) -> float:
        with self.session() as session:
            try:
                total_amount = session.query(func.sum(InvoiceDetailModelSqlAlchemy.total_amount)).filter_by(invoice_id=invoice_id).scalar()
                return total_amount if total_amount else 0.0
            finally:
                session.close()