from datetime import date
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from http import HTTPStatus
import requests
import re
import os
import logging
from ..domain.models.issue import Issue

class IssueService:
    """
    This class is for integrate the service with the Issue api
    Attributes:
        base_url (string): the issue api url 
    """

    def __init__(self):
        """
        service constructor 
        Args:
            
        """
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('default')
        self.logger.info(f'Instanced customer service')
        self.base_url = os.environ.get('ISSUE_API_PATH')

    def get_issues_by_customer_list(self,customer_id,year, month):
        """
        method to query all issues by customer
        Args:
            customer_id (uuid): id customer to query
            year (int): year to query
            month (int): month to query
        Return:
            issues (Issues): list issues of customer
        """
        issues=[]
        try:
            
            self.logger.info(f'init consuming api issues {self.base_url}/issue/getIssuesByCustomer?customer_id={customer_id}&year={year}&month={month}')
            response = requests.get(f'{self.base_url}/issue/getIssuesByCustomer?customer_id={customer_id}&year={year}&month={month}')
            self.logger.info(f'quering issues')
            if response.status_code == 200:
                self.logger.info(f'status code 200 quering issues services')
                data = response.json()
                if data:
                    self.logger.info(f'there are issues response ')
                    for item in data:
                        issues.append(Issue(item.get('id'),
                                item.get('auth_user_id'),
                                item.get('auth_user_agent_id'),
                                item.get('status'),
                                item.get('subject'),
                                item.get('description'),
                                item.get('created_at'),
                                item.get('closed_at'),
                                item.get('channel_plan_id')
                        ))
 
                    self.logger.info(f'deserializing issue list')
                    return issues
                    
                else:
                    self.logger.info(f'there arent issues')
                    return None
            else:
                self.logger.info(f"error consuming issue api: {response.status_code}")
                return None
            
        except Exception as e:
            self.logger.info(f"Error comunication with issue api: {str(e)}")
            return None
        