from __future__ import print_function
import datetime
import re
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


startAddress='Tracker'+os.sep+'start.txt'
updateAddress='Tracker'+os.sep+'trackerUpdate.txt'



# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            # print(calendar_list_entry['id'])
            # print("=======\n"+str(calendar_list_entry)+"=======\n")
            # print(calendar_list_entry['summary'])
            # Call the Calendar API
            now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

            # print(calendar_list_entry['summary'] == "Z LOG")
            if calendar_list_entry['summary'] == "Z LOG":
                
                f = open(updateAddress, "r")
                fread=f.read().replace("  \n","")
                arguments=fread.split(', ') # dont forget to repladce time format " \n"
                print(arguments)
                category=''
                summary=''
                if len(arguments)==3:
                    intent=arguments[0]
                    summary=arguments[1]
                    time=str(arguments[2])
                elif len(arguments)==4:
                    intent=arguments[0]
                    summary=arguments[1]
                    category=arguments[2]
                    time=str(arguments[3])
                elif len(arguments)==2:
                    intent=arguments[0]
                    time=str(arguments[1])
                print("\n |"+str(intent)+"| INTENT")

                if str(intent).lower()=="finish":
                    print("\n FINISHING")
                    endSummary=''
                    if summary:
                        endSummary=summary

                    startFile = open(startAddress, "r")
                    startContent=startFile.read()
                    startArguments=startContent.split(', ') # dont forget to repladce time format " \n"
                    print(startArguments)
                    startFile.close()
                    

                    
                    addtime=fread
                    search=re.sub('((\d*-)(\d*-)(\d*)T(\d*):)(\d*)(:(\d*))', "\g<6>", addtime)
                    splitHolder=search.split(', ')
                    search=splitHolder
                    search=search[len(search)-1]
                    search=int(search)
                    print(search)
                    if search!=59:
                        search=search+1
                        print(search)
                    if (search >9):
                        searchFormatted=str(search)
                    else:
                        searchFormatted="0"+str(search)
                    print(search)
                    addedString=re.sub('((\d*-)(\d*-)(\d*)T(\d*):)(\d*)(:(\d*))', "\g<1>"+searchFormatted+"\g<7>", addtime)

                    if not endSummary:
                        splitHolder[len(splitHolder)-1]=addedString.lower().replace("finish","unknown")
                        unknownSummary=", ".join(splitHolder)
                        addedString=unknownSummary

                    fx = open(startAddress, "w")
                    print(addedString)
                    fx.write(addedString)

                    
                    if len(startArguments)==3:
                        intent=startArguments[0]
                        summary=startArguments[1]
                        startTime=str(startArguments[2])
                    elif len(startArguments)==4:
                        intent=startArguments[0]
                        summary=startArguments[1]
                        if category=='':
                            category=startArguments[2]
                        startTime=str(startArguments[3])
                    elif len(arguments)==2:
                        intent=arguments[0]
                        startTime=str(startArguments[1])

                    id=calendar_list_entry['id']
                    event={}
                    if endSummary:
                        event['summary']=endSummary
                    else:
                        event['summary']=summary
                    
                    event['start']={
                        'dateTime': startTime,
                        'timeZone': 'America/Los_Angeles',
                    }
                    event['end']={
                        'dateTime': time,
                        'timeZone': 'America/Los_Angeles',
                    }
                    if category:
                        event['description']=category
                    print(str(event)+"AAAA")
                    event = service.events().insert(calendarId=id, body=event).execute()
                elif str(intent).lower()=="start":
                    fx = open(startAddress, "w")
                    print(fread)
                    fx.write(fread)
                
         
        page_token = calendar_list.get('nextPageToken')

        

            



        if not page_token:
            break


    


if __name__ == '__main__':
    main()