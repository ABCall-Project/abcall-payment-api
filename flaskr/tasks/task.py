from celery import Celery
from celery.schedules import crontab
import os
from  config import Config
from ..application.invoice_service import InvoiceService
from ..infrastructure.databases.invoice_detail_postgresql_repository import InvoiceDetailPostgresqlRepository
from ..infrastructure.databases.invoice_postgresql_repository import InvoicePostgresqlRepository


config=Config()

celery = Celery('tasks', broker=f'{config.SCHEDULE_BROKER}{config.TOPIC_SCHEDULE}')


@celery.task
def scheduled_generate_invoice_task():
    print("generating invoices!")
    '''
    1. determinar el periodo de facturación sería el mes
    2. consultar si se facturó el monto básico sino crear la factura y el detalle
    3. consultar que incidentes no fueron facturados e insertarlos
    4. generar el pdf de la factura.
    '''
 
    
    
    repository_invoice = InvoicePostgresqlRepository(config.DATABASE_URI)
    repository_detail_invoice=InvoiceDetailPostgresqlRepository(config.DATABASE_URI)
    invoice_service=InvoiceService(repository_invoice,None,repository_detail_invoice)
    invoice_service.generate_invoices()


celery.conf.beat_schedule = {
    'run-generate-invoice-schedule': {
        'task': 'flaskr.tasks.task.scheduled_generate_invoice_task',
        'schedule': crontab(minute=f'*/{config.MINUTES_TO_EXECUTE_INVOICES}'),  
    },
}