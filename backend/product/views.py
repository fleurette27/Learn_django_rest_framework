from django.http import JsonResponse
from django.shortcuts import render
from django.forms.models import model_to_dict

from api_rest.mixins import StaffEditorPermissionMixins, UserQuerrySetMixin

from .models import Product
#django rest framework
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializer import ProductSerializer
from rest_framework import authentication,generics,mixins,permissions
from api_rest.permissions import IsStaffPermission
from .authentication import TokenAuthentication
# CRUD

class DetailProductApiView(StaffEditorPermissionMixins,generics.RetrieveAPIView
                           ):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    # plus la peine vu qu'on a créé la classe StaffEditorPermissionMixins dans api_rest/mixins 
    # permission_classes=[permissions.IsAdminUser,IsStaffPermission]


class CreateProductApiView(StaffEditorPermissionMixins,generics.CreateAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer

    def perform_create(self, serializer):
        name=serializer.validated_data.get('name')
        content=serializer.validated_data.get('content') or None
        if content is None:
            content=name
        serializer.save(content=content)

class UpdateProductApiView(StaffEditorPermissionMixins,generics.UpdateAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    lookup_field='pk'

    def perform_update(self, serializer):
        name=serializer.validated_data.get('name')
        content=serializer.validated_data.get('content') or None
        if content is None:
            content=name
        serializer.save(content=content)

class DeleteProductApiView(StaffEditorPermissionMixins,generics.DestroyAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    lookup_field='pk'


# notion de permission
class GetListProductApiView(StaffEditorPermissionMixins,
                            UserQuerrySetMixin,generics.ListCreateAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    user_field='user'
    #deja mit pas defaut dans le setting donc il ne sert plus a rien
    # authentication_classes=[TokenAuthentication,authentication.SessionAuthentication]
    # permission_classes=[permissions.IsAuthenticatedOrReadOnly,permissions.DjangoModelPermissions]
    # permissions personnalisées

    def perform_create(self, serializer):
        name=serializer.validated_data.get('name')
        email=serializer.validated_data.pop('email')
        content=serializer.validated_data.get('content') or None
        print(email)
        if content is None:
            content=name
        serializer.save(content=content,user=self.request.user)



    

class ListProductApiView(generics.ListAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    def get_queryset(self):
        return super().get_queryset().filter(name__icontains='Avocat')

# Au lieu d'ecrit tt cela ,on peut faire un router comme dans le viewset.py,routers.py
class ProductMixinsViews(generics.GenericAPIView,
                         mixins.CreateModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.ListModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.RetrieveModelMixin,
                        ):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    lookup_field='pk'

    def perform_create(self, serializer):
        name=serializer.validated_data.get('name')
        content=serializer.validated_data.get('content') or None
        if content is None:
            content=name
        serializer.save(content=content)

    def perform_update(self, serializer):
        name=serializer.validated_data.get('name')
        content=serializer.validated_data.get('content') or None
        if content is None:
            content=name
        serializer.save(content=content)  

    def get(self, request, *args, **kwargs):
        pk=kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args,**kwargs)
        return self.list(request,*args,**kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request,*args,**kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request,*args,**kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request,*args,**kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)













#en django rest framework
# @api_view(['POST'])
# def api_view(request):
#     serializer= ProductSerializer(data=request.data)
#     if serializer.is_valid(raise_exception=True):
#          serializer.save()
#          return Response(serializer.data) 
#     else:
#          return Response({'detail':'invalid data'})   


# @api_view(['GET'])
# def api_view(request):
#     query=Product.objects.all().order_by('?').first()
#     data={}
#     if query:
#         data=ProductSerializer(query).data
#     return Response(data)    


#on l'aurait faire comme ca en django
# def api_view(request):
#     query=Product.objects.all().order_by('?').first()
#     #? c'est pour l'envoie aleatoire
#     data={}
#     if query:
#         #serialization :mettre les données sous forme de dictionnaire 
#         # data['name']=query.name
#         # data['content']=query.content
#         # data['price']=query.pric
#         #utilisation de model_to_dict
#         data=model_to_dict(query)
#         #selection des champs de recuperation
#         data=model_to_dict(query,fields=('name','price'))

#     return JsonResponse(data)    

