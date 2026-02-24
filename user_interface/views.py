from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.files.storage import FileSystemStorage
from .models import UserActivity, Profile, ContactQuery, SocialPost
from .social_utils import send_whatsapp_broadcast, post_to_facebook, post_to_instagram, post_to_twitter


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def login_registration(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == "POST":
        user_ip = get_client_ip(request)

        if 'register_submit' in request.POST:
            full_name = request.POST.get('full_name')
            email = request.POST.get('email')
            mobile = request.POST.get('mobile') 
            password = request.POST.get('password')
            
            if User.objects.filter(username=email).exists():
                messages.error(request, "Email ID already registered! Please Login.")
            else:
                try:
                    user = User.objects.create_user(username=email, email=email, password=password)
                    user.first_name = full_name
                    user.save()

                    Profile.objects.create(user=user, mobile_number=mobile)

                    UserActivity.objects.create(user=user, ip_address=user_ip, action="Registration")

                    messages.success(request, "Account created successfully! Please Login.")
                except Exception as e:
                    messages.error(request, "Something went wrong during registration.")

        elif 'login_submit' in request.POST:
            email = request.POST.get('email')
            password = request.POST.get('password')
            
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                login(request, user)
                
                UserActivity.objects.create(user=user, ip_address=user_ip, action="Login")
                
                messages.success(request, f"Welcome back, {user.first_name}!")
                return redirect('index') 
            else:
                messages.error(request, "Invalid email or password.")
                
    return render(request, 'login_registration.html')

def index(request):
    return render(request, 'index.html')

def flavors(request):
    return render(request, 'flavours.html')

def about(request):
    return render(request, 'about.html')

def service(request):
    return render(request, 'service.html')

def contact_us(request):
    return render(request, 'contact_us.html')

def products(request):
    return render(request, 'products.html')

def post_content(request):
    return render(request, 'post_content.html')

def user_logout(request):
    logout(request)
    return redirect('index')

def post_content(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        messages.error(request, "Unauthorized Access!")
        return redirect('index')

    if request.method == "POST":
        caption = request.POST.get('caption')
        image = request.FILES.get('image')
        selected_platforms = request.POST.getlist('platforms')

        if not image or not selected_platforms:
            messages.error(request, "Please upload image and select platforms!")
            return redirect('post_content')

        try:
            # --- 1. PEHLE DATABASE MEIN SAVE KAREIN ---
            # Ye line image ko media/social_posts folder mein save karegi aur entry DB mein banayegi
            new_post = SocialPost.objects.create(
                caption=caption,
                image=image,
                platform_shared=", ".join(selected_platforms)
            )
            
            # Image ka URL nikalo jo DB mein save hua hai
            # Note: request.build_absolute_uri se pura link (http://...) banta hai jo WhatsApp ko chahiye
            file_url = request.build_absolute_uri(new_post.image.url)
            file_path = new_post.image.path # Local path for FB

            success_msg = []

            # --- 2. AB SOCIAL MEDIA PAR BHEJEIN (Real Call) ---
            
            # WhatsApp
            if 'whatsapp' in selected_platforms:
                count = send_whatsapp_broadcast(caption, file_url)
                success_msg.append(f"WhatsApp ({count} Users)")

            # Facebook (Abhi bhi Simulation rahega jab tak FB API key na ho)
            if 'facebook' in selected_platforms:
                # Dhyan dein: Hum 'file_url' bhej rahe hain (jo /media/image.jpg hai)
                post_to_facebook(caption, file_url) 
                success_msg.append("Facebook")

            messages.success(request, f"Saved to Database & Sent to: {', '.join(success_msg)}")

        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

        return redirect('post_content')

    return render(request, 'post_content.html')

# def post_content(request):
#     # 1. Security Check: Sirf Superuser (Admin) hi access kar sake
#     if not request.user.is_authenticated or not request.user.is_superuser:
#         messages.error(request, "Unauthorized Access! Only Admins can post.")
#         return redirect('index')

#     if request.method == "POST":
#         # 2. Data Fetch Karein
#         caption = request.POST.get('caption')
#         image = request.FILES.get('image')
#         selected_platforms = request.POST.getlist('platforms') # List: ['facebook', 'whatsapp', etc.]

#         # Validation
#         if not image or not selected_platforms:
#             messages.error(request, "Please upload an image and select at least one platform!")
#             return redirect('post_content')

#         # 3. Image Save Logic
#         fs = FileSystemStorage()
#         filename = fs.save(image.name, image)
        
#         # Path for FB/Insta/Twitter (Upload ke liye)
#         file_path = fs.path(filename) 
        
#         # URL for WhatsApp (Twilio ko link chahiye hota hai)
#         # Note: 'build_absolute_uri' pura link banata hai (http://127.0.0.1:8000/media/...)
#         file_url = request.build_absolute_uri(fs.url(filename))

#         # 4. Platform Action Logic (Using social_utils)
#         success_msg = []
        
#         try:
#             # --- WHATSAPP BROADCAST ---
#             if 'whatsapp' in selected_platforms:
#                 # Database logic ab social_utils.py ke andar hai
#                 count = send_whatsapp_broadcast(caption, file_url)
#                 if count > 0:
#                     success_msg.append(f"WhatsApp ({count} Users)")
#                 else:
#                     success_msg.append("WhatsApp (0 Users found)")

#             # --- FACEBOOK ---
#             if 'facebook' in selected_platforms:
#                 post_to_facebook(caption, file_path)
#                 success_msg.append("Facebook")

#             # --- INSTAGRAM ---
#             if 'instagram' in selected_platforms:
#                 post_to_instagram(caption, file_path)
#                 success_msg.append("Instagram")

#             # --- X (TWITTER) ---
#             if 'twitter' in selected_platforms:
#                 post_to_twitter(caption, file_path)
#                 success_msg.append("X (Twitter)")

#             # 5. Success Message Show karo
#             platforms_str = ", ".join(success_msg)
#             messages.success(request, f"Campaign Launched Successfully on: {platforms_str}!")

#         except Exception as e:
#             messages.error(request, f"Error processing request: {str(e)}")

#         return redirect('post_content')

#     return render(request, 'post_content.html')

def contact_us(request):
    if request.method == "POST":
        # HTML form se data nikalna (using name attributes)
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Data Database mein save karna
        try:
            ContactQuery.objects.create(
                name=name,
                email=email,
                mobile_number=mobile_number,
                subject=subject,
                message=message
            )
            # Success Message
            messages.success(request, "Thank you! Your message has been sent successfully.")
            return redirect('contact_us')
            
        except Exception as e:
            messages.error(request, "Something went wrong. Please try again.")

    return render(request, 'contact_us.html')


from django.http import HttpResponse
from django.contrib.auth import get_user_model

def create_admin(request):
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@gmail.com',
            password='12345678'
        )
        return HttpResponse("Superuser created")
    return HttpResponse("Superuser already exists")
