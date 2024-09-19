json_string = """
[
{
    "domain": ".facebook.com",
    "expirationDate": 1758189030.625478,
    "hostOnly": false,
    "httpOnly": false,
    "name": "c_user",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "1340587044",
    "id": 1
},
{
    "domain": ".facebook.com",
    "expirationDate": 1752685244,
    "hostOnly": false,
    "httpOnly": true,
    "name": "datr",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "0YFoZvmC_6zeFSXoA2_pALHu",
    "id": 2
},
{
    "domain": ".facebook.com",
    "expirationDate": 1734429030.625615,
    "hostOnly": false,
    "httpOnly": true,
    "name": "fr",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "1RPIL0B3CLJsyHS8u.AWVDTgvaUsVBV831R2jxCcBwziY.Bm6qJn..AAA.0.0.Bm6qJn.AWWIlptTceI",
    "id": 3
},
{
    "domain": ".facebook.com",
    "expirationDate": 1734413090,
    "hostOnly": false,
    "httpOnly": true,
    "name": "m_page_voice",
    "path": "/",
    "sameSite": "lax",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "1340587044",
    "id": 4
},
{
    "domain": ".facebook.com",
    "hostOnly": false,
    "httpOnly": false,
    "name": "presence",
    "path": "/",
    "sameSite": "unspecified",
    "secure": true,
    "session": true,
    "storeId": "0",
    "value": "C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1726653263780%2C%22v%22%3A1%7D",
    "id": 5
},
{
    "domain": ".facebook.com",
    "expirationDate": 1752685012,
    "hostOnly": false,
    "httpOnly": true,
    "name": "ps_l",
    "path": "/",
    "sameSite": "lax",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "1",
    "id": 6
},
{
    "domain": ".facebook.com",
    "expirationDate": 1752685012,
    "hostOnly": false,
    "httpOnly": true,
    "name": "ps_n",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "1",
    "id": 7
},
{
    "domain": ".facebook.com",
    "expirationDate": 1761189899,
    "hostOnly": false,
    "httpOnly": true,
    "name": "sb",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "1YFoZgCVnurv5SvnvFT84MBB",
    "id": 8
},
{
    "domain": ".facebook.com",
    "expirationDate": 1727258062,
    "hostOnly": false,
    "httpOnly": false,
    "name": "wd",
    "path": "/",
    "sameSite": "lax",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "1366x645",
    "id": 9
},
{
    "domain": ".facebook.com",
    "expirationDate": 1758189030.625817,
    "hostOnly": false,
    "httpOnly": true,
    "name": "xs",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "11%3ALZbWTdcboT0ghg%3A2%3A1726629900%3A-1%3A11194%3A%3AAcX3XdumtOrloN6wA_5HxrK3loQSP54HueJBLGIgS4Y",
    "id": 10
}
]
"""
import json

json_object = json.loads(json_string)
out_json = []
for elem in json_object:
    out_elem = {}
    for key, value in elem.items():
        out_elem[key[0].upper() + key[1:]] = value
    out_elem["Persistent"] = True
    out_elem["CanonicalHost"] = "mbasic.facebook.com"
    out_elem["Domain"] = "facebook.com"
    out_elem["Expires"] = "2099-01-30T00:00:00.000000+00:00"
    out_json.append(out_elem)
print(json.dumps(out_json).replace(' ', ''))