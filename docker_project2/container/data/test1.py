import json
import requests
import pandas as pd

api_url = 'http://localhost:8090/invocations'

li = [
    "this is a spam",
    "this is a ham"
]

# create_row_data = {'content_type': 'list', 'data':li}
# print(create_row_data)
# r = requests.post(url=api_url, json=create_row_data )
# print(r.status_code, r.reason, r.text)

files={'files': open('SMS_test.csv','rb')}

df = pd.read_csv( "SMS_test.csv" , encoding = "ISO-8859-1")
df = df['Message_body']
data = df
r=requests.post(api_url,data = df)
print(r.status_code, r.reason, r.text)
