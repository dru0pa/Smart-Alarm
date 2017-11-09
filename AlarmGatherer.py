from __future__ import print_function
import pytz
import dateutil.parser
import httplib2
from oauth2client import tools
from oauth2client import client
import datetime
import logging
from googleapiclient.discovery import build
from oauth2client.file import Storage
import Settings
import os

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

log = logging.getLogger('root')

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Smart-Alarm'
class AlarmGatherer:

    def __init__(self):
        self.settings = Settings.Settings()

#    def __init__(self):
        #home_dir = os.path.expanduser('~')
        #credential_dir = os.path.join(home_dir, 'calendar.dat')
        #if not os.path.exists(credential_dir):
        #    os.makedirs(credential_dir)
        #credential_path = os.path.join(credential_dir, 'client_secret.json')

        SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
        CLIENT_SECRET_FILE = 'client_secret.json'
        APPLICATION_NAME = 'Smart-Alarm'

        self.FLOW = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)

        self.storage = Storage('calendar.dat')
        self.credentials = self.storage.get()

        if not self.checkCredentials():
            log.error("GCal credentials have expired")
            log.warn("Remove calendar.dat and run 'python AlarmGatherer.py' to fix")
            return

        http = httplib2.Http()
        http = self.credentials.authorize(http)

        self.service = build('calendar', 'v3', http=http)

    def checkCredentials(self):
        return not (self.credentials is None or self.credentials.invalid == True)

    def generateAuth(self):
        self.credentials = tools.run_flow(self.FLOW, self.storage)

    def getNextEvent(self, today=False):
        log.debug("Fetching details of next event")
        if not self.checkCredentials():
            log.error("GCal credentials have expired")
            log.warn("Remove calendar.dat and run 'python AlarmGatherer.py' to fix")
            raise Exception("GCal credentials not authorized")

        #time = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC
        time = datetime.datetime.now()
        if not today:
            # We want to find events tomorrow, rather than another one today
            log.debug("Skipping events from today")
            # time += datetime.timedelta(days=1)  # Move to tomorrow
            time = time.replace(hour=10, minute=0, second=0, microsecond=0)  # Reset to 10am the next day
            # 10am is late enough that a night shift from today won't be caught, but a morning shift
            #  from tomorrow will be caught

        result = self.service.events().list(
            calendarId='primary',
            timeMin="%sZ" % (time.isoformat()),
            maxResults=1,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = result.get('items', [])
        return events[0]

    def getNextEventTime(self, includeToday=False):
        log.debug("Fetching next event time (including today=%s)" % (includeToday))
        nextEvent = self.getNextEvent(today=includeToday)
        start = dateutil.parser.parse(nextEvent['start']['dateTime'])
        # start = dateutil.parser.parse(nextEvent['start']['dateTime'], ignoretz=True)
        # start = start.replace(tzinfo=pytz.timezone('Africa/Johannesburg'))

        return start

    def getNextEventLocation(self, includeToday=False):
        log.debug("Fetching next event location (including today=%s)" % (includeToday))
        nextEvent = self.getNextEvent(today=includeToday)
        if (nextEvent['location']):
            return nextEvent['location']
        return None

    def getDefaultAlarmTime(self):
        defaultTime = ('0700')
        #defaultTime = self.settings.getInt('default_wake')
        # defaultTime = self.settings.get('default_wake')
        # defaultTime = self.settings.getint('default_wake')
        defaultHour = int(defaultTime[:2])
        defaultMin = int(defaultTime[2:])

        alarm = datetime.datetime.now(pytz.timezone('Africa/Johannesburg'))
        alarm += datetime.timedelta(days=1)  # Move to tomorrow
        alarm = alarm.replace(hour=defaultHour, minute=defaultMin, second=0, microsecond=0)

        return alarm

if __name__ == '__main__':
    print("Running credential check")
    a = AlarmGatherer()
    try:
        if not a.checkCredentials():
            raise Exception("Credential check failed")
    except:
        print("Credentials not correct, please generate new code")
        a.generateAuth()
        a = AlarmGatherer()

    print(a.getNextEventTime())
    print(a.getNextEventLocation())

