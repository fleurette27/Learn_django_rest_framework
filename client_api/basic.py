import requests 

endpoint="http://127.0.0.1:8000/product"
# response=requests.get(endpoint)
response=requests.post(endpoint,json={'name':'Pasteque','content':'just pasteque','price':20})
print(response.json())
print(response.status_code)

#http resquest--> html
#rest api http --> json (js object notation)