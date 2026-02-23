import requests
from django.conf import settings
from .models import Profile
from twilio.rest import Client

def send_whatsapp_broadcast(caption, image_url):
    print("\n--- STARTING REAL WHATSAPP BROADCAST ---")
    
    users = Profile.objects.exclude(mobile_number__isnull=True).exclude(mobile_number__exact='')
    
    # API Keys abhi bhi settings se lenge
    TWILIO_SID = getattr(settings, 'TWILIO_SID', '') 
    TWILIO_AUTH_TOKEN = getattr(settings, 'TWILIO_AUTH_TOKEN', '')

    if not TWILIO_SID or not TWILIO_AUTH_TOKEN:
        print("Error: Twilio API Keys not found in settings.py!")
        return 0

    try:
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    except Exception as e:
        print(f"Twilio Connection Error: {e}")
        return 0

    success_count = 0
    
    for user_profile in users:
        number = str(user_profile.mobile_number).strip()
        
        if len(number) == 10:
            number = f"+91{number}"
        if not number.startswith('+'):
            number = f"+{number}"

        print(f"Attempting to send to: {number}")

        try:
            message = client.messages.create(
                from_='whatsapp:+14155238886',  
                body=caption,
                media_url=[image_url],
                to=f'whatsapp:{number}'
            )
            
            print(f"Sent! SID: {message.sid}")
            success_count += 1
            
        except Exception as e:
            print(f"Failed to send to {number}. Reason: {e}")

    print(f"--- BROADCAST FINISHED. Total Sent: {success_count} ---\n")
    return success_count

def post_to_facebook(caption, image_relative_url):
    print(f"\n--- 🔵 STARTING FACEBOOK POST ---")
    
    # Settings se data uthayenge
    PAGE_ID = getattr(settings, 'FACEBOOK_PAGE_ID', '')
    ACCESS_TOKEN = getattr(settings, 'FACEBOOK_ACCESS_TOKEN', '')
    DOMAIN = getattr(settings, 'DOMAIN_URL', '')

    if not PAGE_ID or not ACCESS_TOKEN:
        print("❌ Error: Facebook ID or Token missing in settings.py")
        return False

    # 1. Image ka Pura Link banayenge (Ngrok + Image Path)
    # Facebook Localhost wali photo nahi dekh sakta, isliye Ngrok link chahiye
    full_image_url = f"{DOMAIN}{image_relative_url}"
    print(f"🌍 Image URL sending to Facebook: {full_image_url}")

    # 2. Facebook API URL
    post_url = f"https://graph.facebook.com/{PAGE_ID}/photos"

    # 3. Data Setup
    payload = {
        'message': caption,
        'url': full_image_url,  # Ye link Facebook download karega
        'access_token': ACCESS_TOKEN,
        'published': 'true'
    }

    try:
        # 4. Request Bhejna
        response = requests.post(post_url, data=payload)
        result = response.json()

        if 'id' in result:
            print(f"✅ Facebook Post Success! Post ID: {result['id']}")
            return True
        else:
            print(f"❌ Facebook Failed: {result}")
            return False

    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return False

# def post_to_facebook(caption, image_path):
#     print(f"--- POSTING TO FACEBOOK (Saved in DB: {image_path}) ---")
#     return True

def post_to_instagram(caption, image_path):
    print(f"--- POSTING TO INSTAGRAM ---")
    return True

def post_to_twitter(caption, image_path):
    print(f"--- POSTING TO X ---")
    return True