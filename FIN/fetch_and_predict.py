import imaplib
import email
import requests


IMAP_SERVER = "imap.gmail.com"
EMAIL = "rishabdevilliers2005@gmail.com"
PASSWORD = "vrqb eeeh vifa juuj"
N_EMAILS = 5   # How many recent emails to fetch
API_URL = "http://127.0.0.1:8000/predict_email"  #  FastAPI endpoint


def fetch_emails():
    """Fetch latest N emails from Gmail inbox"""
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, PASSWORD)
    mail.select("inbox")

    # Get all email IDs
    status, messages = mail.search(None, "ALL")
    email_ids = messages[0].split()

    # Pick the last N emails
    latest_ids = email_ids[-N_EMAILS:]

    results = []
    for eid in latest_ids:
        status, msg_data = mail.fetch(eid, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])

        subject = msg["subject"] or ""
        body = ""

        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    try:
                        body = part.get_payload(decode=True).decode()
                    except:
                        body = part.get_payload()
                    break
        else:
            try:
                body = msg.get_payload(decode=True).decode()
            except:
                body = msg.get_payload()

        results.append({"subject": subject, "body": body})

    return results

def classify_emails(emails):
    """Sending  emails to FastAPI for prediction (batch)"""
    resp = requests.post("http://127.0.0.1:8000/predict_batch", json={"emails": emails})
    if resp.status_code == 200:
        results = resp.json()["results"]
        for r in results:
            print("\n--- Email ---")
            print("Subject:", r["text"][:80])  # show first 80 chars
            print("Prediction:", r["prediction"])
            print("Probabilities:", r["probabilities"])
    else:
        print("Error:", resp.json())


if __name__ == "__main__":
    emails = fetch_emails()
    classify_emails(emails)