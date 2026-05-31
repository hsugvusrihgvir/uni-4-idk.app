import os
import smtplib
from email.message import EmailMessage
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_KEY = os.getenv("MAIL_KEY")
MAIL_FROM = os.getenv("MAIL_FROM", MAIL_USERNAME)

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.mail.ru")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))


def send_auth_code(email: str, code: str) -> None:
    if not MAIL_USERNAME:
        raise RuntimeError("MAIL_USERNAME is not set")
    if not MAIL_KEY:
        raise RuntimeError("MAIL_KEY is not set")
    if not MAIL_FROM:
        raise RuntimeError("MAIL_FROM is not set")

    msg = EmailMessage()
    msg["Subject"] = "Код подтверждения"
    msg["From"] = MAIL_FROM
    msg["To"] = email
    msg.set_content(
        f"""Ваш код подтверждения: {code}

Код действует 5 минут.
Если вы не запрашивали код, просто проигнорируйте это письмо.
"""
    )

    try:
        print(code)
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
            server.login(MAIL_USERNAME, MAIL_KEY)
            server.send_message(msg)
    except smtplib.SMTPAuthenticationError:
        raise RuntimeError("Invalid MAIL_USERNAME or MAIL_KEY")
    except Exception as e:
        raise RuntimeError(f"Failed to send email: {e}")
