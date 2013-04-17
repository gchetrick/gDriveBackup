#!/usr/bin/python

import httplib2
import pprint
import os
import sys, getopt

from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow

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
			file = open(credfile, "r")
			contents = file.read();
			file.close()
			print "upload file " + arg 
			#flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE, REDIRECT_URI)
			#creds = flow.step2_exchange(contents)
			# Create an httplib2.Http object and authorize it with our credentials
			http = httplib2.Http()
			http = creds.authorize(http)
			
			drive_service = build('drive', 'v2', http=http)
			# Insert a file
			media_body = MediaFileUpload(arg, mimetype='application/zip', resumable=True)
			body = {
 				'title': backupfile,
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
		file = open(credfile, "w")
		file.write(code);		
		file.close()
		sys.exit()
	else: 
		print "Usage: -i,--init; -f,--file <filename>; -h,--help This menu"
