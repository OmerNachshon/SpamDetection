from Gmail.Google import GmailClient

#constants
GMAIL_CLIENT=GmailClient()

if __name__ == '__main__':
    #print(GMAIL_CLIENT.get_labels())
    mails=GMAIL_CLIENT.get_mails()
    for mail in mails:
        if 'spam' in GMAIL_CLIENT.is_spam(GMAIL_CLIENT.get_message(mail)):
            print(GMAIL_CLIENT.get_message(mail))
            GMAIL_CLIENT.apply_spam_label(mail)

