from login import Oauth_Login
import json
import base64
import re
from bs4 import BeautifulSoup

OPEN_TAG = '<td class="content-excerpt-pattern-container mobile-resize-text "'

def print_id(service):
    f = open('messages.json')
    data = json.load(f)
    
    f.close()
    message = data['messages'][3]['id']
    txt = service.users().messages().get(userId='me', id=message).execute()
    encoded = txt['payload']['parts'][0]['body']['data']
    #print(json.dumps(encoded, indent=4,sort_keys=True))

    decoded = base64.urlsafe_b64decode(encoded).decode("UTF-8")
    print(decoded)
    f = open('index.html', 'w')
    f.write(decoded)
    f.close()
    print(re.search(r'' + OPEN_TAG + '(.*?)</td>',decoded).group(1))

def get_message(service, mid):
    txt = service.users().messages().get(userId='me', id=mid).execute()
    encoded = txt['payload']['parts'][0]['body']['data']

    decoded = base64.urlsafe_b64decode(encoded).decode("UTF-8")
    #print(decoded)
    soup = BeautifulSoup(decoded,"html.parser")
    print('<tr>')
    print(soup.body.find(id="email-content-container"))
    print('</tr>')


def get_mails(service):
    f = open('messages.json')
    data = json.load(f)
    f.close()

    for i in data['messages']:
        #txt = service.users().messages().get(userId='me', id=i['id']).execute()
        #payload = txt['payload']
        
        #for h in payload['headers']:
        #    if h['name'] == 'Subject':
        #        print('<h1>' + h['value'] + '</h1>')
        get_message(service, i['id'])        

def show_labels(service):

    results = service.users().labels().list(userId='me').execute()
    
    print(results)
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])

def main():
    service = Oauth_Login()
    #show_labels(service)
    #print_id(service)
    get_mails(service)
    #get_message(service,'17a0ef31e46815bc')

if __name__ == '__main__':
    main()
