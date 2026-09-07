from __future__ import annotations

import csv
import os
import random
import smtplib
from email.message import EmailMessage
from pathlib import Path

QUOTES = (
    "The best way to predict the future is to invent it. — Alan Kay",
    "A dream does not become reality through magic; it takes sweat, determination, and hard work. — Colin Powell",
    "Success is not the key to happiness. Happiness is the key to success. — Albert Schweitzer",
    "Do not watch the clock; do what it does. Keep going. — Sam Levenson",
    "The only limit to our realization of tomorrow is our doubts of today. — Franklin D. Roosevelt",
)


def load_recipients(csv_path: Path) -> list[tuple[str, str]]:
    recipients: list[tuple[str, str]] = []
    with csv_path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or not {"name", "email"} <= set(reader.fieldnames):
            raise ValueError("CSV must contain name and email columns.")
        for row in reader:
            name = row["name"].strip()
            email = row["email"].strip()
            if email:
                recipients.append((name or "there", email))
    return recipients


def build_message(sender: str, recipient: str, name: str, quote: str) -> EmailMessage:
    message = EmailMessage()
    message["Subject"] = "Your Daily Inspiration"
    message["From"] = sender
    message["To"] = recipient
    message.set_content(f"Hello {name},\n\n{quote}\n\nHave a great day!\n")
    return message


def send_quotes(
    sender: str,
    app_password: str,
    recipients: list[tuple[str, str]],
    *,
    smtp_host: str = "smtp.gmail.com",
    smtp_port: int = 465,
) -> None:
    with smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=20) as server:
        server.login(sender, app_password)
        for name, email in recipients:
            server.send_message(build_message(sender, email, name, random.choice(QUOTES)))


def main() -> int:
    sender = os.getenv("SMTP_SENDER_EMAIL")
    app_password = os.getenv("SMTP_APP_PASSWORD")
    if not sender or not app_password:
        print("Set SMTP_SENDER_EMAIL and SMTP_APP_PASSWORD before running.")
        return 1

    csv_path = Path(os.getenv("RECIPIENTS_CSV", "recipients.csv"))
    try:
        recipients = load_recipients(csv_path)
        if not recipients:
            raise ValueError("No recipients were found.")
        send_quotes(sender, app_password, recipients)
    except (OSError, ValueError, smtplib.SMTPException) as exc:
        print(f"Unable to send quotes: {exc}")
        return 1

    print(f"Sent {len(recipients)} message(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
