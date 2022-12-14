from rest_framework import viewsets, permissions, status, serializers
from rest_framework import mixins
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from ..models import Transaction, Client, Account, Address


##########################Serializer######################################
class TransactionSerializer(serializers.ModelSerializer):
    address_string = serializers.CharField(required=False)
    client = serializers.CharField(required=False)
    class Meta:
        fields = ["art", "client", "address", "address_string", "quantity", "date", "is_fulfilled"]
        model = Transaction
        
    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get("request", None)
        if request is not None:
            if request.method in permissions.SAFE_METHODS:
                fields.pop("address_string")
            else:
                fields.pop("address")
        return fields
    
    def create(self, validated_data):
        
        #getting client
        client = Client.objects.get_or_create(email=validated_data['client'])
        client = client[0]
        client.has_purchased = True
        client.save()
        
        #getting address
        address = Address.objects.get_or_create(name=validated_data["address_string"])
        
        #generating unique trans id
        import uuid
        trans_id = uuid.uuid1()
        
        validated_data.pop('client')
        validated_data.pop('address_string')
        # validated_data.pop('transaction_id')
        
        
        transaction = Transaction.objects.create(transaction_id=trans_id, client=client, address=address[0], **validated_data)
        
        #email trigger
        if transaction:
            from ..email_config import email_sender  
             # TODO: getting the admin this way is not right
            admin = Account.objects.filter(pk=1).first()  
            email_sender.send(
                    sender=admin.email,
                    receivers=[client.email],
                    subject=f"Your order has been successfuly made.",
                    text="Hi, your order has been successfully been made. You will be contacted shortly."
                )
        return transaction
################################################################


class TransactionView(mixins.CreateModelMixin,
                            mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            viewsets.GenericViewSet):
    
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    # permission_classes = [permissions.IsAuthenticated]
    
    
    @action(methods=['post'], detail=True, url_path='confirm', url_name='confirm')
    def fullfill_transaction(self, request, pk=None):
        transaction = get_object_or_404(Transaction.objects.all(), pk=pk)
        if transaction.is_fulfilled != True:
            transaction.is_fulfilled = True
            transaction.save()
            return Response({"Message": "Successfuly confirmed the transaction."}, status=status.HTTP_202_ACCEPTED)
        return Response({"Message": "Transaction was already fullfilled."}, status=status.HTTP_403_FORBIDDEN)
        
    # @action(methods=['post'], detail=True, url_path='cancel', url_name='cancel')
    # def cancel_transacation(self, request, pk=None):
    #     transaction = get_object_or_404(Transaction.objects.all(), pk=pk)
    
    """
        def list(self, request):
        pass

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass

    
    """