from django.db import models
from django.utils import timezone

# Component Model
class Component(models.Model):
    provider = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    new_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    repair_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_repairable = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

# Vehicle Model
class Vehicle(models.Model):
    model = models.CharField(max_length=100)
    company = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.model} ({self.company})'

# Issue Model
class Issue(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    components = models.ManyToManyField(Component)
    issue_description = models.TextField()
    issue_date = models.DateTimeField(default=timezone.now)

    # def get_price(self):
    #     if self.component_action == self.NEW_COMPONENT:
    #         return self.component.new_price
    #     return self.component.repair_price

    def __str__(self):
        return f'Issue for {self.vehicle.model} - {self.component.name}'

# Payment Model
class Payment(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Payment for Issue {self.issue.id} - {self.amount}'

# Revenue Tracking (for Graphs)
class Revenue(models.Model):
    date = models.DateField()
    daily_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    @classmethod
    def calculate_revenue(cls, issue):
        date = issue.issue_date.date()
        amount = sum([component.new_price if issue.component_action == issue.NEW_COMPONENT else component.repair_price for component in issue.components.all()])
        revenue, created = cls.objects.get_or_create(date=date)
        revenue.daily_revenue += amount
        revenue.save()

    def __str__(self):
        return f'{self.date} - {self.daily_revenue}'
