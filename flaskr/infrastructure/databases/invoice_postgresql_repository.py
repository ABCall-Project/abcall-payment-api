from sqlalchemy import create_engine,extract, func
from sqlalchemy.orm import sessionmaker
from typing import List, Optional
from uuid import UUID
from ...domain.models import Invoice
from ...domain.interfaces import InvoiceRepository
from ...infrastructure.databases.model_sqlalchemy import Base, InvoiceModelSqlAlchemy

class InvoicePostgresqlRepository(InvoiceRepository):
    def __init__(self, connection_string: str):
        self.engine = create_engine(connection_string)
        self.Session = sessionmaker(bind=self.engine)
        self._create_tables()

    def _create_tables(self):
        Base.metadata.create_all(self.engine)
    
    def list_by_consumer_id(self, customer_id) -> List[Invoice]:
        session = self.Session()
        try:
            invoice_models = session.query(InvoiceModelSqlAlchemy).filter_by(customer_id=customer_id).all()
            return [self._from_model(invoice_model) for invoice_model in invoice_models]
        finally:
            session.close()

    def list(self) -> List[Invoice]:
        session = self.Session()
        try:
            invoice_models = session.query(InvoiceModelSqlAlchemy).all()
            return [self._from_model(invoice_model) for invoice_model in invoice_models]
        finally:
            session.close()


    def invoice_by_month_year_by_customer(self, year, month,customer_id):
        session = self.Session()

        invoice=session.query(InvoiceModelSqlAlchemy.id).filter(
            extract('year', InvoiceModelSqlAlchemy.created_at) == year,
            extract('month', InvoiceModelSqlAlchemy.created_at) == month,
            InvoiceModelSqlAlchemy.customer_id==customer_id).first()
          
        return invoice[0] if invoice else None

    

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
            end_at=invoice.end_at
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
            end_at=model.end_at
        )
    
    def create_invoice(self,invoice: Invoice):
        session = self.Session()
        session.add(self._to_model(invoice))
        session.commit()

    def update_invoice(self,invoice: Invoice):
        session = self.Session()
        session.query(InvoiceModelSqlAlchemy).filter_by(id=invoice.id).update(
            { 
                "customer_id":str(invoice.customer_id),
                "invoice_id":invoice.invoice_id,
                "payment_id":str(invoice.payment_id),
                "amount":str(invoice.amount),
                "tax":str(invoice.tax),
                "total_amount":str(invoice.total_amount),
                "subscription":invoice.subscription,
                "subscription_id":str(invoice.subscription_id),
                "status":invoice.status,
                "created_at": invoice.created_at.isoformat() if invoice.created_at else None,
                "updated_at": invoice.updated_at.isoformat() if invoice.updated_at else None,
                "generation_date": invoice.generation_date.isoformat() if invoice.generation_date else None,
                "period":invoice.period.isoformat() if invoice.generation_date else None,
            })
        session.commit()