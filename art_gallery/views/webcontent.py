from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from ..contants import *


#web content edit
class TextContent(viewsets.ViewSet):
    
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
            
        return [permission() for permission in permission_classes]
    
    
    # TODO: needs admin permission protecttion
    def create(self, request):
        import json
        import os
        # Opening JSON file for text
        text_file = open(f'{os.getcwd()}/art_gallery/web_contents/text.json', 'r')
        text_contents = json.load(text_file)
        # Closing file
        text_file.close()

        text_sections = request.data

        for section in text_sections:
            for sec in text_sections[section]:
                text_contents[section][sec] = text_sections[section][sec]
        
        text_file = open(f'{os.getcwd()}/art_gallery/web_contents/text.json', 'w')  
        json.dump(text_contents, text_file)
        text_file.close()                    
        return Response({"Message": "Succesfully updated content."}, status=status.HTTP_202_ACCEPTED)
    
    def list(self, request):
        import json
        import os
        
        f = open(f'{os.getcwd()}/art_gallery/web_contents/text.json', 'r')
        contents = json.load(f)
        f.close()
        
        f = open(f'{os.getcwd()}/art_gallery/web_contents/text.json', 'w')
        contents["website_visits"] = contents["website_visits"] + 1
        json.dump(contents, f)
        f.close()
        contents.pop("website_visits")
        return Response(contents, status=status.HTTP_200_OK)
    
class ImageContent(viewsets.ViewSet):
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
    
    def create(self, request):
        import json
        import os
        from imagekitio import ImageKit
        image_file = open(f'{os.getcwd()}/art_gallery/web_contents/images.json', 'r')
        image_contents = json.load(image_file)
        # Closing file
        image_file.close() 
        image_sections = request.FILES
        print(image_sections)
        for image_section in image_sections:
            imagekit = ImageKit(
                private_key=PRIVATE_KEY, 
                public_key=PUBLIC_KEY,  
                url_endpoint=URL_ENDPOINT  
            )
            # uploading image to imagekitio
            upload = imagekit.upload_file(
                file=image_sections[image_section],
                file_name= image_section,
                options= {
                    "folder" : "/example-folder/",
                    "tags": ["sample-tag"],
                    "is_private_file": False,
                    "use_unique_file_name": True,
                    "response_fields": ["is_private_file", "tags"],
                }
            )
            image_contents[image_section] = upload['response']['url']
     
        image_file = open(f'{os.getcwd()}/art_gallery/web_contents/images.json', 'w')  
        json.dump(image_contents, image_file)
        image_file.close()                    
        return Response({"Message": "Succesfully updated content."}, status=status.HTTP_202_ACCEPTED)
    
    def list(self, request):
        import json
        import os
        f = open(f'{os.getcwd()}/art_gallery/web_contents/images.json', 'r')      
        contents = json.load(f)
        f.close()     
        return Response(contents, status=status.HTTP_200_OK)   
    
    def destroy(self, request, pk=None):
        import json
        import os
        #TODO: also delete from imagekitio
        
        image_file = open(f'{os.getcwd()}/art_gallery/web_contents/images.json', 'r')
        image_contents = json.load(image_file)   
        image_file.close()
        
        image_contents[pk] = ""
        image_file = open(f'{os.getcwd()}/art_gallery/web_contents/images.json', 'w')  
        json.dump(image_contents, image_file)
        image_file.close()                    
        return Response({"Message": "Succesfully removed image."}, status=status.HTTP_202_ACCEPTED)