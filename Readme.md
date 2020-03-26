# Limehome coding challenge

# Deploy
Please make sure to run create_database.py first. Then run serverless deploy.

# Live version
You can check it out here:

metrics: https://k6a9kj8a20.execute-api.us-east-1.amazonaws.com/dev/api/metrics/ratings/avg
ui: https://k6a9kj8a20.execute-api.us-east-1.amazonaws.com/dev/


## Data format
* According to the pdf we pick the keys Q8A, Q8B and Q8C from the data. The pdf claims that the range of values is between 1 - 5.
Inspecting the data i can see that they are actually from 0 - 6. So we will use the following rules from the key Q10A:
0=Blank, 1=Unacceptable, 2=Below Average, 3=Average, 4=Good, 5=Outstanding, 6=Never used or visited


## Data storage
* Usually would have used a dedicated data store, for simplicity we will be using a sqlite database
* In real life would have used something like alembic for migrations, again for simplicity we will skip it
* Should have used some prepared statements to not insert random data from the internet
* Decided on a star schema to be able to answer different questions in the future easily
