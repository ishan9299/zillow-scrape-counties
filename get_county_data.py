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

    cookies = {
        'pxcts': 'd9383916-fcb4-11ef-9169-e696bb45f1b5',
        '_pxvid': 'd9382ded-fcb4-11ef-9169-62aa21edb82f',
        '_px3': '97558dbd9d3b93a1c30daf87b33277a8f4123f1b27e68a824d1aa2f256901e21:aTbH78HLkYHj9KU56r2470j0sPkPMM6avOw3h17voJbvkuxVKJgD0yGqXutvM/6KtxlyBPxM5F2Ygqv1rmo/gQ==:1000:on+C2F4VRJd/8vcbL2Zxj/3SrJKNEbw1s8pgnHoGyHIkfeEaA8W6xYhGQ/Ek7mBmhCg6kxGXNDMrnKkLDysexFefMSrCtB/acXDRq26dyowY2aveRRkx00WIH3IeB7anrdHisnGSLUhJART0xgzgax7KxwML7QhUyoGIyMnEztxyL5w/t/irApeDim+lySkVtkY1WuUCouiRFiix9e4Wn460MrcLHAsilnhAzf51KpA=',
        'zguid': '24|%24945183f9-7b15-4d4a-97cb-c0d090cbb08c',
        'zgsession': '1|737725ed-4efc-4dea-98fb-23f7bfc01cfd',
        '_ga': 'GA1.2.428334007.1741503934',
        '_gid': 'GA1.2.236554809.1741503934',
        'zjs_anonymous_id': '%22945183f9-7b15-4d4a-97cb-c0d090cbb08c%22',
        'zjs_user_id': 'null',
        'zg_anonymous_id': '%2256a008ec-b2ab-43db-9769-a4b537520c38%22',
        'JSESSIONID': 'AE06B5C8DCB3AC5BA55FF5E4670AD3A9',
        '_gcl_au': '1.1.133566676.1741503939',
        '_rdt_uuid': '1741503945536.2bab3f6b-6155-440d-b42c-c766f9ee06ec',
        '_uetsid': 'ec4b9230fcb411efb851c9f67767156f',
        '_uetvid': 'ec4ba9d0fcb411ef8ec79dbf13677920',
        '_scid': 'eUaKwa5LhhI1Nxm8L1Il8YdbRk4kMiZk',
        '_scid_r': 'eUaKwa5LhhI1Nxm8L1Il8YdbRk4kMiZk',
        'DoubleClickSession': 'true',
        '_fbp': 'fb.1.1741503946586.308745867433675118',
        'tfpsi': '47b6df6f-b269-4f17-850e-5b48b3456add',
        '_pin_unauth': 'dWlkPVl6UTBZakZsWWpNdE1EZzJaaTAwT1dZNExXSTVPR010WVRCa05UQTRZekpoTUdFNQ',
        '_ScCbts': '%5B%5D',
        '_clck': 'v3jgtd%7C2%7Cfu2%7C0%7C1894',
        '_clsk': 'f8ppwq%7C1741503949257%7C1%7C0%7Co.clarity.ms%2Fcollect',
        '_sctr': '1%7C1741458600000',
        '_dd_s': 'rum=0&expire=1741504874137',
        'web-platform-data': '%7B%22wp-dd-rum-session%22%3A%7B%22doNotTrack%22%3Atrue%7D%7D',
        'AWSALB': 'O88smUxkqVTB1Akup16gjcXLvqNx37XTSUtDuUYZ+R3PvRc7J07hrdIL7u4SyZeqtwllkACEEI76QCJ+L6jksJeSwHPkY4ml3ePpjwsvZ1FJSB6NZZxvbaPlt10r',
        'AWSALBCORS': 'O88smUxkqVTB1Akup16gjcXLvqNx37XTSUtDuUYZ+R3PvRc7J07hrdIL7u4SyZeqtwllkACEEI76QCJ+L6jksJeSwHPkY4ml3ePpjwsvZ1FJSB6NZZxvbaPlt10r',
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
        'referer': 'https://www.zillow.com/homes/4_rid/',
        'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        # 'cookie': 'pxcts=d9383916-fcb4-11ef-9169-e696bb45f1b5; _pxvid=d9382ded-fcb4-11ef-9169-62aa21edb82f; _px3=97558dbd9d3b93a1c30daf87b33277a8f4123f1b27e68a824d1aa2f256901e21:aTbH78HLkYHj9KU56r2470j0sPkPMM6avOw3h17voJbvkuxVKJgD0yGqXutvM/6KtxlyBPxM5F2Ygqv1rmo/gQ==:1000:on+C2F4VRJd/8vcbL2Zxj/3SrJKNEbw1s8pgnHoGyHIkfeEaA8W6xYhGQ/Ek7mBmhCg6kxGXNDMrnKkLDysexFefMSrCtB/acXDRq26dyowY2aveRRkx00WIH3IeB7anrdHisnGSLUhJART0xgzgax7KxwML7QhUyoGIyMnEztxyL5w/t/irApeDim+lySkVtkY1WuUCouiRFiix9e4Wn460MrcLHAsilnhAzf51KpA=; zguid=24|%24945183f9-7b15-4d4a-97cb-c0d090cbb08c; zgsession=1|737725ed-4efc-4dea-98fb-23f7bfc01cfd; _ga=GA1.2.428334007.1741503934; _gid=GA1.2.236554809.1741503934; zjs_anonymous_id=%22945183f9-7b15-4d4a-97cb-c0d090cbb08c%22; zjs_user_id=null; zg_anonymous_id=%2256a008ec-b2ab-43db-9769-a4b537520c38%22; JSESSIONID=AE06B5C8DCB3AC5BA55FF5E4670AD3A9; _gcl_au=1.1.133566676.1741503939; _rdt_uuid=1741503945536.2bab3f6b-6155-440d-b42c-c766f9ee06ec; _uetsid=ec4b9230fcb411efb851c9f67767156f; _uetvid=ec4ba9d0fcb411ef8ec79dbf13677920; _scid=eUaKwa5LhhI1Nxm8L1Il8YdbRk4kMiZk; _scid_r=eUaKwa5LhhI1Nxm8L1Il8YdbRk4kMiZk; DoubleClickSession=true; _fbp=fb.1.1741503946586.308745867433675118; tfpsi=47b6df6f-b269-4f17-850e-5b48b3456add; _pin_unauth=dWlkPVl6UTBZakZsWWpNdE1EZzJaaTAwT1dZNExXSTVPR010WVRCa05UQTRZekpoTUdFNQ; _ScCbts=%5B%5D; _clck=v3jgtd%7C2%7Cfu2%7C0%7C1894; _clsk=f8ppwq%7C1741503949257%7C1%7C0%7Co.clarity.ms%2Fcollect; _sctr=1%7C1741458600000; _dd_s=rum=0&expire=1741504874137; web-platform-data=%7B%22wp-dd-rum-session%22%3A%7B%22doNotTrack%22%3Atrue%7D%7D; AWSALB=O88smUxkqVTB1Akup16gjcXLvqNx37XTSUtDuUYZ+R3PvRc7J07hrdIL7u4SyZeqtwllkACEEI76QCJ+L6jksJeSwHPkY4ml3ePpjwsvZ1FJSB6NZZxvbaPlt10r; AWSALBCORS=O88smUxkqVTB1Akup16gjcXLvqNx37XTSUtDuUYZ+R3PvRc7J07hrdIL7u4SyZeqtwllkACEEI76QCJ+L6jksJeSwHPkY4ml3ePpjwsvZ1FJSB6NZZxvbaPlt10r',
    }

    main(url, headers, cookies, payload)
