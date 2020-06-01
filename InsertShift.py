import requests
import json
import datetime
import calendar
import sys

shift = "シフト入力"
shiftList = shift.split("\t")
YEAR = '2020'
#入れたい月を選択
month = '06'
title = ''
start_at = ''
end_at = ''
day = 1

#配列の数が付きの分あるかの判定
dayMax = calendar.monthrange(int(YEAR), int(month))[1]
if len(shiftList) != dayMax:
    print("入力シフトと今月の日数が一致しません。")
    sys.exit()




def sendAPI(start_at,end_at,title,label):
    # ヘッダーの設定
    ACCESS_TOKEN = 'アクセストークン'
    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/vnd.timetree.v1+json',
    'Authorization': 'Bearer ' + ACCESS_TOKEN
    }

    updateCalenderURL = 'https://timetreeapis.com/calendars/NDqW_IFTrZn7/events'
    data = {
        "data": {
          "attributes": {
            "category": "schedule",
            "title": title,
            "all_day": False,
            "start_at": start_at,
            "start_timezone": "UTC",
            "end_at": end_at,
            "end_timezone": "UTC",
            "description": "",
            "location":"tokyo"

          },
          "relationships": {
            "label": {
              "data": {
                "id": label,
                "type": "label"
              }
            }
          }
      }
    }
    r = requests.post(updateCalenderURL, headers=headers,  verify=False, json=data)
    data = r.json()
    print(r.status_code)
    print(json.dumps(data, indent=4, ensure_ascii=False))

for i in range(len(shiftList)):
    print(shiftList[i])
    if shiftList[i] == 'b' or shiftList[i] == 'B':
        start_at = '2020-{month}-{day}T11:00:00.000Z'.format(month=month,day=str(day) if day >= 10 else '0'+str(day))
        end_at = '2020-{month}-{day}T23:00:00.000Z'.format(month=month,day=str(day) if day >= 10 else '0'+str(day))
        if shiftList[i] == 'B':
            title = '夜勤（シフトリーダー）'
        elif shiftList[i] == 'b':
            title = '夜勤'
        sendAPI(start_at,end_at,title,"1")

    elif  shiftList[i] == 'a' or shiftList[i] == 'A':
        if day == 1:
            start_at = '2020-{month}-{day}T23:00:00.000Z'.format(month=month,day=calendar.monthrange(int(YEAR), int(month))[1])
        else:
            start_at = '2020-{month}-{day}T23:00:00.000Z'.format(month=month,day=str(day-1) if (day-1) >= 10 else '0'+str(day-1))
        end_at = '2020-{month}-{day}T11:00:00.000Z'.format(month=month,day=str(day) if day >= 10 else '0'+str(day))
        if shiftList[i] == 'A':
            title = '日勤（シフトリーダー）'
        elif shiftList[i] == 'a':
            title = '日勤'
        sendAPI(start_at,end_at,title,"2")

    elif  shiftList[i] == 'C' or shiftList[i] == 'c':
        if day == 1:
            start_at = '2020-{month}-{day}T23:00:00.000Z'.format(month=month,day=calendar.monthrange(int(YEAR), int(month))[1])
        else:
            start_at = '2020-{month}-{day}T00:00:00.000Z'.format(month=month,day=str(day) if (day)>= 10 else '0'+str(day))
        end_at = '2020-{month}-{day}T09:00:00.000Z'.format(month=month,day=str(day) if day >= 10 else '0'+str(day))
        title = '研修'
        sendAPI(start_at,end_at,title,"3")

    else:
        pass
    

    day += 1
    
    
