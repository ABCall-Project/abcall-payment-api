from datetime import date
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from http import HTTPStatus
import requests
import re
import os
import logging
from ..domain.models.customer import Customer

class CustomerService:
    """
    This class is for integrate the service with the Customer api
    Attributes:
        base_url (string): the customer api url 
    """

    def __init__(self):
        """
        service constructor 
        Args:
            
        """
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('default')
        self.logger.info(f'Instanced customer service')
        self.base_url = os.environ.get('CUSTOMER_API_PATH')

    def get_customer_list(self):
        """
        method to query all customers
        Args:
            none
        Return:
            customers (Customer): list of customer object
        """
        customers=[]
        try:
            
            self.logger.info(f'init consuming api customers {self.base_url}/customer/getCustomerList')
            response = requests.get(f'{self.base_url}/customer/getCustomerList')
            self.logger.info(f'quering customers')
            if response.status_code == 200:
                self.logger.info(f'status code 200 queryng customer services')
                data = response.json()
                if data:
                    self.logger.info(f'there are customer response ')
                    for item in data:


                        customers.append(Customer(item.get('id'),
                                item.get('name'),
                                item.get('plan_id'),
                                item.get('date_suscription')                       
                        ))
 
                    self.logger.info(f'deserializing customer list')
                    return customers
                    
                else:
                    self.logger.info(f'there arent customers')
                    return None
            else:
                self.logger.info(f"error consuming customer api: {response.status_code}")
                return None
            
        except Exception as e:
            self.logger.info(f"Error comunication with customer api: {str(e)}")
            return None
        


    def get_customer_plan_rate(self,customer_id):
        """
        method to query customer plan rate
        Args:
            none
        Return:
            rate (float): rate base value
        """
        rate=0
        try:
            
            self.logger.info(f'init consuming api customers {self.base_url}/customer/getRateByCustomer?customer_id={customer_id}')
            response = requests.get(f'{self.base_url}/customer/getRateByCustomer?customer_id={customer_id}')
            self.logger.info(f'quering customer rate')
            if response.status_code == 200:
                self.logger.info(f'status code 200 quering customer rate service')
                data = response.json()
                if data:
                    self.logger.info(f'there are customer response ')
                    rate=data.get('basic_monthly_rate')

                    return rate
                    
                else:
                    self.logger.info(f'there arent response')
                    return None
            else:
                self.logger.info(f"error consuming customer rate api: {response.status_code}")
                return None
            
        except Exception as e:
            self.logger.info(f"Error comunication with customer rate api: {str(e)}")
            return None
        

    def get_customer_plan_issue_fee(self,customer_id):
        """
        method to query customer issue fee
        Args:
            customer_id (Customer): customer id
        Return:
            fee (float): issue fee
        """
        fee=0
        try:
            
            self.logger.info(f'init consuming api customers {self.base_url}/customer/get_issue_fee_by_customer?customer_id={customer_id}')
            response = requests.get(f'{self.base_url}/customer/get_issue_fee_by_customer?customer_id={customer_id}')
            self.logger.info(f'quering customer issue fee')
            if response.status_code == 200:
                self.logger.info(f'status code 200 quering customer issue fee service')
                data = response.json()
                if data:
                    self.logger.info(f'there are customer issue fee response ')
                    fee=data.get('issue_fee')

                    return fee
                    
                else:
                    self.logger.info(f'there arent response')
                    return None
            else:
                self.logger.info(f"error consuming customer fee api: {response.status_code}")
                return None
            
        except Exception as e:
            self.logger.info(f"Error comunication with customer fee api: {str(e)}")
            return None