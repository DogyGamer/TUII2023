import requests


# curr = requests.get(endpoint+"api/states/switch.lamp", headers=headers)

# print(curr.json()["state"])

def toggle_light():
    endpoint = "https://dogyhome.duckdns.org:8123/"
    headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI0MTVjNDMzNjA1YzE0ZDdiYTM0NGI0YTQwMGViYTEwNSIsImlhdCI6MTY4MDM0MzIzMywiZXhwIjoxOTk1NzAzMjMzfQ.RNsTOrm7Jb-42p2W42EYVGuxqQ4ENCp6NUGHsS24cZE",
            "content-type": "application/json",
            }
    data = {"area_id": "spalnia_sasha"}
    requests.post(endpoint+"api/services/light/toggle", headers=headers, json=data)

toggle_light()