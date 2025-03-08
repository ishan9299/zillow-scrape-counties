import requests
import json
import pandas as pd

def main(url, headers, payload):
    try:
        with open("region_data.json") as file:
            region_data = json.load(file)

        result = []
        for state_code in list(region_data.keys()):
            counties = region_data[f"{state_code}"]["counties"]
            if state_code == "DE":
                for county in counties:
                    mapBounds = region_data[f"{state_code}"]["mapBounds"]
                    payload["searchQueryState"]["mapBounds"] = mapBounds
                    payload["searchQueryState"]["regionSelection"][0]["regionId"] = county["regionId"]

                    payload["searchQueryState"]["filterState"]["isPendingListingsSelected"]["value"] = True
                    payload_str = json.dumps(payload)
                    response = requests.request("PUT", url, headers=headers, data=payload_str).json()
                    pnd_true = response["categoryTotals"]["cat1"]["totalResultCount"]

                    payload["searchQueryState"]["filterState"]["isPendingListingsSelected"]["value"] = False
                    payload_str = json.dumps(payload)
                    response = requests.request("PUT", url, headers=headers, data=payload_str).json()
                    pnd_false = response["categoryTotals"]["cat1"]["totalResultCount"]

                    result_dic = {"name": county["id"], "pnd_true": pnd_true, "pnd_false": pnd_false}
                    result.append(result_dic)

        print(result)
        df = pd.DataFrame(result)
        df.to_csv("result.csv", index=False)

    except Exception as e:
        print(f"An error has occured: {e}")


if __name__ == "__main__":
    url = "https://www.zillow.com/async-create-search-page-state"

    payload = {
        "searchQueryState": {
            "isMapVisible": True,
            "mapBounds": {
                "north": 37.81175785567474,
                "south": 30.455562904515066,
                "east": -102.48297767968751,
                "west": -109.56915932031251
            },
            "filterState": {
                "sortSelection": {
                    "value": "globalrelevanceex"
                },
                "isTownhouse": {
                    "value": False
                },
                "isMultiFamily": {
                    "value": False
                },
                "isCondo": {
                    "value": False
                },
                "isLotLand": {
                    "value": False
                },
                "isApartment": {
                    "value": False
                },
                "isManufactured": {
                    "value": False
                },
                "isApartmentOrCondo": {
                    "value": False
                },
                "isPendingListingsSelected": {
                    "value": True
                },
                "built": {
                    "max": 2021
                }
            },
            "isListVisible": True,
            "mapZoom": 7,
            "regionSelection": [
                {
                    "regionId": 41,
                    "regionType": 2
                }
            ],
            "usersSearchTerm": "NM",
            "schoolId": None,
            "pagination": {}
        },
        "wants": {
            "cat1": [
                "listResults",
                "mapResults"
            ],
            "cat2": [
                "total"
            ]
        },
        "requestId": 9,
        "isDebugRequest": False
    }

    headers = {
      'accept': '*/*',
      'accept-language': 'en-US,en;q=0.9',
      'cache-control': 'no-cache',
      'content-type': 'application/json',
      'dnt': '1',
      'origin': 'https://www.zillow.com',
      'pragma': 'no-cache',
      'priority': 'u=1, i',
      'referer': 'https://www.zillow.com/al/?searchQueryState=%7B%22isMapVisible%22%3Afalse%2C%22mapBounds%22%3A%7B%22north%22%3A35.008028%2C%22south%22%3A30.144425%2C%22east%22%3A-84.888246%2C%22west%22%3A-88.473227%7D%2C%22usersSearchTerm%22%3A%22AL%22%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%7D%2C%22isListVisible%22%3Afalse%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A4%2C%22regionType%22%3A2%7D%5D%7D&category=SEMANTIC',
      'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-origin',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
      'Cookie': 'zguid=24|%24237050a9-f41e-49af-b678-8e66f99a8a48; zgsession=1|e7ec0aed-567d-4bcc-8968-079b41efefbe; _ga=GA1.2.150401820.1741182733; _gid=GA1.2.268627220.1741182733; zjs_anonymous_id=%22237050a9-f41e-49af-b678-8e66f99a8a48%22; zjs_user_id=null; zg_anonymous_id=%22f2528a79-e0e7-4718-8978-6b9be02ed32c%22; pxcts=0a9d75bf-f9c9-11ef-a0e1-7901a226971c; _pxvid=0a9d66df-f9c9-11ef-a0e1-6e3d3c08a2c1; JSESSIONID=30DFEEE11BFC2533C51C4E9FE521B1EB; _gcl_au=1.1.301305770.1741182736; _rdt_uuid=1741182736059.4cd18c39-5b9a-470f-bc9d-0cad0c50a50a; _fbp=fb.1.1741182736439.693896856214106791; tfpsi=9cf454ff-1c7a-48f8-aea8-9ebe696fcffa; _scid=C1PAZvCtpFiHjAWw29Tfof1ojONjfw9f; _scid_r=C1PAZvCtpFiHjAWw29Tfof1ojONjfw9f; _pin_unauth=dWlkPVkyUXdZakl3TVRjdE9URXdOeTAwWm1VM0xXRmxOVGd0TnpGbU9ERTRPRFpqTXpVdw; _ScCbts=%5B%5D; _clck=nij7mp%7C2%7Cfty%7C0%7C1890; DoubleClickSession=true; _sctr=1%7C1741113000000; _dd_s=rum=0&expire=1741183685056; _px3=f4256640de5a85baab4ec1fac246e59add1333004ee036efe7e1dc1d84aea58a:zMOdTJ0YlNGbEpg6KGOwCVDm4kndjbdmxiWJ9r9ibOtDLmosXfeteogF9rx808yjT1WqA+hO3bxp18/drtIp4w==:1000:l7RNBgMr9BwI+8BveO1qX6xK8h8FkIWpxUDmaXDk1JgTRCvY5Bp4veOXEeqM564h2tLnvSRQZcg2lNzfnWmB4k6HwjJ/1KXH3UcPR2Wa1c/c3gl49mm8JZzKzVhBLC+IKHvJtDSqQt5W76CnerB0KVxfNGn99LOJwdxn+vefEncARYlErq/u+LDg0J0u6o3+lWnz7IbxqAfLncE4bjKM0hoMICuwztNOBREoh6qJjhw=; web-platform-data=%7B%22wp-dd-rum-session%22%3A%7B%22doNotTrack%22%3Atrue%7D%7D; AWSALB=R7RmRspHnwTY48W27YcNvbaH+Ts1VsxK26XSZ6zensdIplPoDlDiOOhio2FZjjkOSZP3wfWEw+wHOKWxwj6iQjgQ3+L5XyM5REIhlprmDmLoeMP5wsduT2+qLnYD; AWSALBCORS=R7RmRspHnwTY48W27YcNvbaH+Ts1VsxK26XSZ6zensdIplPoDlDiOOhio2FZjjkOSZP3wfWEw+wHOKWxwj6iQjgQ3+L5XyM5REIhlprmDmLoeMP5wsduT2+qLnYD; _uetsid=0c764740f9c911ef9717738c798decb8; _uetvid=0c767aa0f9c911efb48bf133a3975c92; search=6|1743774817208%7Crect%3D50.827053%2C-63.296718%2C24.617482%2C-125.523281%26rid%3D4%26disp%3Dmap%26mdm%3Dauto%26p%3D1%26listPriceActive%3D1%26fs%3D1%26fr%3D0%26mmm%3D0%26rs%3D0%26singlestory%3D0%26housing-connector%3D0%26parking-spots%3Dnull-%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%26showcase%3D0%26featuredMultiFamilyBuilding%3D0%26onlyRentalStudentHousingType%3D0%26onlyRentalIncomeRestrictedHousingType%3D0%26onlyRentalMilitaryHousingType%3D0%26onlyRentalDisabledHousingType%3D0%26onlyRentalSeniorHousingType%3D0%26commuteMode%3Ddriving%26commuteTimeOfDay%3Dnow%09%094%09%7B%22isList%22%3Atrue%2C%22isMap%22%3Afalse%7D%09%09%09%09%09; _clsk=1oofmvp%7C1741182817878%7C4%7C0%7Cx.clarity.ms%2Fcollect; search=6|1744024627453%7Crect%3D35.008028%2C-84.888246%2C30.144425%2C-88.473227%26rid%3D4%26disp%3Dmap%26mdm%3Dauto%26p%3D1%26listPriceActive%3D1%26fs%3D1%26fr%3D0%26mmm%3D0%26rs%3D0%26singlestory%3D0%26housing-connector%3D0%26parking-spots%3Dnull-%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%26showcase%3D0%26featuredMultiFamilyBuilding%3D0%26onlyRentalStudentHousingType%3D0%26onlyRentalIncomeRestrictedHousingType%3D0%26onlyRentalMilitaryHousingType%3D0%26onlyRentalDisabledHousingType%3D0%26onlyRentalSeniorHousingType%3D0%26commuteMode%3Ddriving%26commuteTimeOfDay%3Dnow%09%094%09%7B%22isList%22%3Atrue%2C%22isMap%22%3Afalse%7D%09%09%09%09%09; zgsession=1|0a4f280e-e2e5-42bb-9749-429d1391a003; zguid=24|%24ae7cb6be-0627-4818-ae6a-6d6d0b66be2a; AWSALB=z43wgwSdQDXa69YIrRwy5r8bFKwz1RvN5DBAyz2PPwt1DOZIV0eVgJP/EecHgASPCal/HXu1LiijxlNjk1u9qg6Ha4/9wtmJG2uRq+jktCUGdLmBaCMnuOcQBLiU; AWSALBCORS=z43wgwSdQDXa69YIrRwy5r8bFKwz1RvN5DBAyz2PPwt1DOZIV0eVgJP/EecHgASPCal/HXu1LiijxlNjk1u9qg6Ha4/9wtmJG2uRq+jktCUGdLmBaCMnuOcQBLiU'
    }

    main(url, headers, payload)
