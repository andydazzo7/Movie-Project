from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os, glob
from datetime import date
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

today = date.today()
dateToday = today.strftime("%B %d, %Y")

for f in glob.glob("ProjectAutomationTest{}*.csv".format(dateToday)):
            print f
            with open(f,"r") as f1:
                fn = os.path.basename(f1.name)
                file_drive = drive.CreateFile({'title': fn, 'parents':[{'id':'1xRUZ4SCtusiTYhlNt9s8u9t_HIYD8GUH'}]})  
                file_drive.SetContentFile(fn) 
                file_drive.Upload()
                print "The file: " + fn + " has been uploaded"