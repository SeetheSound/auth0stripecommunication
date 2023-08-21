This is the basic connection between auth0 and stripe. When a customer logs in or signs up for the first time auth0 creates a stripe customer id and points them to a checkout page. when the customer selects a product they will be redirected to a stripe checkout to make a purchase.

Every time the customer logs into their account an auth0action will call the customers stripe id to be stored and passed into the manage subscription route on the backend. auth0 permissions will change depending on what the customers does inside the manage subscripton/checkout page. 

1. Build the server

~~~
pip3 install -r requirements.txt
~~~

2. Run the server

~~~
export FLASK_APP=server.py
python3 -m flask run --port=4242
~~~

3. Login to stripe via backend

~~~
stripe login
~~~

4. Run the client app

~~~
npm start
~~~

5. Build the server

~~~
