"""POSProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from rest_framework import routers
from JohnCarAirCo import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

router = routers.DefaultRouter()
router.register(r'product_units', views.ProductUnitViewSet, basename='product-unit')
router.register(r'customer_details', views.CustomerDetailsViewSet)
router.register(r'technician_details', views.TechnicianDetailsViewSet)
router.register(r'technician_schedule', views.TechnicianScheduleViewSet)
router.register(r'services', views.ServiceTypeViewSet)
router.register(r'sales_orders', views.SalesOrderViewSet)
router.register(r'sales_order_entries', views.SalesOrderEntryViewSet)
router.register(r'supply_orders', views.SupplyOrderViewSet)
router.register(r'supply_order_entries', views.SupplyOrderEntryViewSet)
router.register(r'service_orders', views.ServiceOrderViewSet)
router.register(r'service_order_entries', views.ServiceOrderEntryViewSet)
router.register(r'aircon_types', views.AirconTypeViewSet)
router.register(r'service_order_payments', views.ServiceOrderPaymentViewSet)
router.register(r'sales_order_payments', views.SalesOrderPaymentViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('get_details/', views.UserDetailAPIView.as_view(), name="get-details"),
    path('register/', views.RegisterUserAPIView.as_view(), name="register"),
]
