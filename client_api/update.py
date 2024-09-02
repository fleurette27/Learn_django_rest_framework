import requests 

endpoint="http://127.0.0.1:8000/product/update/9/"
response=requests.put(endpoint,json={'name':'Fraise','content':'','price':'1000'})
# print(response.json())
print(response.status_code)

