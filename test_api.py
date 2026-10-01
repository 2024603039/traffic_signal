import requests
import csv
import os

SERVICE_KEY = "8130daac91ce3acca2028fa8f58cfc43976da1944d6fa210256c89127a0fd873"

URL = "https://apis.data.go.kr/6260000/BusanITSSINTACR/ACRTrf"

all_items = []

page_no = 1

while True:

    params = {
        "serviceKey": SERVICE_KEY,
        "pageNo": page_no,
        "numOfRows": 10,
        "yyyyMMdd": "20260929",
        "hour": "00",
        "resultType": "json"
    }

    response = requests.get(URL, params=params)
    data = response.json()

    content = data.get("content")

    if content is None:
        print("API 오류:")
        print(data)
        break

    items = content.get("items", [])

    if not items:
        break

    all_items.extend(items)

    print(f"{page_no}페이지: {len(items)}건")

    total_count = content["totalCount"]

    if len(all_items) >= total_count:
        break

    page_no += 1


print()
print("전체 데이터:", len(all_items), "건")


# CSV 저장
file_path = "data/traffic.csv"

fieldnames = [
    "clctDt",
    "ixrNm",
    "istlLctn",
    "lrgGoTfvl",
    "lrgLeftTfvl",
    "lrgRghtTfvl",
    "mddlGoTfvl",
    "mddlLeftTfvl",
    "mddlRghtTfvl",
    "smalGoTfvl",
    "smalLeftTfvl",
    "smalRghtTfvl",
    "intlAtmpHeatLngt",
    "walkCnt"
]

with open(file_path, "w", newline="", encoding="utf-8-sig") as f:

    writer = csv.DictWriter(f, fieldnames=fieldnames)

    writer.writeheader()

    for item in all_items:
        writer.writerow(item)


print("traffic.csv 저장 완료!")
print("저장 위치:", os.path.abspath(file_path))