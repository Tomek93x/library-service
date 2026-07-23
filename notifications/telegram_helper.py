import os

import requests
from django.conf import settings


def send_telegram_message(message):
    """Send a message to Telegram chat via Bot API."""
    bot_token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID

    if not bot_token or not chat_id:
        print("Telegram credentials not configured. Skipping notification.")
        return False

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML",
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        print(f"Failed to send Telegram message: {e}")
        return False


def notify_new_borrowing(borrowing):
    """Send notification about new borrowing."""
    message = (
        f"📚 <b>New Borrowing Created</b>\n\n"
        f"Book: {borrowing.book.title}\n"
        f"Author: {borrowing.book.author}\n"
        f"Borrowed by: {borrowing.user.email}\n"
        f"Borrow date: {borrowing.borrow_date}\n"
        f"Expected return: {borrowing.expected_return_date}\n"
    )
    send_telegram_message(message)


def notify_overdue_borrowing(borrowing):
    """Send notification about overdue borrowing."""
    from datetime import date

    days_overdue = (date.today() - borrowing.expected_return_date).days

    message = (
        f"⚠️ <b>Overdue Borrowing Alert</b>\n\n"
        f"Book: {borrowing.book.title}\n"
        f"Author: {borrowing.book.author}\n"
        f"Borrowed by: {borrowing.user.email}\n"
        f"Expected return: {borrowing.expected_return_date}\n"
        f"Days overdue: {days_overdue}\n"
    )
    send_telegram_message(message)


def notify_successful_payment(payment):
    """Send notification about successful payment."""
    message = (
        f"✅ <b>Payment Successful</b>\n\n"
        f"Payment ID: {payment.id}\n"
        f"Type: {payment.type}\n"
        f"Amount: ${payment.money_to_pay}\n"
        f"Book: {payment.borrowing.book.title}\n"
        f"User: {payment.borrowing.user.email}\n"
    )
    send_telegram_message(message)
