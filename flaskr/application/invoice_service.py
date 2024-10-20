from typing import List
from ..domain.models import Invoice,InvoiceDetail
import requests
from ..domain.interfaces.invoice_repository import InvoiceRepository
from ..domain.interfaces.customer_repository import CustomerRepository
from ..domain.interfaces.invoice_detail_repository import InvoiceDetailRepository
from ..infrastructure.mappers import InvoiceMapper
import uuid
from datetime import datetime,timedelta
from ..utils import Logger
from  config import Config
from .customer_service import CustomerService
from .issues_service import IssueService
from ..domain.constants import *
from uuid import UUID
class InvoiceService:
    def __init__(self, repository: InvoiceRepository,customer_repository: CustomerRepository=None,invoice_detail_repository: InvoiceDetailRepository=None):
        self.log = Logger()
        self.repository = repository
        self.customer_repository=customer_repository
        self.customer_service=CustomerService()
        self.invoice_detail_repository=invoice_detail_repository
        self.issue_service=IssueService()

    def list_invoices_by_customer(self, customer_id)->str:
        invoices = self.repository.list_by_consumer_id(customer_id)
        mapper = InvoiceMapper()
        json_response =  mapper.list_response(invoices)
        return json_response
    
    def generate_invoices(self)->str:
        self.log.info('generating invoices')
        customers=self.customer_service.get_customer_list()
        self.log.info(customers)
        for item in customers:
            '''
            1. determinar el periodo de facturación sería el mes
            2. consultar si se facturó el monto básico sino crear la factura y el detalle
            3. consultar que incidentes no fueron facturados e insertarlos
            4. generar el pdf de la factura.
            '''
            #1. determinar el periodo de facturación 
            current_date = datetime.now()
            year = current_date.year
            month = current_date.month
            now = int(datetime.now().strftime("%Y%m%d%H%M"))

            #2. consultar si se facturó el monto básico sino crear la factura y el detalle
            invoice_id=self.repository.invoice_by_month_year_by_customer(year,month,item.id)
            #consultar el valor base
            base_monthly_rate=self.customer_service.get_customer_plan_rate(item.id)
            issue_fee=self.customer_service.get_customer_plan_issue_fee(item.id)
            self.log.info(issue_fee)
            if invoice_id is None: # no existe la factura
                self.log.info('no existe la factura')
                
                
                self.log.info(base_monthly_rate)
                
                # insertar la factura 
                new_invoice=Invoice(
                            id=uuid.uuid4(),
                            customer_id=item.id,
                            invoice_id=f'I{now}',
                            plan_id=item.plan_id,
                            amount=base_monthly_rate,
                            tax=0,
                            total_amount=base_monthly_rate,
                            status=STATUS_INVOICE_GENERATED,
                            created_at=datetime.now(),
                            start_at=item.date_suscription,
                            generation_date=datetime.now(),
                            end_at=datetime.fromisoformat(item.date_suscription) + timedelta(days=30),
                            plan_amount=base_monthly_rate,
                            issues_amount=0
                            )
                self.repository.create_invoice(new_invoice)

                self.log.info(f'id factura {new_invoice.id}')
                
                #insertar el detalle del valor base
                new_detail=InvoiceDetail(
                    id=uuid.uuid4(),
                    detail='Base monthly rate',
                    invoice_id=new_invoice.id,
                    issue_id=None,
                    amount=base_monthly_rate,
                    tax=0,
                    total_amount=base_monthly_rate,
                    chanel_plan_id=None,
                    issue_date=None
                )
                self.invoice_detail_repository.create_invoice_detail(new_detail)
                invoice_id=new_invoice.id
               
            
            #insertar los incidentes reportados como detalles de factura
            issue_list=self.issue_service.get_issues_by_customer_list(item.id, year, month)
            
                
            if issue_list:
                #consultar los incidentes reportados y si existen entonces crear un detalle por cada incidente reportado
                
                all_billed_issues=self.invoice_detail_repository.get_factured_issue_ids()


                for issue in issue_list:
                    issue_uuid = UUID(issue.id)
                    if issue_uuid not in all_billed_issues:
                        print(f'this is the issue date {issue.created_at}')
                        new_detail = InvoiceDetail(
                            id=uuid.uuid4(),
                            detail=f'cost by issue solved {issue.id}',
                            invoice_id=invoice_id,
                            issue_id=issue.id,
                            amount=issue_fee,
                            tax=0,
                            total_amount=issue_fee,
                            chanel_plan_id=issue.channel_plan_id,
                            issue_date=issue.created_at
                        )
                        self.invoice_detail_repository.create_invoice_detail(new_detail)


            #updating amount  invoice
            invoice_to_update=self.repository.get_invoice_by_id(invoice_id)
            total_value=self.invoice_detail_repository.get_total_amount_by_invoice_id(invoice_id)
            invoice_to_update.amount=total_value
            invoice_to_update.total_amount=total_value
            invoice_to_update.issues_amount = (float(total_value) if total_value is not None else 0) - (float(base_monthly_rate) if base_monthly_rate is not None else 0)
            self.repository.update_invoice(invoice_to_update)

            #generating invoice
            if self.__send_invoice_to_document(invoice_to_update)==False:
                #error creating pdf document
                invoice_to_update.status=STATUS_INVOICE_GENERATED_WITH_ERROR # no fue posible generar la factura
                self.repository.update_invoice(invoice_to_update)


    def __send_invoice_to_document(self,invoice: Invoice):
        """
        method to send invoice to create document pdf 
        Args:
            invoice (Invoice): invoice to process
        Return:
           None
        """
        try:
            config=Config()
            data={
                "id":str(invoice.id),
                "customer_id":str(invoice.customer_id),
                "invoice_id":str(invoice.invoice_id),
                "plan_id":str(invoice.plan_id),
                "amount":str(invoice.amount),
                "tax":str(invoice.tax),
                "total_amount":str(invoice.total_amount),
                "status":str(invoice.status),
                "created_at": invoice.created_at.isoformat() if invoice.created_at else None,
                "start_at": invoice.start_at.isoformat() if invoice.start_at else None,
                "generation_date": invoice.generation_date.isoformat() if invoice.generation_date else None,
                "end_at":invoice.end_at.isoformat() if invoice.end_at else None,
            }
            self.log.info('calling endpoint to generate pdf invoice ')
            response = requests.post(f'{config.URL_REPORTS_SERVICE}/invoice',json=data)
            self.log.info('api reports called')
            if response.status_code == 200:
                self.log.info('invoice created')
                data = response.json()
                self.log.info('invoice generated successfull')
                return True
            else:
                self.log.error(f'error in service to generate pdf invoice {response.status_code}')
                return False
            
        except Exception as e:
            self.log.error(f'Comunication error with reports service: {str(e)}')
            return False
        


    def get_total_cost_pending(self, customer_id: UUID ):
        """
        This method query total cost of invoices
        Args: 
            customer_id (UUID): customer id
        Returns:
            total_cost: (decimal)
        """
        total_cost=self.repository.sum_total_amount_by_customer_and_status(customer_id,STATUS_INVOICE_GENERATED)
        print(f'total cost {total_cost}')
        return total_cost if total_cost is not None else 0
    

    def list_details_invoice_by_id(self,invoice_id):
        """
        This method query all invoice details
        Args: 
            invoice_id (UUID): invoice id

        Returns:
            invoice details (list): list of invoice details
        """
        list_invoice_details=self.invoice_detail_repository.get_by_invoice_details_by_id(invoice_id)
        return list_invoice_details