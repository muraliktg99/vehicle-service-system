from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Sum
from .models import Component, Vehicle, Issue, Payment, Revenue
from .serializers import ComponentSerializer, VehicleSerializer, IssueSerializer, PaymentSerializer, RevenueSerializer, MonthlyRevenueSerializer, YearlyRevenueSerializer
from rest_framework.decorators import api_view
from django.db.models import Sum
from django.db.models.functions import TruncDay, TruncMonth, TruncYear

# Component ViewSet
class ComponentViewSet(viewsets.ModelViewSet):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer

# Vehicle ViewSet
class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

# Issue ViewSet
class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    def perform_create(self, serializer):
        # Save the issue first
        issue = serializer.save()

        # Parse the request data to get components and their actions
        components_data = self.request.data.get('components', [])
        total_price = 0

        for component_data in components_data:
            component_id = component_data.get('component')
            action = component_data.get('action')
            component = Component.objects.get(id=component_id)

            if action == 'new':
                total_price += component.new_price
            else:
                total_price += component.repair_price

        # Create a payment with the calculated total price
        payment = Payment.objects.create(issue=issue, amount=total_price)

        # Update the revenue calculation
        # Revenue.calculate_revenue(issue)

        return payment

# Payment ViewSet
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

# Revenue ViewSet (For Graphs)
class RevenueViewSet(viewsets.ViewSet):
    def list(self, request):
        # Get daily, monthly, yearly revenue based on request params
        time_period = request.query_params.get('period', 'daily')
        
        if time_period == 'daily':
            revenue = Revenue.objects.all()
            serializer = RevenueSerializer(revenue, many=True)

        elif time_period == 'monthly':
            revenue = Revenue.objects.extra(select={'month': 'strftime("%%Y-%%m", date)'}).values('month').annotate(monthly_revenue=Sum('daily_revenue'))
            serializer = MonthlyRevenueSerializer(revenue, many=True)

        elif time_period == 'yearly':
            revenue = Revenue.objects.extra(select={'year': 'strftime("%%Y", date)'}).values('year').annotate(yearly_revenue=Sum('daily_revenue'))
            serializer = YearlyRevenueSerializer(revenue, many=True)
        
        return Response(serializer.data)



@api_view(['GET'])
def revenue_report(request):
    daily = Payment.objects.annotate(date=TruncDay('paid_on')).values('date').annotate(total=Sum('amount')).order_by('date')
    monthly = Payment.objects.annotate(date=TruncMonth('paid_on')).values('date').annotate(total=Sum('amount')).order_by('date')
    yearly = Payment.objects.annotate(date=TruncYear('paid_on')).values('date').annotate(total=Sum('amount')).order_by('date')
    return Response({
        'daily': daily,
        'monthly': monthly,
        'yearly': yearly,
    })