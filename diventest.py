import requests

url = "https://astroapi-3.divineapi.com/indian-api/v1/english-calendar-festivals"

payload = {'api_key': '2cbe6fce5ad1b5379adb736f80f4cb24',
'year': '2023',
'Place': 'New Delhi',
'lat': '28.6139',
'lon': '77.2090',
'tzone': '5.5'}

headers = {
  'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL2RpdmluZWFwaS5jb20vc2lnbnVwIiwiaWF0IjoxNzY0NDk0NzcyLCJuYmYiOjE3NjQ0OTQ3NzIsImp0aSI6Ik5GZExobUZMcEFQN3FTTVkiLCJzdWIiOiI0NTI4IiwicHJ2IjoiZTZlNjRiYjBiNjEyNmQ3M2M2Yjk3YWZjM2I0NjRkOTg1ZjQ2YzlkNyJ9.vXKNf89A4BP5RXHIFtyf4PC0DFCtdhL9EmxI0AVTsI4'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
