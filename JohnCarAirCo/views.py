from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from JohnCarAirCo.models import (
    AirconType,
    ProductUnit,
    CustomerDetails,
    TechnicianDetails,
    ServiceType,
    SalesOrder,
    SalesOrderEntry,
    ServiceOrder,
    ServiceOrderEntry,
    SalesOrderPayment,
    ServiceOrderPayment,
    TechnicianSchedule,
)
from JohnCarAirCo.serializers import (
    AirconTypeSerializer,
    UserSerializer,
    RegisterSerializer,
    GroupSerializer,
    ProductUnitSerializer,
    CustomerDetailsSerializer,
    TechnicianScheduleSerializer,
    TechnicianDetailsSerializer,
    ServiceTypeSerializer,
    SalesOrderSerializer,
    SalesOrderEntrySerializer,
    ServiceOrderSerializer,
    ServiceOrderEntrySerializer,
    SalesOrderPaymentSerializer,
    ServiceOrderPaymentSerializer,
)
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import generics

class UserDetailAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

#Class based view to register user
class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class ProductUnitViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    serializer_class = ProductUnitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = ProductUnit.objects.all()
        available_only = self.request.query_params.get('available_only')
        if available_only:
            queryset = queryset.filter(unit_stock__gt=0)
        return queryset

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class CustomerDetailsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = CustomerDetails.objects.all()
    serializer_class = CustomerDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
class TechnicianScheduleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = TechnicianSchedule.objects.all()
    serializer_class = TechnicianScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class TechnicianDetailsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = TechnicianDetails.objects.all()
    serializer_class = TechnicianDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class ServiceTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class AirconTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = AirconType.objects.all()
    serializer_class = AirconTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class SalesOrderEntryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = SalesOrderEntry.objects.all()
    serializer_class = SalesOrderEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # subtract price to sales order total
        sales_order_entry = self.get_object()
        sales_order = SalesOrder.objects.get(id=sales_order_entry.order.id)

        sales_order.total_price -= sales_order_entry.quantity * sales_order_entry.product.unit_price
        sales_order.save()

        # increment product units
        product = ProductUnit.objects.get(id=sales_order_entry.product.id)
        product.unit_stock += sales_order_entry.quantity
        product.save()

        sales_order_entry.delete()

        return Response(request.data, status=200)

class SalesOrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = SalesOrder.objects.all()
    serializer_class = SalesOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class ServiceOrderEntryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = ServiceOrderEntry.objects.all()
    serializer_class = ServiceOrderEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # subtract price to sales order total
        service_order_entry = self.get_object()
        service_order = ServiceOrder.objects.get(id=service_order_entry.order.id)
        
        service_order.total_price -= service_order_entry.quantity * service_order_entry.service.service_cost
        service_order.save()

        service_order_entry.delete()

        return Response(request.data, status=200)

class ServiceOrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = ServiceOrder.objects.all()
    serializer_class = ServiceOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
class SalesOrderPaymentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = SalesOrderPayment.objects.all()
    serializer_class = SalesOrderPaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class ServiceOrderPaymentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = ServiceOrderPayment.objects.all()
    serializer_class = ServiceOrderPaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)