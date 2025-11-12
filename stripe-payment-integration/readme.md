# 💳 Stripe Payment Integration API

Flask API for secure payment processing with Stripe.

## ✨ Features
- ✅ Stripe checkout session
- ✅ Webhook handling
- ✅ Payment confirmation
- ✅ Multiple products support
- ✅ Success/Cancel pages

## 🚀 Quick Start
```bash
pip install flask stripe
python app.py
```

## 🔧 Configuration

Replace in code:
```python
stripe.api_key = "sk_test_YOUR_KEY"
WEBHOOK_SECRET = "whsec_YOUR_SECRET"
```

## 📡 API Endpoints

**Create Payment:**
```bash
POST /buy/basic
```

**Webhook:**
```bash
POST /webhook
```

## 💻 Tech Stack
- Python Flask
- Stripe API
- Webhooks

## 📫 Contact
For payment integration services: fahad.integration.ml@gmail.com