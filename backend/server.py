
from flask import Flask, redirect, request, render_template_string
#from decouple import config
import stripe
#from boto3 import boto3

#AWS_ACCESS_KEY_ID     = config("AWS_ACCESS_KEY_ID")
#AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
#REGION_NAME           = config("REGION_NAME")

#Pass in your own stripe key that you will receive when you sign up for stripe
stripe.api_key = 'sk_test_51Nb4PVFVqhdR7gUTfQBF1vIkACcXMkDUsYXbj6jcW3miha4qy6AYFWwzgOpwP5IRZvBgksKoLJWOA3mBtEPngjDd00eJpXJw8h'

price_id = 'price_1Ngr2AFVqhdR7gUTHNAbOFyq'

#create a variable that checks the user token and confirms the stripe id

app = Flask(__name__,
            static_url_path='',
            static_folder='public')


YOUR_DOMAIN = 'http://localhost:4242'  
FRONT_DOMAIN = 'http://localhost:4040'

#create a checkout session
@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': price_id,
                    'quantity': 1,
                },
            ],
            mode='subscription',
            #redirect you to a success page and triggers a webhook letting you know that the payment succedded. this webhook will be put into a database and will be updated if the payment has failed or the subscription has stopped.
            success_url=FRONT_DOMAIN + '/success' + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=FRONT_DOMAIN + '/cancel/' + '?canceled=true',
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)

'''
@app.route('/customer-portal', methods=['POST'])
def customer_portal():
    try:
        portal_session = stripe.billing_portal.Session.create(
            customer=
        )
'''
# Redirect to the URL returned on the session
#   return redirect(session.url, code=303)

@app.route('/success', methods=['GET'])
def order_success():
  session = stripe.checkout.Session.retrieve(request.args.get('session_id'))
  customer = stripe.Customer.retrieve(session.customer)

  return render_template_string('<html><body><h1>Thanks for your order, {{customer.name}}!</h1></body></html>', customer=customer)


#create route that redircts customer to manage subscriptions

#create a webhook that will update the subscription status inside auth0
@app.route('/webhook', methods=['POST'])
def webhook_received():
    webhook_secret = {{'STRIPE_WEBHOOK_SECRET'}}
    request_data = json.loads(request.data)

    if webhook_secret:
        # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
        signature = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload=request.data, sig_header=signature, secret=webhook_secret)
            data = event['data']
        except Exception as e:
            return e
        # Get the type of webhook event sent - used to check the status of PaymentIntents.
        event_type = event['type']
    else:
        data = request_data['data']
        event_type = request_data['type']
    data_object = data['object']

    if event_type == 'checkout.session.completed':
    # Payment is successful and the subscription is created.
    # You should provision the subscription and save the customer ID to your database.
      print(data)
    elif event_type == 'invoice.paid':
    # Continue to provision the subscription as payments continue to be made.
    # Store the status in your database and check when a user accesses your service.
    # This approach helps you avoid hitting rate limits.
      print(data)
    elif event_type == 'invoice.payment_failed':
    # The payment failed or the customer does not have a valid payment method.
    # The subscription becomes past_due. Notify your customer and send them to the
    # customer portal to update their payment information.
      print(data)
    else:
      print('Unhandled event type {}'.format(event_type))

    return jsonify({'status': 'success'})

if __name__== "__main__":
    app.run(port=4242, debug=True)
    
