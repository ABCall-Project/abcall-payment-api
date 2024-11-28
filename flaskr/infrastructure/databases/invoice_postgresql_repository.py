from sqlalchemy import create_engine,extract, func
from sqlalchemy.orm import sessionmaker
from typing import List, Optional
from uuid import UUID
from ...domain.models import Invoice
from ...domain.interfaces import InvoiceRepository
from ...infrastructure.databases.model_sqlalchemy import Base, InvoiceModelSqlAlchemy
from .postgres.db import Session, engine

class InvoicePostgresqlRepository(InvoiceRepository):
    def __init__(self):
        self.engine = engine
        self.session = Session
        self._create_tables()

    def _create_tables(self):
        Base.metadata.create_all(self.engine)
    
    def list_by_consumer_id(self, customer_id) -> List[Invoice]:
        with self.session() as session:
            try:
                invoice_models = session.query(InvoiceModelSqlAlchemy).filter_by(customer_id=customer_id).all()
                return [self._from_model(invoice_model) for invoice_model in invoice_models]
            finally:
                session.close()

    def list(self) -> List[Invoice]:
        with self.session() as session:
            try:
                invoice_models = session.query(InvoiceModelSqlAlchemy).all()
                return [self._from_model(invoice_model) for invoice_model in invoice_models]
            finally:
                session.close()


    def invoice_by_month_year_by_customer(self, year, month,customer_id):
        with self.session() as session:
            try:
                invoice=session.query(InvoiceModelSqlAlchemy.id).filter(
                    extract('year', InvoiceModelSqlAlchemy.created_at) == year,
                    extract('month', InvoiceModelSqlAlchemy.created_at) == month,
                    InvoiceModelSqlAlchemy.customer_id==customer_id).first()
                
                return invoice[0] if invoice else None
            finally:
                session.close()


    def get_invoice_by_id(self, invoice_id: UUID) -> Optional[Invoice]:
        with self.session() as session:
            try:
                invoice_model = session.query(InvoiceModelSqlAlchemy).filter_by(id=invoice_id).first()
                return self._from_model(invoice_model) if invoice_model else None
            finally:
                session.close()

    

    def _to_model(self, invoice: Invoice) -> InvoiceModelSqlAlchemy:
        return InvoiceModelSqlAlchemy(
            id=invoice.id,
            customer_id=invoice.customer_id,
            invoice_id=invoice.invoice_id,
            plan_id=invoice.plan_id,
            amount=invoice.amount,
            tax=invoice.tax,
            total_amount=invoice.total_amount,
            status=invoice.status,
            created_at=invoice.created_at,
            start_at=invoice.start_at,
            generation_date=invoice.generation_date,
            end_at=invoice.end_at,
            plan_amount=invoice.plan_amount,
            issues_amount=invoice.issues_amount
        )

    def _from_model(self, model: InvoiceModelSqlAlchemy) -> Invoice:
        return Invoice(
            id=model.id,
            customer_id=model.customer_id,
            invoice_id=model.invoice_id,
            plan_id=model.plan_id,
            amount=model.amount,
            tax=model.tax,
            total_amount=model.total_amount,
            status=model.status,
            created_at=model.created_at,
            start_at=model.start_at,
            generation_date=model.generation_date,
            end_at=model.end_at,
            plan_amount=model.plan_amount,
            issues_amount=model.issues_amount
        )
    
    def create_invoice(self,invoice: Invoice):
        with self.session() as session:
            try:
                session.add(self._to_model(invoice))
                session.commit()
            finally:
                session.close()

    def update_invoice(self,invoice: Invoice):
        with self.session() as session:
            try:

                session.query(InvoiceModelSqlAlchemy).filter_by(id=invoice.id).update(
                    { 
                        "customer_id":str(invoice.customer_id),
                        "invoice_id":invoice.invoice_id,
                        "plan_id":str(invoice.plan_id),
                        "amount":str(invoice.amount),
                        "tax":str(invoice.tax),
                        "total_amount":str(invoice.total_amount),
                        "status":invoice.status,
                        "created_at": invoice.created_at.isoformat() if invoice.created_at else None,
                        "start_at": invoice.start_at.isoformat() if invoice.start_at else None,
                        "generation_date": invoice.generation_date.isoformat() if invoice.generation_date else None,
                        "end_at":invoice.end_at.isoformat() if invoice.end_at else None,
                        "issues_amount":invoice.issues_amount
                    })
                session.commit()
            finally:
                session.close()


    def sum_total_amount_by_customer_and_status(self, customer_id: UUID, status: UUID):
        """
        summary of total ammount

        :param customer_id: UUID of customer
        :param status: UUID of status invoice
        :return: Summary of total_amount
        """
        with self.session() as session:
            try:
                total_sum = session.query(func.sum(InvoiceModelSqlAlchemy.total_amount)) \
                    .filter(InvoiceModelSqlAlchemy.customer_id == customer_id) \
                    .filter(InvoiceModelSqlAlchemy.status == status) \
                    .scalar()
                print(f'total sum :{total_sum}')
                return total_sum
            except Exception as e:
                return 0
            finally:
                session.close()