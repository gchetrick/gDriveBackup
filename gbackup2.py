#!/usr/bin/python

import httplib2
import pprint
import os
import sys, getopt
import logging

from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import FlowExchangeError
from apiclient import errors
from oauth2client.file import Storage

CLIENT_ID = '303911097105.apps.googleusercontent.com'
CLIENT_SECRET = 'GWLv1F-cFwDn4PxOQnY9v1mL'
OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

user = os.getlogin()
try:
        opts, args = getopt.getopt(sys.argv[1:], "i f:h ", ["init", "file", "help"])
except getopt.GetoptError as error:
        print (str(error))
        print("Usage: -i,--init; -f,--file <filename>; -h,--help This menu" % sys.argv[0])
        sys.exit(2)

homedir = os.environ['HOME']
if homedir == "" :
        homedir = "/root"
credfile = homedir + "/.gbackupcred"
for opt, arg in opts:
        if opt in ("-h","--help"):
                print "Usage: -i,--init; -f,--file <filename>; -h,--help This menu"
                sys.exit()
        elif opt in ("-f", "--file"):
                #look for credential file
                if not os.path.isfile(credfile):
                        print "Need to run qbackup with --init before uploading a file"
                else:
                        storage = Storage(credfile)
                        creds = storage.get()
                        print "upload file " + arg
                        flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE, REDIRECT_URI)

                        #Create an httplib2.Http object and authorize it with our credentials
                        http = httplib2.Http()
                        http = creds.authorize(http)

                        drive_service = build('drive', 'v2', http=http)
                        # Insert a file
                        media_body = MediaFileUpload(arg, mimetype='application/zip', resumable=True)
                        body = {
                                'title': arg,
                                'description': 'Backupfile from gbackup.py',
                                'mimeType': 'application/zip'
                        }
                        file = drive_service.files().insert(body=body, media_body=media_body).execute()
                        sys.exit()
        elif opt in ("-i", "--init"):
                flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE, REDIRECT_URI)
                authorize_url = flow.step1_get_authorize_url()
                print 'Go to the following link in your browser: \n' + authorize_url
                code = raw_input('Enter verification code: ').strip()
                credentials = flow.step2_exchange(code)
                #http = httplib2.Http()
                #http = credentials.authorize(http)
                storage = Storage(credfile)
                storage.put(credentials)
                #print "CREDS" + credentials
                #user_info_service = build('oauth2', 'v2', http=http)
                        #http=code.authorize(httplib2.Http()))
                #user_info = None
                #try:
                #       user_info = user_info_service.userinfo().get().execute()
                #except errors.HttpError, e:
                #       logging.error('An error occurred: %s', e)
                #if user_info and user_info.get('id'):
                #       ident = user_info.get('id')
                #       print "IDENTITY" + ident
                #else:
                #       #raise NoUserIdException()
                #       print "NO USER ID"
                print "All finished initializing, run again using -f or --file to upload a file."
                sys.exit()
        else:
                print "Usage: -i,--init; -f,--file <filename>; -h,--help This menu"
