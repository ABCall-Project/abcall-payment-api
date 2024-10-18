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

            issue_fee=self.customer_service.get_customer_plan_issue_fee(item.id)
            self.log.info(issue_fee)
            if invoice_id is None: # no existe la factura
                self.log.info('no existe la factura')
                #consultar el valor base
                base_monthly_rate=self.customer_service.get_customer_plan_rate(item.id)
                
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
                            end_at=datetime.fromisoformat(item.date_suscription) + timedelta(days=30)
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
                    chanel_plan_id=None
                )
                self.invoice_detail_repository.create_invoice_detail(new_detail)
                invoice_id=new_invoice.id
               
            
            #insertar los incidentes reportados como detalles de factura
            issue_list=self.issue_service.get_issues_by_customer_list(item.id, year, month)
            
           
            for item in issue_list:
                self.log.info(f'issues solveds {item.id}')
                self.log.info(f'Type of issue.id: {type(item.id)}')
                
            if issue_list:
                #consultar los incidentes reportados y si existen entonces crear un detalle por cada incidente reportado
                
                all_billed_issues=self.invoice_detail_repository.get_factured_issue_ids()

                for item in all_billed_issues:
                    self.log.info(f'issues billed {item}')
                    self.log.info(f'Type of billed_id: {type(item)}')

                for issue in issue_list:
                    issue_uuid = UUID(issue.id)
                    if issue_uuid not in all_billed_issues:
                        new_detail = InvoiceDetail(
                            id=uuid.uuid4(),
                            detail=f'cost by issue solved {issue.id}',
                            invoice_id=invoice_id,
                            issue_id=issue.id,
                            amount=issue_fee,
                            tax=0,
                            total_amount=issue_fee,
                            chanel_plan_id=issue.channel_plan_id 
                        )
                        self.invoice_detail_repository.create_invoice_detail(new_detail)


            #updating amount  invoice
            invoice_to_update=self.repository.get_invoice_by_id(invoice_id)
            total_value=self.invoice_detail_repository.get_total_amount_by_invoice_id(invoice_id)
            invoice_to_update.amount=total_value
            invoice_to_update.total_amount=total_value
            self.repository.update_invoice(invoice_to_update)


            # now+=1
            # self.log.info(f'generating invoice I{now}')
            # new_invoice=Invoice(uuid.uuid4(),
            #                     item.id,
            #                     f'I{now}',
            #                     uuid.uuid4(),
            #                     item.plan_rate,
            #                     0,
            #                     item.plan_rate,
            #                     'Emprendedor',
            #                     uuid.uuid4(),
            #                     'G', #Generada con éxito
            #                     datetime.now(),
            #                     None,
            #                     datetime.now(),
            #                     datetime.now()
            #                     )
            # self.repository.create_invoice(new_invoice)
            # #generating invoice
            # if self.__send_invoice_to_document(new_invoice)==False:
            #     #error creating pdf document
            #     new_invoice.status='E' # no fue posible generar la factura
            #     self.repository.update_invoice(new_invoice)


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