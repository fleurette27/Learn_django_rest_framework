import requests 

endpoint="http://127.0.0.1:8000/product/create/"
response=requests.post(endpoint,json={'name':'cerise','content':'','price':200})
print(response.json())
print(response.status_code)

