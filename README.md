gDriveBackup
=======

Used Google Drive API to push backup files to Google Drive.


gbackup.py v 0.1
Author: Greg Hetrick
Email: greghetrick@gmail.com

Released under the GPL license.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>

Libraries required for this to work
httplib2
google-api-python-client

with setuptools you can do this
easy_install httplib2
easy_install google-api-python-client

Usage: gbackup.py [options]

Options:

-h,--help               Show this help menu and exit
-i, --init              Initalize the access with Google for this script and the users account.
                        Only needs to be run once, unless access is revoked. Must run as root (working on it)
                        First time this is run copy the printed URL from the command line to a browser and
                        allow access for the script. Copy the code presented back to the commandline

-f,--file filename(s)   This can be a space delimited list: file1.txt file2.txt file3.txt - Or it can be *

