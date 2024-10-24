from rest_framework import serializers
from .models import Component, Vehicle, Issue, Payment, Revenue

# Component Serializer
class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = ['id', 'provider', 'name', 'new_price', 'repair_price', 'is_repairable']

# Vehicle Serializer
class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'model', 'company']

# Issue Serializer
class IssueSerializer(serializers.ModelSerializer):
    component_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Issue
        fields = ['id', 'vehicle', 'component_details', 'issue_description', 'issue_date']
    

    def create(self, validated_data):
        components_data = self.initial_data.get('components', [])
        issue = Issue.objects.create(
            vehicle=validated_data['vehicle'],
            issue_description=validated_data['issue_description'],
        )

        total_price = 0
        for component_data in components_data:
            component_id = component_data.get('component')
            component = Component.objects.get(id=component_id)
            issue.components.add(component)

        # Here you can handle the total price as needed, e.g., save it to the issue or create a payment record

        return issue
    def get_component_details(self, obj):
        return [
            {
                'id': component.id,
                'name': component.name,
                'new_price': component.new_price,
                'repair_price': component.repair_price
            }
            for component in obj.components.all()
        ]
# Payment Serializer
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'issue', 'amount', 'paid_on']

# Revenue Serializer
class RevenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Revenue
        fields = ['date', 'daily_revenue']


class MonthlyRevenueSerializer(serializers.Serializer):
    month = serializers.CharField()
    monthly_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)


class YearlyRevenueSerializer(serializers.Serializer):
    year = serializers.CharField()
    yearly_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)

