from getpass import getpass
import requests 


endpoint='http://127.0.0.1:8000/api/auth'
username=input('Entrez votre username: \n')
password=getpass('Entrez votre password: \n')
auth_response=requests.post(endpoint,json={'username':username,'password':password})
print(auth_response.json())
if auth_response.status_code==200:
# les deux font la meme chose
# pour la route get_liste,on peut aussi faire un post ,pour créer une liste de produire
    endpoint="http://127.0.0.1:8000/product/get_create_list/"
    headers={
        'Authorization':'Bearer 129f235327aae81d888e9a172d81a9958f414476'
    }
# pour la route list_create
# endpoint="http://127.0.0.1:8000/product/list_create/"
# endpoint="http://127.0.0.1:8000/product/list/"
    response=requests.get(endpoint,headers=headers)
# response=requests.post(endpoint,json={'name':'Citron','content':'','price':200})
    print(response.json())
    print(response.status_code)

