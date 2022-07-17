import base64
import datetime
import pickle
import warnings
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

warnings.filterwarnings("ignore")
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import string
from nltk.corpus import stopwords
stopwords.words('english')[0:10]

class GmailClient:
    SPAM_LBL = 'Label_3164355819646382579'
    def __init__(self):
        self.API='AIzaSyDIC1dRI3roEXPpV6c_GKtvo0H6kRRrLJA'
        self.CLIENT_FILE='Gmail/client_secret.json'
        self.API_NAME='gmail'
        self.API_VERSION='v1'
        self.SCOPES=['https://mail.google.com/']
        self.service=self.Create_Service(self.CLIENT_FILE,self.API_NAME,self.API_VERSION,self.SCOPES)

    def Create_Service(self,client_secret_file, api_name, api_version, *scopes):
        print(client_secret_file, api_name, api_version, scopes, sep='-')
        CLIENT_SECRET_FILE = client_secret_file
        API_SERVICE_NAME = api_name
        API_VERSION = api_version
        SCOPES = [scope for scope in scopes[0]]
        #print(SCOPES)

        cred = None
        working_dir = os.getcwd()
        token_dir = 'token files'

        pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'
        # print(pickle_file)

        ### Check if token dir exists first, if not, create the folder
        if not os.path.exists(os.path.join(working_dir, token_dir)):
            os.mkdir(os.path.join(working_dir, token_dir))

        if os.path.exists(os.path.join(working_dir, token_dir, pickle_file)):
            with open(os.path.join(working_dir, token_dir, pickle_file), 'rb') as token:
                cred = pickle.load(token)

        if not cred or not cred.valid:
            if cred and cred.expired and cred.refresh_token:
                cred.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
                cred = flow.run_local_server()

            with open(os.path.join(working_dir, token_dir, pickle_file), 'wb') as token:
                pickle.dump(cred, token)

        try:
            service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
            print(API_SERVICE_NAME, 'service created successfully')
            return service
        except Exception as e:
            print(e)
            print(f'Failed to create service instance for {API_SERVICE_NAME}')
            os.remove(os.path.join(working_dir, token_dir, pickle_file))
            return None

    def convert_to_RFC_datetime(self,year=1900, month=1, day=1, hour=0, minute=0):
        dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
        return dt

    def get_mails(self, labelIds=None):
        if labelIds is None:
            labelIds = ['INBOX']
        results = self.service.users().messages().list(userId='me', labelIds=labelIds).execute()
        messages = results.get('messages', [])
        messages=[self.service.users().messages().get(userId='me',id=msg['id']).execute() for msg in messages]
        return messages

    @staticmethod
    def create_message(sender,to,subject,message_text):
        message=MIMEText(message_text)
        message['to']=to
        message['from']=sender
        message['subject']=subject

        raw_message=base64.urlsafe_b64encode(message.as_string().encode("utf-8"))
        return {
            'raw':raw_message.decode("utf-8")
        }

    def send_message(self,message):
        try:
            message=self.service.users().messages().send(userId='me',body=message).execute()
            print('Message Id: %s' % message['id'])
            return message
        except Exception as e:
            print('An error occurred: %s' % e)
            return None


    def text_process(mess):
        nopunc = [char for char in mess if char not in string.punctuation]
        nopunc = ''.join(nopunc)
        return [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]

    @staticmethod
    def is_spam(str_input):  # determines if message is spam or not
        with open('Gmail/model.pkl', 'rb') as fp:
            model=pickle.load(fp)
        with open('Gmail/tfidf_vectorizer.pkl', 'rb') as fp1:
            vect = pickle.load(fp1)
            cleaned_text=GmailClient.text_process(mess=str_input)
            if len(cleaned_text)==0:
                cleaned_text.append('')
            cleaned_text_tfidf = vect.transform(cleaned_text)
            res=model.predict(cleaned_text_tfidf)
            return res


    def get_sender(self,msg):  # get sender email address from the message
        for header in msg['payload']['headers']:
            if header['name'] == 'From':
                return header['value']

    def create_description(self,msg):  # creating the description  , title = "suicidal" {default}
        desc = "sender :\n"
        for str in self.get_sender(msg):
            desc += str
        str += "\n"
        for str in msg['snippet']:
            desc += str
        return str

    def get_message(self,msg):
        return msg['snippet']

    def get_labels(self):
        results = self.service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])
        return labels

    def switch_labels(self,mail,add_labels=[],remove_labels=[]):
        body={
            "addLabelIds": [
                label for label in add_labels
            ],
            "removeLabelIds": [
                label for label in remove_labels
            ]
        }
        result = self.service.users().messages().modify(userId='me', id=mail['id'], body=body).execute()

    def apply_spam_label(self,mail):
        body = {
            "addLabelIds": [
                self.SPAM_LBL
            ],
            "removeLabelIds": [
            ]
        }
        result = self.service.users().messages().modify(userId='me', id=mail['id'], body=body).execute()


