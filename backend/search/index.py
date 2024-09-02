from product.models import Product
import algoliasearch_django as algoliasearch
from algoliasearch_django import AlgoliaIndex

algoliasearch.register(Product)
# @register(Product)
class ProductIndex(AlgoliaIndex):
    # should_index = "is_public"
    fields = [
        'name',
        'content',
        'price',
        'public',
        'user',
        
    ]
    tags = "get_tags_list"

    settings = {
        'searchableAttributes':['name', 'content'],
        'attributesForFaceting':['user', 'public']
    }


