import requests
import json


r = requests.get('http://0.0.0.0:5000/api/health')
print(r.status_code, r.text)

payload = [
    {"name":"example1", "t":13515551,"v":1.1},
    {"name":"example1", "t":13515552,"v":2.4},
    {"name":"example1", "t":13515553,"v":3.5},
    {"name":"example2", "t":13515554,"v":1.5},
    {"name":"example2", "t":13515555,"v":2.5},
]
r = requests.post('http://0.0.0.0:5000/api/add_customers', json=payload)
print(r.status_code, r.text)

r = requests.get('http://0.0.0.0:5000/api/get_average/example1/13515551/13515553')
print(r.status_code, r.text)