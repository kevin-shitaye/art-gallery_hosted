from rest_framework import viewsets, status, permissions, serializers
from rest_framework.response import Response

from ..models import EmailMessage, Client, Account



class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = EmailMessage
        
    def create(self, validated_data):
        category = validated_data['recipients']
    
        clients = Client.objects.filter(is_subscribed=category["is_subscribed"], has_contacted=category["has_contacted"], has_purchased=["has_purchased"])
          #extracting email adresses
        emails = [client.email for client in clients]
        
        validated_data.pop('recipients')
        message = EmailMessage.objects.create(**validated_data)
        message.recipients.set(emails)
        message.save()
        
        from .email_config import email_sender
        # TODO: getting the admin this way is not right
        admin = Account.objects.filter(pk=1).first()
        email_sender.send(
                sender=admin.email,
                receivers=message.recipients,
                subject=message.subject,
                attachments=message.attachement
            )
        
        return message
    
    
class Email(viewsets.ModelViewSet):
    
    serializer_class = EmailSerializer
    queryset = EmailMessage.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    
class ContactMe(viewsets.ViewSet):
    
    def create(self, request):
        data = request.data
        client = Client.objects.get_or_create(email=request.data['email'])
        email_message = EmailMessage.objects.create(subject=data['subject'], body=data['body'])
        email_message.recipients.set([client[0]])
        
        from ..email_config import email_sender
        # TODO: getting the admin this way is not right
        admin = Account.objects.filter(pk=1).first()  
        email_sender.send(
                sender=admin.email,
                receivers=[admin.email],
                subject=f"Client - {client[0].email} contacted you: {email_message.subject}",
                text=email_message.body
            )
       
        email_sender.send(
                sender=admin.email,
                receivers=[client[0].email],
                subject=f"Your message has succesfully reached.",
                text="Hi, Thank you for writing to us. You will be contacted shortly."
            )
        return Response({"Message": "Successfuly submitted message."}, status=status.HTTP_200_OK)
