import requests
import json


class hoba:
    # def __init__(self):
    def print(self, obj):
        text = json.dumps(obj, sort_keys=True, indent=4)
        print(text)

    def get(self, gym):
        if gym:
            response = requests.get('https://codeforces.com/api/contest.list?gym=true')
        else:
            response = requests.get('https://codeforces.com/api/contest.list?gym=false')
        if response.status_code == 200:
            text = response.json()  # { [ {name,difficulty},{  } ] }
            for i in text["result"]:
                if "difficulty" in i:
                    print(i["name"], "https://codeforces.com/gym/" + str(i["id"]), i["difficulty"])
                else:
                    print(i["name"], "https://codeforces.com/gym/" + str(i["id"]))
        else:
            print("try after few second")


hoba1 = hoba()
hoba1.get(1)
