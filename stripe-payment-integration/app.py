import os
import json
import stripe
import smtplib
from email.message import EmailMessage
from flask import Flask, redirect, request, jsonify
from dotenv import load_dotenv

load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

app = Flask(__name__)

@app.route('/')
def home():
    html_button = """
    <h2>৳5000 এর API buy integration service</h2>
    <form action="/create-checkout-session" method="POST">
        <button type="submit" style="padding:15px;font-size:18px;background:#6772e5;color:white;border:none;border-radius:5px;cursor:pointer;">
            Stripe Checkout start 
        </button>
    </form>
    """
    return html_button


@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'bdt',
                        'unit_amount': 500000, # ৳5000
                        'product_data': {'name': 'API Integration Service'},
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=request.url_root + 'success',
            cancel_url=request.url_root + 'cancel',
        )
        return redirect(checkout_session.url, code=303)

    except Exception as e:
        return jsonify(error="error: " + str(e)), 500

@app.route('/success')
def success():
    return "✅ payment is successful!service is activated"

@app.route('/cancel')
def cancel():
    return "❌ payment cancel!communicate for help"


@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.data
    sig_header = request.headers.get('stripe-signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, WEBHOOK_SECRET
        )
    except Exception as e:
        return 'Invalid request', 400

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        print(f"✅ Payment successful for session: {session['id']}")

        try:
            send_email(
                to_email="client@example.com",
                subject="Payment Successful - Service Activated",
                body="Thanks!your service is activated"
            )
        except Exception as e:
            print("Email not sent:", e)

    return 'Success', 200

def send_email(to_email, subject, body):
    EMAIL = os.getenv("SMTP_USER")
    PASSWORD = os.getenv("SMTP_PASS")
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

    msg = EmailMessage()
    msg["From"] = EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)


if __name__ == '__main__':
    app.run(port=4242, debug=True)