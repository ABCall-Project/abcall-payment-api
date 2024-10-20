from uuid import UUID
from typing import Optional
from datetime import datetime
class Issue:
    """
    This class represent a Issue reported by customer
    Attributes:
        id (UUID) : issue id
        auth_user_id (UUID): user reporter id
        auth_user_agent_id (UUID): agent id
        status (UUID): issue status
        subject (str): issue subject
        description (str): description of issue
        created_at (datetime): when was created
        closed_at (datetime): when was closed
        channel_plan_id (UUID): channel plan id
    """
    def __init__(self, id:UUID,auth_user_id:UUID,auth_user_agent_id:UUID,
                 status:UUID,subject:str,description:str,created_at:datetime,
                 closed_at:datetime,channel_plan_id:UUID):
        self.id=id
        self.auth_user_id=auth_user_id
        self.auth_user_agent_id=auth_user_agent_id
        self.status=status
        self.subject=subject
        self.description=description
        self.created_at=created_at
        self.closed_at=closed_at
        self.channel_plan_id=channel_plan_id


    def to_dict(self):
        return {
            'id': str(self.id),
            'auth_user_id': str(self.auth_user_id),
            'auth_user_agent_id': str(self.auth_user_agent_id),
            'status': str(self.status),
            'subject': str(self.subject),
            'description': str(self.description),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'closed_at': self.closed_at.isoformat() if self.closed_at else None,
            'channel_plan_id': str(self.channel_plan_id)
        }