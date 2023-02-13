import requests
import json
from googleapiclient import discovery
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'keys.json'

creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)


class Work:
    # def __init__(self):
    def print(self, obj):
        text = json.dumps(obj, sort_keys=True, indent=4)
        print(text)

    def getFromCodefroces(self, gym):
        res = []
        if gym:
            response = requests.get('https://codeforces.com/api/contest.list?gym=true')
            if response.status_code == 200:
                text = response.json()  # { [ {name,difficulty},{  } ] }
                for i in text["result"]:
                    if "difficulty" in i:
                        res.append([i["name"], str(i["difficulty"]), "https://codeforces.com/gym/" + str(i["id"]),
                                    str(i["durationSeconds"] / 3600)])
                    else:
                        res.append([i["name"], 'non', "https://codeforces.com/gym/" + str(i["id"]),
                                    str(i["durationSeconds"] / 3600)])
            else:
                print("try after few second")

        else:
            response = requests.get('https://codeforces.com/api/contest.list?gym=false')
            if response.status_code == 200:
                text = response.json()  # { [ {name,difficulty},{  } ] }
                for i in text["result"]:
                    name = i["name"]
                    diff = "non"
                    posOfCharD = name.find("(Div.")
                    if posOfCharD != -1:
                        posOfCharD += 1
                        diff = ""
                        while name[posOfCharD] != ')':
                            diff += name[posOfCharD]
                            posOfCharD += 1
                    res.append([i["name"], diff, "https://codeforces.com/contest/" + str(i["id"]),
                                str(i["durationSeconds"] / 3600)])
            else:
                print("try after few second")
        return res

    def putInGoogleSheet(self, res):
        spreadSheetId = '1QMmtgNHnW8NsVNQ6-87WELcUBIZ7qn9JIopeu8RmnT8'
        service = discovery.build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        range = 'gyms!A2'
        request = sheet.values().update(spreadsheetId=spreadSheetId, range=range, valueInputOption="USER_ENTERED",
                                        body={"values": res}).execute()
        print(request)


obj = Work()
res = obj.getFromCodefroces(True)
obj.putInGoogleSheet(res)

