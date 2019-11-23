# LeapFinance
Assignment for LeapFinance

Django Application is deployed here: http://leap-finance-crawler.us-east-1.elasticbeanstalk.com

An already created user can be used:

User: sumit <br/>
Pass: sumit

Admin Console is enabled to visualize or edit the model data. Same user can be used to login here: http://leap-finance-crawler.us-east-1.elasticbeanstalk.com/admin/


{{host}}/spider/ shows a Django Form to submit any link to be scraped and wait for 3-10 seconds while scrapping happens and then populates the data on page.

If the scraping takes more time then user can leave the screen and come back later and submit the same url in the above endpoint. This time if the scrapped data is already in DB then it'll just be retrieved from DB and shown on the screen.
