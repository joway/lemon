import requests

req = requests.post('http://127.0.0.1:9999', cookies={
    'my_cookie': 'xxx',
    'my_cookie2': 'xxx2',
})

print(req.json())
