import os
import smtplib
from email.message import EmailMessage
import requests
import json
import schedule
import time


EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

URL = "https://www.dira.moch.gov.il/api/Invoker?method=Projects&param=%3FfirstApplicantIdentityNumber%3D%26secondApplicantIdentityNumber%3D%26ProjectStatus%3D1%26Entitlement%3D1%26PageNumber%3D1%26PageSize%3D12%26"
USER_AGENT ="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
COOKIE="GCLB=CJKotKHlnIL64QE; rbzid=Bikao4TL/P1ndJ92xQb4YHvj2HVRUBFgmaczcYfI7/qTkChFOoXCvRxYv6VtEuodFCVj/TEn2EFs4xon3FQAoMS/tMkMBxLkUWA6oX0cZQIQK2bbjO4HaLEq7caDx8zY4yvXCKrp5el8oTSIydAY7jUX+AWSqXsscNA66CYee37on8iksiFCNVqbBDCDR3LyPCNun5T1EKlSbV09d8lkNldNYGi4+KjXLUywH4ho8B7NnDFIAau8VrgyMulMYzzgrz3/qvTvv1Z/3Q2c88lPKbT8mZPUxSzaDIdUccIOuLM=; rbzsessionid=4736429116cfbab46f1aebdd99cee8cd; ARRAffinity=49c1d2b645019f7ff7d0650a0a905b755701542b8ba4eae43162e09c21bb79a3; ARRAffinitySameSite=49c1d2b645019f7ff7d0650a0a905b755701542b8ba4eae43162e09c21bb79a3"
HEADER= {'user-agent': USER_AGENT, 'Content-type': 'text/html', "cookie":COOKIE}


def get_current_open_lotteries_num():
    with open ("data.txt", "r",encoding="utf8") as f:
        data = f.read()
        read_with_json = json.loads(data)
        return {"number" :read_with_json["OpenLotteriesCount"], "first_project_in_list" : read_with_json["ProjectItems"][0]["LotteryNumber"]}

def main():
    total_appartments = 0
    city_list = set()
    for number in range(1,5):
        URL = "https://www.dira.moch.gov.il/api/Invoker?method=Projects&param=%3FfirstApplicantIdentityNumber%3D%26secondApplicantIdentityNumber%3D%26ProjectStatus%3D1%26Entitlement%3D1%26PageNumber%3D"+str(number)+"%26PageSize%3D12%26"
        response = (requests.get(URL))
        html_doc = response.text
        open_lotteries = json.loads(html_doc)
        for i in open_lotteries["ProjectItems"]:
            if i["IsLotteryHeld"]== False:
                appartment_number = int(i["LotteryApparmentsNum"])
                city_name = i["CityDescription"] 
                city_name = city_name[::-1]
                total_appartments +=appartment_number
                city_list.add(city_name)

        list_of_lotteries = get_current_open_lotteries_num()
        current_open_lotteries = list_of_lotteries["number"]
        if open_lotteries["OpenLotteriesCount"] > 0 and current_open_lotteries != open_lotteries["OpenLotteriesCount"]:
            msg = EmailMessage()
            msg['Subject'] = f'יש {open_lotteries["OpenLotteriesCount"]} הגרלות חדשות '
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = "tzadik1911@gmail.com"
            msg.add_alternative("""\
            <!DOCTYPE html>
            <html lang="en">
            <body>
                <h1 style="color: slategray;">מוזמנים לבדוק את ההגרלות שנפתחו בלינק הבא:  </h1>
                <div>https://www.dira.moch.gov.il/ProjectsList</div>
            </body>
            </html>

            """,subtype="html")

            with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:

                smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)

                smtp.send_message(msg)

                print(f'There are: {open_lotteries["OpenLotteriesCount"]} new lotteri open')
        else:
            print("there are no new open lotteries ")

    with open ("data.txt","w", encoding="utf-8") as f:
        URL = "https://www.dira.moch.gov.il/api/Invoker?method=Projects&param=%3FfirstApplicantIdentityNumber%3D%26secondApplicantIdentityNumber%3D%26ProjectStatus%3D1%26Entitlement%3D1%26PageNumber%3D1%26PageSize%3D12%26"
        response = requests.get(URL)
        html_doc = response.text
        f.write(html_doc)

schedule.every().day.at("10:30").do(main)

if __name__ == "__main__":
    main()

while True:
    schedule.run_pending()
    time.sleep(1)

    


