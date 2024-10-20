class Customer:
    """
    This class represent a customer
    Attributes:
        id (UUID): customer id
        name (str): customer name
        plan_id (UUID): plan suscription id
        date_suscription (Timestamp): date suscription
    """
    def __init__(self, id, name,plan_id,date_suscription):
        self.id=id
        self.name=name
        self.plan_id=plan_id
        self.date_suscription=date_suscription