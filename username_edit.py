import json
import time
from json import JSONDecodeError

import snipeitpyapi as snipeit


server = "http://10.10.15.145"
server = "http://192.168.5.120"
server = "http://10.10.1.53"
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiZDYzNjMwZDlhMzgyMGUzMGVhMDEwY2Y5ZmMwYjgwNjFmOGRiOTVhNTA0NTkwMzIyN2IyMDU5YjBlYjhjNDdmNjY3ZGNmZGRkY2FjNTIzZjYiLCJpYXQiOjE2NDEyOTk4MDIsIm5iZiI6MTY0MTI5OTgwMiwiZXhwIjoyOTAzNjAzODAyLCJzdWIiOiIxNTUiLCJzY29wZXMiOltdfQ.lHpM4lB4oQiu2PdSoLNbiIIHff8VGK-hORYNw70b-kxv7d4qWcsIStxjhG_s0VIVZQvxJAr05KuzY0CJSwdYHJIk3w8Eo_aQm-oq1xP-0XLpeNBPzzNEkQZy2lgqRdBAlV__eJrkYEEstAJoBo3Yp5uccFRelByJMUQozjF8EKT6NB2bmxGszMsJyh7q5TnnoLkKZShlE2D9XVLndBxsFS5PbcNtHNf5U0WGVvxsBXBMQjCi2j-aX_NWx5B5r721he3rjylulIB0FpvPhoDg22GHlgsoB2q4sLwETpeUB-8wmKQwGdG5BaOeIVJXCHDviZDCn3SY4RSg3wi0knfNq9QZZZnDUM8GCyiZeLtuCCzA64EbVMLG9pkdRX4s6uulvnSeFOYIgqbexsWumz87fJGsSfjCzM88Ig6X96J0KerIY2KY-6rQ4cJqiP1-WmgHxzoiM1JVdu7oE_DGZH6CvvkmyNIJfpXBQ5yT0UlnGkqhCINuz4SX_M8ediCXI4-beB0DkwQclpLNMn0IMxLBaVwkoC3T1gCuslNymR5dGhTY1BNzTzgh7ZzJSz8_yVSOSgh-dYL45qMdM4C2N5YDwgAuS3ndgySjVBR2WB26a92GGTsgPdFDWNGPtJHWQw8MBECSAGEKw-iqhf_M-fgqgx7rqQEl2PnySuEXYed8BIQ"

Users = snipeit.Users()


def replace_special_characters(input_string):
    replacements = {
        'č': 'c',
        'ć': 'c',
        'ž': 'z',
        'đ': 'd',
        'š': 's'
    }

    # Remove spaces from the input string
    input_string = input_string.replace(' ', '')

    output_string = ""
    for char in input_string:
        if char in replacements:
            output_string += replacements[char]
        else:
            output_string += char

    return output_string


all_user_ids = []


def get_all_ids():
    all_user_data = json.loads(Users.get(server=server, token=token, limit=500))
    for user in all_user_data["rows"]:
        all_user_ids.append(user["id"])
    all_user_ids.sort(key=lambda x: int(x))


get_all_ids()

for user_id in all_user_ids:
    print(user_id)
    time.sleep(0.5)
    try:
        f = Users.getDetailsByID(server=server, token=token, userID=user_id)
        json_object = json.loads(f)
        email = f"{json_object['first_name']}.{json_object['last_name']}@sofascore.com"
        email = email.lower()
        email = replace_special_characters(email)
        print(email)
        #payload = f'{"email":"{email}"}'
        #r = Users.updateUser(server=server, token=token, UserID=id, payload=payload)
        #print(r)
    except JSONDecodeError:
        print(JSONDecodeError)
        print("error")

