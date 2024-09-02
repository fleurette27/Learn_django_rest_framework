import requests 

id=input('enter the id of product thaht you want delete: ')
endpoint= f"http://127.0.0.1:8000/product/delete/{id}/"
response= requests.delete(endpoint)
print(response.status_code,response.status_code==204)

