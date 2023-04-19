from django.contrib.auth.models import User, Group
from JohnCarAirCo.models import (
  AirconType,
  ProductUnit,
  CustomerDetails,
  TechnicianSchedule,
  TechnicianDetails,
  ServiceType,
  SalesOrder,
  SalesOrderEntry,
  ServiceOrder,
  ServiceOrderEntry,
  SupplyOrder,
  SupplyOrderEntry,
  SalesOrderPayment,
  ServiceOrderPayment,
)
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ["id", "first_name", "last_name", "username"]

#Serializer to Register User
class RegisterSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(
    required=True,
    validators=[UniqueValidator(queryset=User.objects.all())]
  )
  password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
  password2 = serializers.CharField(write_only=True, required=True)

  class Meta:
    model = User
    fields = ('username', 'password', 'password2',
         'email', 'first_name', 'last_name')
    extra_kwargs = {
      'first_name': {'required': True},
      'last_name': {'required': True}
    }

  def validate(self, attrs):
    if attrs['password'] != attrs['password2']:
      raise serializers.ValidationError({"password": "Password fields didn't match."})
    return attrs

  def create(self, validated_data):
    user = User.objects.create(
      username=validated_data['username'],
      email=validated_data['email'],
      first_name=validated_data['first_name'],
      last_name=validated_data['last_name']
    )
    user.set_password(validated_data['password'])
    user.save()
    return user

class GroupSerializer(serializers.ModelSerializer):
  class Meta:
    model = Group
    fields = ['url', 'name']

class ProductUnitSerializer(serializers.ModelSerializer):

  unit_type = serializers.StringRelatedField(many=False)
  unit_type_id = serializers.PrimaryKeyRelatedField(
    queryset=AirconType.objects.all(),
    source='unit_type',
  )

  class Meta:
    model = ProductUnit
    fields = [
      'id',
      'unit_name',
      'unit_price',
      'unit_stock',
      'unit_type',
      'unit_type_id'
    ]

class CustomerDetailsSerializer(serializers.ModelSerializer):
  class Meta:
    model = CustomerDetails
    fields = [
      'id',
      'customer_name',
      'customer_contact',
      'customer_email',
      'customer_address'
    ]

class TechnicianScheduleSerializer(serializers.ModelSerializer):

  technician = serializers.StringRelatedField(many=False)
  technician_id = serializers.PrimaryKeyRelatedField(
    queryset=TechnicianDetails.objects.all(),
    source='technician',
  )

  class Meta:
    model = TechnicianSchedule
    fields = [
      'id',
      'technician',
      'technician_id',
      'tech_sched_day',
      'tech_sched_time_start',
      'tech_sched_time_end',
      'tech_sched_status'
    ]

class TechnicianDetailsSerializer(serializers.ModelSerializer):

  tech_scheds = TechnicianScheduleSerializer(many=True, read_only=True)

  class Meta:
    model = TechnicianDetails
    fields = [
      'id',
      'tech_name',
      'tech_phone',
      'tech_email',
      'tech_scheds'
    ]

class ServiceTypeSerializer(serializers.ModelSerializer):
  class Meta:
    model = ServiceType
    fields = [
      'service_name',
      'service_cost'
    ]

class AirconTypeSerializer(serializers.ModelSerializer):
  class Meta:
    model = AirconType
    fields = [
      'type_name',
    ]

class SupplyOrderEntrySerializer(serializers.ModelSerializer):
  product = serializers.StringRelatedField(many=False)
  product_id = serializers.PrimaryKeyRelatedField(
    queryset=ProductUnit.objects.all(),
    source='product',
  )

  order = serializers.StringRelatedField(many=False)
  order_id = serializers.PrimaryKeyRelatedField(
    queryset=SupplyOrder.objects.all(),
    source='order',
  )

  class Meta:
    model = SupplyOrderEntry
    fields = [
      'id',
      'product',
      'product_id',
      'order',
      'order_id',
      'quantity',
    ]

  # add price to sales order total price
  def create(self, validated_data):
    product_unit = validated_data['product']
    quantity = validated_data['quantity']

    # increment stock
    product_unit.unit_stock += quantity
    product_unit.save()

    return SupplyOrderEntry.objects.create(**validated_data)

  def update(self, instance, validated_data):
    product_unit = validated_data.get('product', instance.product)
    quantity = validated_data.get('quantity', instance.quantity)

    # update stock
    product_unit.unit_stock -= instance.quantity
    product_unit.unit_stock += quantity
    product_unit.save()

    instance.product = product_unit
    instance.quantity = quantity
    instance.save()

    return instance


class SupplyOrderSerializer(serializers.ModelSerializer):
  entries = SupplyOrderEntrySerializer(many=True, read_only=True)

  class Meta:
    model = SupplyOrder
    fields = [
      'id',
      'date_ordered',
      'entries',
    ]

class SalesOrderEntrySerializer(serializers.ModelSerializer):
  product = serializers.StringRelatedField(many=False)
  product_id = serializers.PrimaryKeyRelatedField(
    queryset=ProductUnit.objects.all(),
    source='product',
  )

  order = serializers.StringRelatedField(many=False)
  order_id = serializers.PrimaryKeyRelatedField(
    queryset=SalesOrder.objects.all(),
    source='order',
  )

  entry_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

  class Meta:
    model = SalesOrderEntry
    fields = [
      'id',
      'product',
      'product_id',
      'order',
      'order_id',
      'quantity',
      'entry_price'
    ]

  # add price to sales order total price
  def create(self, validated_data):
    product_unit = validated_data['product']
    quantity = validated_data['quantity']

    # check if stock is sufficient
    if product_unit.unit_stock < quantity:
        raise serializers.ValidationError('Insufficient stock.')

    validated_data['entry_price'] = product_unit.unit_price * quantity

    # update sales order total price
    order = validated_data['order']
    order.total_price += validated_data['entry_price']
    order.save()

    # decrement stock
    product_unit.unit_stock -= quantity
    product_unit.save()

    return SalesOrderEntry.objects.create(**validated_data)

  def update(self, instance, validated_data):
    product_unit = validated_data.get('product', instance.product)
    quantity = validated_data.get('quantity', instance.quantity)

    # check if stock is sufficient
    if product_unit.unit_stock + instance.quantity < quantity:
        raise serializers.ValidationError('Insufficient stock.')

    # update sales order total price
    order = validated_data['order']
    order.total_price -= instance.entry_price
    order.total_price += product_unit.unit_price * quantity
    order.save()

    # update stock
    product_unit.unit_stock += instance.quantity
    product_unit.unit_stock -= quantity
    product_unit.save()

    instance.product = product_unit
    instance.quantity = quantity
    instance.entry_price = product_unit.unit_price * quantity
    instance.save()

    return instance


class SalesOrderSerializer(serializers.ModelSerializer):
  customer = serializers.StringRelatedField(many=False)
  customer_id = serializers.PrimaryKeyRelatedField(
    queryset=CustomerDetails.objects.all(),
    source='customer',
  )

  entries = SalesOrderEntrySerializer(many=True, read_only=True)

  total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

  class Meta:
    model = SalesOrder
    fields = [
      'id',
      'customer',
      'customer_id',
      'date_ordered',
      'total_price',
      'entries',
      'status',
      'total_price'
    ]

class ServiceTypeSerializer(serializers.ModelSerializer):
  class Meta:
    model = ServiceType
    fields = [
      'id',
      'service_name',
      'service_cost'
    ]

class ServiceOrderEntrySerializer(serializers.ModelSerializer):
  service = serializers.StringRelatedField(many=False)
  service_id = serializers.PrimaryKeyRelatedField(
    queryset=ServiceType.objects.all(),
    source='service',
  )

  order = serializers.StringRelatedField(many=False)
  order_id = serializers.PrimaryKeyRelatedField(
    queryset=ServiceOrder.objects.all(),
    source='order',
  )

  entry_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

  class Meta:
    model = ServiceOrderEntry
    fields = [
      'id',
      'service',
      'service_id',
      'order',
      'order_id',
      'quantity',
      'entry_price',
    ]

  # add price to sales order total price
  def create(self, validated_data):
    service = validated_data['service']
    quantity = validated_data['quantity']

    validated_data['entry_price'] = service.service_cost * quantity

    # update service order total price
    order = validated_data['order']
    order.total_price += validated_data['entry_price']
    order.save()

    return ServiceOrderEntry.objects.create(**validated_data)
  
  def update(self, instance, validated_data):
    service = validated_data.get('service', instance.service)
    quantity = validated_data.get('quantity', instance.quantity)

    # update service order total price
    order = validated_data['order']
    order.total_price -= instance.entry_price
    order.total_price += service.service_cost * quantity
    order.save()

    instance.service = service
    instance.quantity = quantity
    instance.entry_price = service.service_cost * quantity
    instance.save()

    return instance

class ServiceOrderSerializer(serializers.ModelSerializer):
  customer = serializers.StringRelatedField(many=False)
  customer_id = serializers.PrimaryKeyRelatedField(
    queryset=CustomerDetails.objects.all(),
    source='customer',
  )

  technician = serializers.StringRelatedField(many=False)
  technician_id = serializers.PrimaryKeyRelatedField(
    queryset=TechnicianDetails.objects.all(),
    source='technician',
  )

  entries = ServiceOrderEntrySerializer(many=True, read_only=True)

  service_date = serializers.DateField(format="%Y-%m-%d")

  total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

  class Meta:
    model = ServiceOrder
    fields = [
      'id',
      'customer',
      'customer_id',
      'date_ordered',
      'entries',
      'status',
      'technician',
      'technician_id',
      'service_date',
      'total_price',
    ]
  
  def validate(self, data):
    service_date = data['service_date']
    schedules = TechnicianSchedule.objects.filter(tech_sched_day=service_date.weekday() + 1, technician=data['technician'].id, tech_sched_status=True)
    for schedule in schedules:
      if schedule.tech_sched_status:
        return data
    raise ValidationError("Selected technician is not available on the service date.")

class SalesOrderPaymentSerializer(serializers.ModelSerializer):
  order = serializers.StringRelatedField(many=False)
  order_id = serializers.PrimaryKeyRelatedField(
    queryset=SalesOrder.objects.all(),
    source='order',
  )

  class Meta:
    model = SalesOrderPayment
    fields = [
      'id',
      'order',
      'order_id',
      'amount_paid',
      'date_paid',
      'cc_number',
      'cc_name',
      'cc_expiry',
      'cc_cvv',
    ]

class ServiceOrderPaymentSerializer(serializers.ModelSerializer):
  order = serializers.StringRelatedField(many=False)
  order_id = serializers.PrimaryKeyRelatedField(
    queryset=ServiceOrder.objects.all(),
    source='order',
  )

  class Meta:
    model = ServiceOrderPayment
    fields = [
      'id',
      'order',
      'order_id',
      'amount_paid',
      'date_paid',
      'cc_number',
      'cc_name',
      'cc_expiry',
      'cc_cvv',
    ]