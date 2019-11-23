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


### AWS Details
# Capacity
Server Type: AWS AMI Linux
Max: 4
Min: 1
Scale down increment: -1
Scale up increment: 1
Availability Zones: Any
Breach duration: 5
Scaling cooldown: 360 seconds
Placement:
Environment type: load balancing, auto scaling
Instance type: t2.micro

# Load Balancer

Listeners: 1
Load balancing across multiple Availability Zones enabled: disabled
Interval: 10
Unhealthy threshold: 5
Healthy threshold: 3
Load balancer type: classic
Timeout: 5
