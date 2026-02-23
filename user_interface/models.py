from django.db import models
from django.contrib.auth.models import User

class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    login_time = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username} - {self.action} at {self.login_time}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class ContactQuery(models.Model):
    name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.name} - {self.subject}"

# prodct page ko dynamic bnane ke liye
# class Product(models.Model):
#     CATEGORY_CHOICES = (
#         ('Dark', 'Dark Chocolate'),
#         ('White', 'White Chocolate'),
#         ('Milky', 'Milky Chocolate'),
#         ('Fruit', 'Fruit Nut'),
#     )

# models.py ke end mein add karein

class SocialPost(models.Model):
    caption = models.TextField()
    image = models.ImageField(upload_to='social_posts/')
    created_at = models.DateTimeField(auto_now_add=True)
    platform_shared = models.CharField(max_length=200) # Store karega kahan share hua (e.g. "WhatsApp, Facebook")

    def __str__(self):
        return f"Post on {self.created_at.strftime('%Y-%m-%d')} - {self.caption[:20]}..."







#     name = models.CharField(max_length=100)
#     category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
#     price = models.DecimalField(max_digits=6, decimal_places=2) # Example: 499.00
#     description = models.TextField()
#     image = models.ImageField(upload_to='products/') # Photos 'media/products' mein jayengi
#     is_available = models.BooleanField(default=True) # Agar stock khatam ho jaye to hide kar sakein

#     def __str__(self):
#         return self.name