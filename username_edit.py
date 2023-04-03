import json
from json import JSONDecodeError

import snipeitpyapi as snipeit


server = "http://10.10.15.145"
server = "http://192.168.5.120"
token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiZDYzNjMwZDlhMzgyMGUzMGVhMDEwY2Y5ZmMwYjgwNjFmOGRiOTVhNTA0NTkwMzIyN2IyMDU5YjBlYjhjNDdmNjY3ZGNmZGRkY2FjNTIzZjYiLCJpYXQiOjE2NDEyOTk4MDIsIm5iZiI6MTY0MTI5OTgwMiwiZXhwIjoyOTAzNjAzODAyLCJzdWIiOiIxNTUiLCJzY29wZXMiOltdfQ.lHpM4lB4oQiu2PdSoLNbiIIHff8VGK-hORYNw70b-kxv7d4qWcsIStxjhG_s0VIVZQvxJAr05KuzY0CJSwdYHJIk3w8Eo_aQm-oq1xP-0XLpeNBPzzNEkQZy2lgqRdBAlV__eJrkYEEstAJoBo3Yp5uccFRelByJMUQozjF8EKT6NB2bmxGszMsJyh7q5TnnoLkKZShlE2D9XVLndBxsFS5PbcNtHNf5U0WGVvxsBXBMQjCi2j-aX_NWx5B5r721he3rjylulIB0FpvPhoDg22GHlgsoB2q4sLwETpeUB-8wmKQwGdG5BaOeIVJXCHDviZDCn3SY4RSg3wi0knfNq9QZZZnDUM8GCyiZeLtuCCzA64EbVMLG9pkdRX4s6uulvnSeFOYIgqbexsWumz87fJGsSfjCzM88Ig6X96J0KerIY2KY-6rQ4cJqiP1-WmgHxzoiM1JVdu7oE_DGZH6CvvkmyNIJfpXBQ5yT0UlnGkqhCINuz4SX_M8ediCXI4-beB0DkwQclpLNMn0IMxLBaVwkoC3T1gCuslNymR5dGhTY1BNzTzgh7ZzJSz8_yVSOSgh-dYL45qMdM4C2N5YDwgAuS3ndgySjVBR2WB26a92GGTsgPdFDWNGPtJHWQw8MBECSAGEKw-iqhf_M-fgqgx7rqQEl2PnySuEXYed8BIQ"

Users = snipeit.Users()


IDs = ["96", "97", "98", "100", "101", "102", "72", "73", "75", "76", "77", "78", "80", "82", "85", "86", "58", "59", "61", "64", "65", "66", "67", "69", "71", "42", "43", "44", "45", "48", "49", "51", "52", "53", "54", "55", "57", "27", "28", "29", "31", "33", "35", "36", "37", "39", "41", "12", "13", "14", "15", "16", "20", "22", "24", "25", "26", "7", "9", "10", "6", "4"]

for id in IDs:
    print(id)
    try:
        f = Users.getDetailsByID(server=server, token=token, userID=id)
        json_object = json.loads(f)
        email = f"{json_object['first_name']}.{json_object['last_name']}@sofascore.com"
        email = email.lower()
        print(email)
        #payload = f'{"email":"{email}"}'
        #r = Users.updateUser(server=server, token=token, UserID=id, payload=payload)
        #print(r)
    except JSONDecodeError:
        print("error")





