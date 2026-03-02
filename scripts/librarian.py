import imaplib
import email
from email.header import decode_header
import os
import re
import time
from datetime import datetime

# Path Configuration
CRED_DIR = "/home/openclaw/.openclaw/credentials/imap"
KB_DIR = "/home/openclaw/.openclaw/knowledge-base"

def clean_filename(text):
    return re.sub(r'[^\w\s-]', '', text).strip().replace(' ', '_').lower()

def get_librarian_credentials():
    with open(f"{CRED_DIR}/user", 'r') as f:
        user = f.read().strip()
    with open(f"{CRED_DIR}/pass", 'r') as f:
        password = f.read().strip()
    return user, password

def html_to_markdown(html_content):
    # Simple regex-based tag stripping as a fallback for missing BeautifulSoup
    clean = re.compile('<.*?>')
    return re.sub(clean, '', html_content)

def fetch_newsletters():
    user, password = get_librarian_credentials()
    
    try:
        print(f"Connecting to imap.gmail.com as {user}...")
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        print("Logging in...")
        mail.login(user, password)
        mail.select("inbox")

        # Search for unseen messages
        print("Searching for UNSEEN...")
        status, messages = mail.search(None, '(UNSEEN)')
        
        if status != 'OK':
            print("Failed to search inbox.")
            return

        message_ids = messages[0].split()
        total = len(message_ids)
        print(f"Found {total} new messages.")
        
        for i, num in enumerate(message_ids):
            if i > 0:
                print(f"Waiting for sequential processing (Message {i+1}/{total})...")
                time.sleep(5) 

            status, data = mail.fetch(num, '(RFC822)')
            msg = email.message_from_bytes(data[0][1])
            
            subject_header = decode_header(msg["Subject"])[0]
            subject = subject_header[0]
            if isinstance(subject, bytes):
                encoding = subject_header[1]
                subject = subject.decode(encoding or "utf-8")
            
            sender = msg.get("From")
            date_str = datetime.now().strftime("%Y-%m-%d")
            filename = f"{date_str}_{clean_filename(subject)}.md"
            filepath = os.path.join(KB_DIR, filename)

            content = f"# {subject}\n\n**Source:** {sender}\n**Date:** {date_str}\n\n---\n\n"
            
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/plain":
                        try:
                            body = part.get_payload(decode=True).decode()
                            content += body
                            break
                        except:
                            pass
                    elif content_type == "text/html":
                        try:
                            html_body = part.get_payload(decode=True).decode()
                            content += html_to_markdown(html_body)
                            break
                        except:
                            pass
            else:
                content_type = msg.get_content_type()
                try:
                    body = msg.get_payload(decode=True).decode()
                    if content_type == "text/html":
                        content += html_to_markdown(body)
                    else:
                        content += body
                except:
                    content += "[Error decoding body]"

            with open(filepath, 'w') as f:
                f.write(content)
            
            print(f"✅ Saved: {filename}")

        mail.logout()
        
        if message_ids:
            # Note: QMD indexing skipped due to system environment issues
            print("✅ New content saved to knowledge base.")

    except Exception as e:
        print(f"❌ Librarian error: {str(e)}")

if __name__ == "__main__":
    fetch_newsletters()
