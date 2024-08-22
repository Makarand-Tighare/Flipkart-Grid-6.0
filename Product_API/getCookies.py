import requests

# Define the URL and the headers you want to use
url = "https://1.rome.api.flipkart.com/api/5/self-serve/orders/?page=1&filterType=PREORDER_UNITS"
cookies = {
        "T": "cm053lge802c213bn4gwqooz1-BR1724319980864",
        "K-ACTION": "null",
        "vh": "813",
        "vw": "617",
        "dpr": "2",
        "Network-Type": "4g",
        "AMCVS_17EB401053DAF4840A490D4C%40AdobeOrg": "1",
        "gpv_pn": "HomePage",
        "gpv_pn_t": "FLIPKART%3AHomePage",
        "AMCV_17EB401053DAF4840A490D4C%40AdobeOrg": "-227196251%7CMCIDTS%7C19958%7CMCMID%7C21710891124751702416899752741292449003%7CMCAID%7CNONE%7CMCOPTOUT-1724327182s%7CNONE%7CMCAAMLH-1724924782%7C7%7CMCAAMB-1724924782%7Cj8Odv6LonN4r3an7LhD3WZrU1bUpAkFkkiY1ncBR96t2PTI",
        "ULSN": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJjb29raWUiLCJhdWQiOiJmbGlwa2FydCIsImlzcyI6ImF1dGguZmxpcGthcnQuY29tIiwiY2xhaW1zIjp7ImdlbiI6IjEiLCJ1bmlxdWVJZCI6IlVVSTI0MDgyMjE1MTYzODcyNUNRQlBXOU8iLCJma0RldiI6bnVsbH0sImV4cCI6MTc0MDA5OTk5OCwiaWF0IjoxNzI0MzE5OTk4LCJqdGkiOiIzZjAxNDVmNS1mM2ViLTQxNTYtYTAyYi01ZWRiNzljZWMxOWYifQ.m7caxkuDgMsXjSOsOoZMAnzJ0PvlVg6vNfDLVtWJXSQ",
        "at": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjNhNzdlZTgxLTRjNWYtNGU5Ni04ZmRlLWM3YWMyYjVlOTA1NSJ9.eyJleHAiOjE3MjQzMjE3OTgsImlhdCI6MTcyNDMxOTk5OCwiaXNzIjoia2V2bGFyIiwianRpIjoiMjhhMjNiMGUtMmY2Yy00ZDQyLWI2NDctMDc0NGYwN2NiYjIwIiwidHlwZSI6IkFUIiwiZElkIjoiY20wNTNsZ2U4MDJjMjEzYm40Z3dxb296MS1CUjE3MjQzMTk5ODA4NjQiLCJiSWQiOiI2QVlRNEEiLCJrZXZJZCI6IlZJNDRBQkE1QkQwMEQxNDNCRTlFMDUyNEMxRjBCRkQ4QkUiLCJ0SWQiOiJtYXBpIiwiZWFJZCI6ImhpS0dmUzd2T2JVZm90LTV2ZmJ0bzhPTWR5YWpWT3JVYThFUVdVOXdWb0stRGRLQXctX1Z6Zz09IiwidnMiOiJMSSIsInoiOiJIWUQiLCJtIjp0cnVlLCJnZW4iOjR9.iYd_IAtJWo8Kb1Mff4K_Xre5tMAXu9ZQYvcWQfadUBM",
        "rt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjhlM2ZhMGE3LTJmZDMtNGNiMi05MWRjLTZlNTMxOGU1YTkxZiJ9.eyJleHAiOjE3NDAyMTc1OTgsImlhdCI6MTcyNDMxOTk5OCwiaXNzIjoia2V2bGFyIiwianRpIjoiMjFjNTI5ZTktOTMxMy00NDVmLTgzOTItMmQwM2RhNmM2YWEwIiwidHlwZSI6IlJUIiwiZElkIjoiY20wNTNsZ2U4MDJjMjEzYm40Z3dxb296MS1CUjE3MjQzMTk5ODA4NjQiLCJiSWQiOiI2QVlRNEEiLCJrZXZJZCI6IlZJNDRBQkE1QkQwMEQxNDNCRTlFMDUyNEMxRjBCRkQ4QkUiLCJ0SWQiOiJtYXBpIiwibSI6eyJ0eXBlIjoibiJ9LCJ2IjoiOTNPT01SIn0.j7pt4q52Ysg8dnQvs9Wvb0fMIgCT2rcaRLFcw7M04qg",
        "ud": "0.kg-XnFW5gcfK9f7SstW1IN72H5ij2JFnXkB84-sRkKjeLx8FuK0ArnV4teTZg9SCn08Rp9txeGpCDJeljDGxuUjAs0jDuVoZ6-X2VTbI5b5dZK0NoKlzGOvdiF8pMl04-8lRJzvBKFYFUEORigrG0qe85LGm-vZv91UXgLCdAscUeN7uoqHajOaxDLKNfehO",
        "S": "d1t11IT8hMA4LPz8/Rj9cP3o/P4HztCuxUO+Zq/Tq9uJnV0AnXO598u29mvoRHxaWsLE0zCJIxY9aSThGdBtn8KSSjw==",
        "s_sq": "flipkart-prd%3D%2526pid%253Dwww.flipkart.com%25253Aaccount%25253Alogin%2526pidt%253D1%2526oid%253DVerify%2526oidt%253D3%2526ot%253DSUBMIT",
        "SN": "VI44ABA5BD00D143BE9E0524C1F0BFD8BE.TOKE1E846567F9D41789DF64580CC5E0D4E.1724320024.LI",
        "vd": "VI44ABA5BD00D143BE9E0524C1F0BFD8BE-1724319983063-1.1724320078.1724319983.155731869"
}

# Combine all cookies into a single string
headers = {
     "accept": "*/*",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "content-type": "application/json",
        "cookie": "T=cm053lge802c213bn4gwqooz1-BR1724319980864; K-ACTION=null; vh=813; vw=617; dpr=2; Network-Type=4g; AMCVS_17EB401053DAF4840A490D4C%40AdobeOrg=1; gpv_pn=HomePage; gpv_pn_t=FLIPKART%3AHomePage; AMCV_17EB401053DAF4840A490D4C%40AdobeOrg=-227196251%7CMCIDTS%7C19958%7CMCMID%7C21710891124751702416899752741292449003%7CMCAID%7CNONE%7CMCOPTOUT-1724327182s%7CNONE%7CMCAAMLH-1724924782%7C7%7CMCAAMB-1724924782%7Cj8Odv6LonN4r3an7LhD3WZrU1bUpAkFkkiY1ncBR96t2PTI; ULSN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJjb29raWUiLCJhdWQiOiJmbGlwa2FydCIsImlzcyI6ImF1dGguZmxpcGthcnQuY29tIiwiY2xhaW1zIjp7ImdlbiI6IjEiLCJ1bmlxdWVJZCI6IlVVSTI0MDgyMjE1MTYzODcyNUNRQlBXOU8iLCJma0RldiI6bnVsbH0sImV4cCI6MTc0MDA5OTk5OCwiaWF0IjoxNzI0MzE5OTk4LCJqdGkiOiIzZjAxNDVmNS1mM2ViLTQxNTYtYTAyYi01ZWRiNzljZWMxOWYifQ.m7caxkuDgMsXjSOsOoZMAnzJ0PvlVg6vNfDLVtWJXSQ; at=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjNhNzdlZTgxLTRjNWYtNGU5Ni04ZmRlLWM3YWMyYjVlOTA1NSJ9.eyJleHAiOjE3MjQzMjE3OTgsImlhdCI6MTcyNDMxOTk5OCwiaXNzIjoia2V2bGFyIiwianRpIjoiMjhhMjNiMGUtMmY2Yy00ZDQyLWI2NDctMDc0NGYwN2NiYjIwIiwidHlwZSI6IkFUIiwiZElkIjoiY20wNTNsZ2U4MDJjMjEzYm40Z3dxb296MS1CUjE3MjQzMTk5ODA4NjQiLCJiSWQiOiI2QVlRNEEiLCJrZXZJZCI6IlZJNDRBQkE1QkQwMEQxNDNCRTlFMDUyNEMxRjBCRkQ4QkUiLCJ0SWQiOiJtYXBpIiwiZWFJZCI6ImhpS0dmUzd2T2JVZm90LTV2ZmJ0bzhPTWR5YWpWT3JVYThFUVdVOXdWb0stRGRLQXctX1Z6Zz09IiwidnMiOiJMSSIsInoiOiJIWUQiLCJtIjp0cnVlLCJnZW4iOjR9.iYd_IAtJWo8Kb1Mff4K_Xre5tMAXu9ZQYvcWQfadUBM; rt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjhlM2ZhMGE3LTJmZDMtNGNiMi05MWRjLTZlNTMxOGU1YTkxZiJ9.eyJleHAiOjE3NDAyMTc1OTgsImlhdCI6MTcyNDMxOTk5OCwiaXNzIjoia2V2bGFyIiwianRpIjoiMjFjNTI5ZTktOTMxMy00NDVmLTgzOTItMmQwM2RhNmM2YWEwIiwidHlwZSI6IlJUIiwiZElkIjoiY20wNTNsZ2U4MDJjMjEzYm40Z3dxb296MS1CUjE3MjQzMTk5ODA4NjQiLCJiSWQiOiI2QVlRNEEiLCJrZXZJZCI6IlZJNDRBQkE1QkQwMEQxNDNCRTlFMDUyNEMxRjBCRkQ4QkUiLCJ0SWQiOiJtYXBpIiwibSI6eyJ0eXBlIjoibiJ9LCJ2IjoiOTNPT01SIn0.j7pt4q52Ysg8dnQvs9Wvb0fMIgCT2rcaRLFcw7M04qg; ud=0.kg-XnFW5gcfK9f7SstW1IN72H5ij2JFnXkB84-sRkKjeLx8FuK0ArnV4teTZg9SCn08Rp9txeGpCDJeljDGxuUjAs0jDuVoZ6-X2VTbI5b5dZK0NoKlzGOvdiF8pMl04-8lRJzvBKFYFUEORigrG0qe85LGm-vZv91UXgLCdAscUeN7uoqHajOaxDLKNfehO; S=d1t11IT8hMA4LPz8/Rj9cP3o/P4HztCuxUO+Zq/Tq9uJnV0AnXO598u29mvoRHxaWsLE0zCJIxY9aSThGdBtn8KSSjw==; s_sq=flipkart-prd%3D%2526pid%253Dwww.flipkart.com%25253Aaccount%25253Alogin%2526pidt%253D1%2526oid%253DVerify%2526oidt%253D3%2526ot%253DSUBMIT; SN=VI44ABA5BD00D143BE9E0524C1F0BFD8BE.TOKE1E846567F9D41789DF64580CC5E0D4E.1724320024.LI; vd=VI44ABA5BD00D143BE9E0524C1F0BFD8BE-1724319983063-1.1724320078.1724319983.155731869",
        "origin": "https://www.flipkart.com",
        "priority": "u=1, i",
        "referer": "https://www.flipkart.com/",
        "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "x-user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 FKUA/website/42/website/Desktop"
}

# Send the request
response = requests.get(url, headers=headers, cookies=cookies)

# Extract and print all cookies from the response
print("Cookies received from the server:")
for cookie in response.cookies:
    print(f"{cookie.name}={cookie.value}")

# Save cookies to a file
with open('cookies.txt', 'w') as file:
    for cookie in response.cookies:
        file.write(f""" "{cookie.name}" : "{cookie.value}"\n""")

# Print response headers
print("Response headers:")
for header, value in response.headers.items():
    print(f"{header}: {value}")


print("Cookies have been saved to 'cookies.txt'")
