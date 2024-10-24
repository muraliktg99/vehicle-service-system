from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ComponentViewSet, VehicleViewSet, IssueViewSet, PaymentViewSet, RevenueViewSet, revenue_report

# Define the router
router = DefaultRouter()
router.register(r'components', ComponentViewSet)
router.register(r'vehicles', VehicleViewSet)
router.register(r'issues', IssueViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'revenue', RevenueViewSet, basename='revenue')

# URL patterns
urlpatterns = [
    path('', include(router.urls)),
    path('revenue-report/', revenue_report),
]
