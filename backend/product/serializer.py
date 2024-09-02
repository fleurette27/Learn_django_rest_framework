from rest_framework import serializers
from rest_framework.reverse import reverse
from .validators import validators_unique_product_name
from api_rest.serializer import UserPublicSerializer
from .models import Product 



class UserProductInlineSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(view_name='product-detail', lookup_field='pk')
    email = serializers.EmailField(write_only=True)
    name = serializers.CharField()
    

class ProductSerializer(serializers.ModelSerializer):
    # url=serializers.SerializerMethodField(read_only=True)
    # def get_url(self,obj):
    #     request=self.context.get('request')
    #     if request is None:
    #         return None
    #     return reverse("product-detail",kwargs={'pk':obj.pk},request=request)

    # ce url fait la meme chose que ce qui est en haut 
    url = serializers.HyperlinkedIdentityField(view_name='product-detail', lookup_field='pk')
    email = serializers.EmailField(write_only=True)
    name = serializers.CharField(validators=[validators_unique_product_name])
    # user_name=serializers.CharField(source="user.username" ,read_only=True)
    owner = UserProductInlineSerializer(read_only=True, many=True, source='user.product_set.all')


    # def create(self,validated_data):
    #     print(validated_data)
    #     email=validated_data.pop('email')
    #     print(email)
    #     print(validated_data)
    #     # return Product.objects.create(**validated_data)
    #     obj=super().create(validated_data)
    #     return obj

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name')
        return super().update(instance, validated_data)
    
    def validate_name(self, value):
        request = self.context.get('request')
        qs = Product.objects.filter(name__iexact=value)
        if qs.exists():
           raise serializers.ValidationError(f"Le produit {value} existe deja en db")
        return value        
    
      
    #si on veut passer la methode get_discount a travers un champs my_discount
    my_discount=serializers.SerializerMethodField(read_only=True)
    def get_my_discount(self,obj):
        if not hasattr (obj, 'id'):
            return None
        if not isinstance(obj, Product):
            return None
        return obj.get_discount

    class Meta:
        model=Product
        fields=('owner','url','pk','email','name','content','price','my_discount','get_discount')
        