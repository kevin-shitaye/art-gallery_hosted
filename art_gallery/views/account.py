from rest_framework import viewsets, permissions, generics, serializers, status
from rest_framework.response import Response
from ..models import Client, Account
from ..contants import *

# from ..casefold()email_config import email_sender

########### serializer ################
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["user_name","first_name","last_name","email","phone_number","facebook","telegram","instagram","tiktok","youtube","twitter","linkedin","email_notification", "gmail_smtp_key"]
    
    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get("request", None)
        if request is not None:
            # KEYPOINT: if different accounts are creatded check here
            if  request.user is not Account:
                fields.pop("user_name")
                fields.pop("last_name")
                fields.pop("first_name")
                fields.pop("email_notification")
                fields.pop("gmail_smtp_key")

        return fields
    
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Client

##########################################

class AccountView(generics.RetrieveUpdateAPIView):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
class ClientView(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    
class Subscribe(viewsets.ViewSet):
    
    # creating a client model when a client subcribes to a newsletter
    def create(self, request):
        client = Client.objects.get_or_create(email=request.data['email'])
         # client[0] because the above statement returns a tuple (obj, bool)
        client[0].is_subscribed = True
        client[0].save()
        from ..email_config import email_sender  
        # TODO: getting the admin this way is not right
        admin = Account.objects.filter(pk=1).first()  
        email_sender.send(
                sender=admin.email,
                receivers=[client[0].email],
                subject=f"Your have subcribed to R3R3 newsletter.",
                text="Hi, Welcome. \n You have subribed to my weekly newsletter where I share upcoming events and notify you about awsome discounts and deals."
            )
        return Response({"Message": "Succesfully subscribed."}, status=status.HTTP_202_ACCEPTED)

class UnSubscribe(viewsets.ViewSet):
    def create(self, request):
        client = Client.objects.filter(email=request.data['email']).first()
        client.is_subscribed = False
        client.save()
        
        from ..email_config import email_sender  
        # TODO: getting the admin this way is not right
        admin = Account.objects.filter(pk=1).first()  
        email_sender.send(
                sender=admin.email,
                receivers=[client[0].email],
                subject=f"Your have unsubcribed from R3R3 newsletter.",
                text=":("
            )
        return Response({"Message": "Succesfully Unsubscribed."}, status=status.HTTP_202_ACCEPTED)