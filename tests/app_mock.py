from flaskr.app import app

app.config['DATABASE_URI'] = 'sqlite:///data/dbapp.test.sqlite'
app.config['SCHEDULE_BROKER'] = 'azureservicebus://RootManageSharedAccessKey:s7kJ3o2JIMa+Q4iYJe0w3i9lC/dfsRbAT+ASbMgdpoE=@abcall-broker.servicebus.windows.net/'
app.config['TOPIC_SCHEDULE'] = 'invoices-schedule'
app.config['MINUTES_TO_EXECUTE_INVOICES'] = 1
app.config['URL_REPORTS_SERVICE'] = 'http://reports:3008'
app.config['ISSUE_API_PATH'] = 'http://api-customer:3003'
app.config['CUSTOMER_API_PATH'] = 'http://localhost:5003'
