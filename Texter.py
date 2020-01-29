import sys
import csv
import time
import datetime
import credentials
import requests


ACT = credentials.master_twilio_account_sid
TOK = credentials.master_twilio_auth_token
curcount = 0
sendcount = 0
FROM = '+441865922021'
URL = 'https://api.twilio.com/2010-04-01/Accounts/{}/Messages.json'.format(ACT)
sentlist = []
readlist = []
with open('PressOneResolutionList.csv', 'r') as csvf:  # read in targets
    redder = csv.reader(csvf, delimiter=',', quotechar='"')
    for row in redder:
        readlist.append(row)
with open('SentList.csv', 'r') as csvf:
    redder = csv.reader(csvf, delimiter=',', quotechar='"')
    for row in redder:  # load up the already-sent cache
        if len(row) > 0:
            if not row[0] in sentlist:
                sendcount += 1
                sentlist.append(row[0])

with open('SentList.csv', 'a') as csvf:
    for row in readlist:
        telenum = row[5]
        try:
            into = int(telenum)
            if telenum in sentlist:
                print("Already sent to :: " + str(telenum))
            else:
                print("Sending to :: "+str(telenum))
                sys.stdout.flush()  # Mason code below, basically.
                body = {
                    'From': FROM,
                    'To': telenum,
                    'Body': (
                        "The \"press 1\" issue is now resolved. The responsible telecoms provider has made needed changes in their network.\nAccordingly, hands free answering (saying \"Yes\" to accept the call) is now turned off. If you would like this turned on for your account, please reply \"yes\" to this text.\nMany thanks,\nConsultant Connect"
                    ),
                }
                started = datetime.datetime.now()
                res = requests.post(URL, data=body, auth=(ACT, TOK))
                row.append(res.status_code)
                print(" got {}".format(res.status_code))  # Mason code ends
                # print (res.content)
                sentlist.append(telenum)
                sendcount += 1
                curcount += 1
                csvf.write(str(telenum)+"\n")
            time.sleep(0.25)  # IDK why but it works so keep it
        except Exception as e:
            print(e)
            print("not a number :: "+str(telenum))

print("Messaging completed")
print("Total texts sent :: "+str(sendcount))
print("Texts sent this run :: "+str(curcount))
