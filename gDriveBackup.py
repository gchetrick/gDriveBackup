#!/usr/bin/python
#gbackup.py v 0.1
#Author Greg Hetrick
#greghetrick@gmail.com
#Released under the GPL license.

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>


import httplib2
import pprint
import os
import sys, getopt
import mimetypes
import logging

from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from apiclient import errors
from oauth2client.file import Storage

OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive.file'
REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

USAGE = """
Usage: gbackup.py [options]

Options:

-h,--help               Show this help menu and exit
-i, --init              Initalize the access with Google for this script and the users account.
                        Only needs to be run once, unless access is revoked. Must run as root
                        First time this is run copy the printed URL from the command line to a browser and
                        allow access for the script. Copy the code presented back to the commandline

-f,--file filename(s)   This can be a space delimited list: file1.txt file2.txt file3.txt - Or it can be *
"""

user = os.getlogin()
try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "i f:h ", ["init", "file", "help"])
except getopt.GetoptError as error:
        print (str(error))
        print USAGE
        sys.exit(2)

homedir = os.environ['HOME']
if homedir == "" :
        homedir = "/root"
credfile = homedir + "/.gbackupcred"
if opts == []:
        print USAGE
        sys.exit(2)

for opt,toss in opts:
        if opt in ("-h","--help"):
                print USAGE
                sys.exit()
        elif opt in ("-f", "--file"):
                #look for credential file
                if not os.path.isfile(credfile):
                        print "Need to run qbackup with --init before uploading a file"
                else:
                        storage = Storage(credfile)
                        creds = storage.get()
                        flow = flow_from_clientsecrets('client_secrets.json', OAUTH_SCOPE, REDIRECT_URI)

                        #Create an httplib2.Http object and authorize it with our credentials
                        http = httplib2.Http()
                        http = creds.authorize(http)

                        drive_service = build('drive', 'v2', http=http)
                        # Insert a file
                        for arg in sys.argv[2:]:
                                filename = os.path.basename(arg)
                                format,encoding = mimetypes.guess_type(arg)
                                if format is None:
                                        format = 'application/zip'
                                media_body = MediaFileUpload(arg, mimetype=format, resumable=True)
                                body = {
                                        'title': filename,
                                        'description': 'Backupfile from gbackup.py',
                                        'mimeType': format
                                }
                                #file = drive_service.files().insert(body=body, media_body=media_body).execute()
                                file = drive_service.files().insert(body=body, media_body=media_body)
                                response = None
                                while response is None:
                                        status, response = file.next_chunk()
                                        if status:
                                                print "Uploaded %d%%." % int(status.progress() *100)
                                print filename + " - Upload Complete!"
        elif opt in ("-i", "--init"):
                flow = flow_from_clientsecrets('client_secrets.json', OAUTH_SCOPE, REDIRECT_URI)
                authorize_url = flow.step1_get_authorize_url()
                print 'Go to the following link in your browser: \n' + authorize_url
                code = raw_input('Enter verification code: ').strip()
                credentials = flow.step2_exchange(code)
                storage = Storage(credfile)
                storage.put(credentials)
                print "All finished initializing, run again using -f or --file to upload a file."
                sys.exit()
