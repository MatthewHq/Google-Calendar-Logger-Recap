from __future__ import print_function
import json
import datetime
import re
import pickle
import os.path
import sys
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime


startAddress = 'Tracker'+os.sep+'start.txt'
updateAddress = 'Tracker'+os.sep+'trackerUpdate.txt'
dataFilePath = 'Tracker'+os.sep+'cache.json'


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def registerNextCacheTime(nextTime):
    # Opening JSON file
    with open(dataFilePath, 'r') as openfile:
        # Reading from json file
        json_object = json.load(openfile)

    with open(dataFilePath, "w") as outfile:
        json_object['cachedTime'] = nextTime
        json_object = json.dumps(json_object, indent=4)
        outfile.write(json_object)


def getNextCacheTime(currentCacheTime):
    search = re.sub(
        '((\d*-)(\d*-)(\d*)T(\d*):)(\d*)(:(\d*))', "\g<6>", currentCacheTime)
    # splitHolder = search.split(', ')
    # search = splitHolder
    # search = search[len(search)-1]
    search = int(search)
    # print(search)
    if search != 59:
        search = search+1
        # print(search)
    if (search > 9):
        searchFormatted = str(search)
    else:
        searchFormatted = "0"+str(search)
    # print(search)
    addedString = re.sub(
        '((\d*-)(\d*-)(\d*)T(\d*):)(\d*)(:(\d*))', "\g<1>"+searchFormatted+"\g<7>", currentCacheTime)
    return addedString


def parseArgs(args):
    # arg example: start-XXXX end-XXXXX title-XXXX descripion-XXXXX
    inputs = {}
    # unparsedInputs = inputStr.split(' ')
    for x in args:
        y = x.split('=-')
        inputs[y[0]] = y[1]
    return inputs


def getNowTime():
    # get current datetime
    now = datetime.now()

    # Get current ISO 8601 datetime in string format
    iso_date = now.isoformat()
    iso_date = iso_date.split('.')[0]
    print("returning", iso_date)
    return iso_date


def checkDataFile():
    if not os.path.isfile('Tracker'+os.sep+'cache.json'):

        now = getNowTime()

        # Data to be written
        dictionary = {
            "cachedTime": now
        }

        # Serializing json
        json_object = json.dumps(dictionary, indent=4)

        # Writing to sample.json
        with open(dataFilePath, "w") as outfile:
            outfile.write(json_object)


def determineCache(args):
    startTime = args.get('startTime')
    endTime = args.get('endTime')
    category = args.get('category')
    summary = args.get('summary')

    if not (startTime and endTime):
        if endTime:
            #cachedTime @ endTime
            registerNextCacheTime(getNextCacheTime(endTime))
        else:
            #cachedTime @ Now
            registerNextCacheTime(getNextCacheTime(getNowTime()))


def timeLengthConstructor(startTime, endTime):
    sTimeDT = datetime.fromisoformat(startTime)
    eTimeDT = datetime.fromisoformat(endTime)
    delt = eTimeDT-sTimeDT
    seconds = delt.total_seconds()

    deltaStr = str(delt)

    if seconds < 3600:
        deltaStr = deltaStr[2:4]+'m'
    elif seconds < 86400:
        deltaStr = deltaStr[0:4]+'m'

    return deltaStr


def eventContructor(args):
    startTime = args.get('startTime')
    endTime = args.get('endTime')
    category = args.get('category')
    summary = args.get('summary')

    event = {}

    if not startTime:

        # Opening JSON file
        with open(dataFilePath, 'r') as openfile:
            # Reading from json file
            json_object = json.load(openfile)
            startTime = json_object['cachedTime']

    if not endTime:
        # Opening JSON file
        endTime = getNowTime()

    deltaStr = timeLengthConstructor(startTime, endTime)

    event['summary'] = "{} [{}]".format(summary, deltaStr)

    event['start'] = {
        'dateTime': startTime,
        'timeZone': 'America/Los_Angeles',
    }
    event['end'] = {
        'dateTime': endTime,
        'timeZone': 'America/Los_Angeles',
    }
    if category:
        event['description'] = category
    return event


def main():
    checkDataFile()
    print(sys.argv)
    args = parseArgs(sys.argv[1:len(sys.argv)])

    event = eventContructor(args)
    determineCache(args)
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """

    print(event)

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
            # now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

            # print(calendar_list_entry['summary'] == "Z LOG")
            if calendar_list_entry['summary'] == "Z LOG":

                id = calendar_list_entry['id']

                # used to be event=.... ??
                service.events().insert(calendarId=id, body=event).execute()

        page_token = calendar_list.get('nextPageToken')

        if not page_token:
            break


if __name__ == '__main__':
    main()
    # pass

# print(parseArgs("start-XXXX end-XXXXX title-XXXX descripion-XXXXX"))
# print(getNextCacheTime("2022-12-08T12:39:21"))
# print(timeLengthConstructor("2022-12-08T12:39:21", "2022-12-08T13:50:21"))
