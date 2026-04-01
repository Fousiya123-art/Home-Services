from django.db import models
from django.contrib.auth.models import User

class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)
    imgc = models.ImageField(upload_to='ServiceCategory', null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class profile(models.Model):
    imgp = models.ImageField(upload_to='profile')
    phone = models.CharField(max_length=15)
    us = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.us)


class ServiceProvider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.user.username


class Service(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    img1 = models.ImageField(upload_to='Service', null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.title


class QuoteRequest(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    service = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, default='New')

    def __str__(self):
        return f"QuoteRequest({self.name} - {self.service or 'General'})"


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    booking_date = models.DateField()
    status = models.CharField(max_length=50, default='Pending')

    def __str__(self):
        return f"{self.user.username} - {self.service.title}"
    
class cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.service.title}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()

    def __str__(self):
        return f"{self.service.title} - {self.rating}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Contact from {self.name} - {self.subject}"

    class Meta:
        ordering = ['-created_at']
