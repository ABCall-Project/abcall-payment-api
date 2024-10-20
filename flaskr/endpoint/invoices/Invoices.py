from flask_restful import Resource
from flask import jsonify, request
import logging
import requests
from ...application.invoice_service import InvoiceService
from http import HTTPStatus
from ...infrastructure.databases import InvoicePostgresqlRepository,InvoiceDetailPostgresqlRepository

from ...utils import Logger

from config import Config

log = Logger()

class Invoices(Resource):

    def __init__(self):
        config = Config()
        self.repository = InvoicePostgresqlRepository(config.DATABASE_URI)
        self.invoice_detail_repository=InvoiceDetailPostgresqlRepository(config.DATABASE_URI)
        self.service = InvoiceService(self.repository,None,self.invoice_detail_repository)
        

    def get(self, action=None):
        if action == 'getInvoices':
            return self.getInvoices()
        elif action=='getTotalCostPending':
            return self.get_total_cost_pending()
        elif action=='getListDetailsInvoiceById':
            return self.get_list_details_invoice_by_id()
        else:
            return {"message": "Action not found"}, 404

    def getInvoices(self):
        try:
            customer_id = request.args.get('customer_id')
            log.info(f'Receive request to get the data from customer_id {customer_id}')
            invoices = self.service.list_invoices_by_customer(customer_id)
            return invoices
        except Exception as ex:
            log.error(f'Some error occurred trying to get the data from {customer_id}: {ex}')
            return {'message': 'Something was wrong trying to get the data'}, HTTPStatus.INTERNAL_SERVER_ERROR


    def post(self, action=None):
        if action == 'generateInvoices':
            return self.generate_invoices()
        else:
            return {"message": "Action not found"}, 404


    def generate_invoices(self):
        self.service.generate_invoices()
        return '',200
    

    def get_total_cost_pending(self):

        try:
            customer_id = request.args.get('customer_id')
            log.info(f'Receive request to get total cost of customer_id {customer_id}')
            total_cost = self.service.get_total_cost_pending(customer_id)
            return {
                'total_cost': float(total_cost)
            }, HTTPStatus.OK
        except Exception as ex:
            log.error(f'Some error occurred trying to get total cost of {customer_id}: {ex}')
            return {'message': 'Something was wrong trying to get total cost'}, HTTPStatus.INTERNAL_SERVER_ERROR
        

    def get_list_details_invoice_by_id(self):
        try:

            log.info(f'Receive request to get invoice details')

            invoice_id = request.args.get('invoice_id')
            invoice_detail_list = self.service.list_details_invoice_by_id(invoice_id)
            list_details = [detail.to_dict() for detail in invoice_detail_list]
            
            return list_details, HTTPStatus.OK
        except Exception as ex:
            log.error(f'Some error occurred trying to get invoice details: {ex}')
            return {'message': 'Something was wrong trying to get invoice details'}, HTTPStatus.INTERNAL_SERVER_ERROR
        
