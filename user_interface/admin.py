from django.contrib import admin
from .models import UserActivity, ContactQuery, Profile, SocialPost
# from .models import products

@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_mobile', 'ip_address', 'login_time', 'action')
    list_filter = ('action', 'login_time')
    search_fields = ('user__username', 'ip_address', 'user__first_name', 'user__profile__mobile_number')
    readonly_fields = ('user', 'ip_address', 'login_time', 'action')
    ordering = ('-login_time',)

    def get_mobile(self, obj):
        try:
            return obj.user.profile.mobile_number
        except Exception:
            return "-"
    
    get_mobile.short_description = 'Mobile Number'

@admin.register(ContactQuery)
class ContactQueryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')
    list_filter = ('created_at',)

# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('name', 'category', 'price', 'is_available')
#     list_filter = ('category', 'is_available')
#     search_fields = ('name',)

admin.site.register(Profile)
admin.site.register(SocialPost)