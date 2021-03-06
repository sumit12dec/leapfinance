# LeapFinance
Assignment for LeapFinance

### Application is hosted using Elastic Beanstalk by AWS here: 

Django Application can be accessed here: http://leap-finance-crawler.us-east-1.elasticbeanstalk.com

An already created user can be used:

`User: sumit` <br/>
`Pass: sumit`

Admin Console is enabled to visualize or edit the model data. Same user can be used to login here: http://leap-finance-crawler.us-east-1.elasticbeanstalk.com/admin/


# How to setup the application?

`virtualenv -p python venv`

`source venv/bin/activate`

`pip install -r requirements.txt`

Note: Make sure to add the `ACCESS_KEY_ID` and `SECRET_ACCESS_KEY` in `extractor/utils/aws.py` else few functionality might not run.

# How to run the application?

`python manage.py runserver`

# How to run the tests?

`python manage.py test`

{{host}}/spider/ shows a Django Form to submit any link to be scraped and wait for 3-10 seconds while scrapping happens and then populates the data on page.

If the scraping takes more time then user can leave the screen and come back later and submit the same url in the above endpoint. This time if the scrapped data is already in DB then it'll just be retrieved from DB and shown on the screen.


# AWS Lambda Code

Code deployed in AWS Lambda can be seen under <b>extractor</b> folder. `lambda_function.py` is the entry module

## Architecture Diagram


<img src="./lp_architecture_diagram.png" />


## AWS Configuration Details
# Capacity
Server Type: AWS AMI Linux<br/>
Max: 4<br/>
Min: 1<br/>
Scale down increment: -1<br/>
Scale up increment: 1<br/>
Availability Zones: Any<br/>
Breach duration: 5<br/>
Scaling cooldown: 360 seconds<br/>
Environment type: load balancing, auto scaling<br/>
Instance type: t2.micro<br/>

# Load Balancer

Listeners: 1<br/>
Load balancing across multiple Availability Zones enabled: disabled<br/>
Interval: 10<br/>
Unhealthy threshold: 5<br/>
Healthy threshold: 3<br/>
Load balancer type: classic<br/>
Timeout: 5<br/>

# Software

NumProcesses: 1<br/>
NumThreads: 15<br/>
WSGIPath: crawler/wsgi.py<br/>
Static files: /static/="static/"<br/>

# Technologies Used

EC2, Load Balancer, Auto Scaling Group, S3, DynamoDB, Scrapy Web Framework, Python, Django, SQLite DB, AWS Elasticbeanstalk, AWS Lambda, Boto3.
