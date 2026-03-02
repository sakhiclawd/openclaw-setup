import imaplib

def test_connection():
    try:
        user = open('/home/openclaw/.openclaw/credentials/imap/user', 'r').read().strip()
        password = open('/home/openclaw/.openclaw/credentials/imap/pass', 'r').read().strip()
        
        print(f"Connecting to imap.gmail.com as {user}...")
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(user, password)
        print("✅ Login successful!")
        
        status, folders = mail.list()
        if status == 'OK':
            print("✅ Successfully retrieved folder list.")
            
        mail.logout()
        return True
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_connection()
