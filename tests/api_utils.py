import http.client
import json

CLIENT_CODE = "AAAK529196"
CLIENT_PIN = "1807"  # Replace with your actual password
TOTP_CODE = "AJTURKJ6NLTJWCMLAY5L6KU6Z4"  # Replace with your current TOTP
STATE_VARIABLE = ""

CLIENT_LOCAL_IP = "192.168.31.153"
CLIENT_PUBLIC_IP = "152.58.33.164"
MAC_ADDRESS = "4C-BB-58-F2-76-DA"
API_KEY = "HXZlCLIo"
AUTHORIZATION_TOKEN = ""  # Replace after login
REFRESH_TOKEN = "YOUR_REFRESH_TOKEN"              # Replace when available

def post_request(path, payload_dict, headers):
    conn = http.client.HTTPSConnection("apiconnect.angelone.in")
    payload = json.dumps(payload_dict)
    conn.request("POST", path, payload, headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")

def get_request(path, headers):
    conn = http.client.HTTPSConnection("apiconnect.angelone.in")
    conn.request("GET", path, headers=headers)
    res = conn.getresponse()
    data = res.read()
    return data.decode("utf-8")

common_headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'X-UserType': 'USER',
    'X-SourceID': 'WEB',
    'X-ClientLocalIP': CLIENT_LOCAL_IP,
    'X-ClientPublicIP': CLIENT_PUBLIC_IP,
    'X-MACAddress': MAC_ADDRESS,
    'X-PrivateKey': API_KEY,
}

print("Login Response:")
login_payload = {
    "clientcode": CLIENT_CODE,
    "password": CLIENT_PIN,
    "totp": TOTP_CODE,
    "state": STATE_VARIABLE
}
login_response = post_request("/rest/auth/angelbroking/user/v1/loginByPassword", login_payload, common_headers)
print(login_response)

auth_headers = common_headers.copy()
auth_headers['Authorization'] = f"Bearer {AUTHORIZATION_TOKEN}"

print("\nGet Profile Response:")
profile_response = get_request("/rest/secure/angelbroking/user/v1/getProfile", auth_headers)
print(profile_response)

print("\nGet RMS Response:")
rms_response = get_request("/rest/secure/angelbroking/user/v1/getRMS", auth_headers)
print(rms_response)

print("\nLogout Response:")
logout_payload = {
    "clientcode": CLIENT_CODE
}
logout_response = post_request("/rest/secure/angelbroking/user/v1/logout", logout_payload, auth_headers)
print(logout_response)

print("\nRefresh Tokens Response:")
refresh_payload = {
    "refreshToken": REFRESH_TOKEN
}
refresh_response = post_request("/rest/auth/angelbroking/jwt/v1/generateTokens", refresh_payload, common_headers)
print(refresh_response)
