import os
import gspread
import pandas as pd

from oauth2client.service_account import ServiceAccountCredentials

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

SCOPES = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive',
         'https://www.googleapis.com/auth/spreadsheets']

CLIENT_SECRET_FILE = 'Hands_onclient_secret.json'

# ----------------------------------------------------------------------------------------------------------------------#
#    Establish Connection with Google API's via client_secret.json file resides in src directory
# ----------------------------------------------------------------------------------------------------------------------#
def get_google_api_connection():
   credential_path = os.path.join(CURRENT_DIR,'config',CLIENT_SECRET_FILE)
   credentials = ServiceAccountCredentials.from_json_keyfile_name(credential_path, SCOPES)
   google_connection = gspread.authorize(credentials)
   SHEET_ID = '1qTRyOfzg3gPht1FA4nvJCAMKMsyLnV90cAil0rzMFRE'
   SHEET_NAME = 'Employee_details'
   googlesheetdata = google_connection.open_by_key(SHEET_ID).worksheet(SHEET_NAME).get_all_values()
   #print(googlesheetdata)
   data_frame = pd.DataFrame(googlesheetdata)
   #print(data_frame)
   head=str(googlesheetdata.pop(0))[1:-1].replace("\'","")
   columns =list(data_frame)
   cols = "','".join([str(i) for i in (0, columns)])
   index = data_frame.index
   nof = int(len(index))
   #print(nof)
   cnt = 0
   for i in columns:
      cnt = cnt + 1
   cnt = cnt - 1
   #print(cnt)
   #print(head)
   file = open("SQL.txt", "w")
   for row in range(0, nof - 1):
      tail = str(googlesheetdata[row])[1:-1].replace("$","")
      sql = "INSERT INTO emp_table(" + head+ ") VALUES ( " + tail + " );"
      file.writelines(sql+ "\n")
      #print(sql)
   file.close()

get_google_api_connection()

