from rest_framework import viewsets, permissions,serializers
from django.shortcuts import get_object_or_404

from ..models import Art, Category
from ..contants import *



class ArtSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    class Meta:
        fields = ("id", "title", "tags", "category", "description", "is_featured", "image", "image_url", "number_of_views", "available_copies", "sold_amount", "discount")
        model = Art
        
    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get("request", None)
        if request is not None:
            if request.method not in permissions.SAFE_METHODS:
                #TODO: check image requirement
                fields.pop("image_url")
                fields.pop("sold_amount")
                fields.pop("number_of_views")
                fields.pop("id")
            if request.method in permissions.SAFE_METHODS:
                fields.pop('image')
                
        return fields
    
    def create(self, validated_data):
        from imagekitio import ImageKit
        imagekit = ImageKit(
            private_key=PRIVATE_KEY,
            public_key=PUBLIC_KEY,
            url_endpoint =URL_ENDPOINT
        )
        # uploading image to imagekitio
        upload = imagekit.upload_file(
            file= validated_data['image'],
            file_name= validated_data['title'],
            options= {
                "folder" : "/example-folder/",
                "tags": ["sample-tag"],
                "is_private_file": False,
                "use_unique_file_name": True,
                "response_fields": ["is_private_file", "tags"],
            }
        )
        # setting id from imagekitio
        validated_data['id'] = upload['response']['fileId']
        
        fields = super().get_fields()
        fields.pop('image')
        validated_data.pop('image')
        validated_data['image_url'] = upload['response']['url']
        
        
        
        art = Art.objects.create(**validated_data)
        return art
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Category

##########################################################

class ArtView(viewsets.ModelViewSet):
    serializer_class = ArtSerializer
    queryset = Art.objects.all()
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        obj.number_of_views += 1
        obj.save()
        return obj
    
class CategoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    
    # def get_permissions(self):
    #     if self.request.method in permissions.SAFE_METHODS:
    #         permission_classes = [permissions.AllowAny]
    #     else:
    #         permission_classes = [permissions.IsAuthenticated]
            
    #     return [permission() for permission in permission_classes]