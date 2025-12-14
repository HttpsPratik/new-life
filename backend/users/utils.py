"""
Email utility functions
Handles sending emails for various user actions
"""
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import strip_tags


def send_verification_email(user, verification_link):
    """
    Send email verification link to user
    
    Args:
        user: User object
        verification_link: URL for email verification
    """
    subject = 'Verify your Adopt Me account'
    
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #3B82F6; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0; }}
            .content {{ background-color: #f9fafb; padding: 30px; border-radius: 0 0 5px 5px; }}
            .button {{ display: inline-block; padding: 12px 30px; background-color: #3B82F6; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
            .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Welcome to Adopt Me!</h1>
            </div>
            <div class="content">
                <h2>Hello {user.full_name},</h2>
                <p>Thank you for registering with Adopt Me. We're excited to have you join our community!</p>
                <p>Please verify your email address by clicking the button below:</p>
                <p style="text-align: center;">
                    <a href="{verification_link}" class="button">Verify Email Address</a>
                </p>
                <p>Or copy and paste this link into your browser:</p>
                <p style="word-break: break-all; color: #3B82F6;">{verification_link}</p>
                <p>If you didn't create an account with us, please ignore this email.</p>
                <p>This link will expire in 24 hours.</p>
            </div>
            <div class="footer">
                <p>© 2025 Adopt Me. All rights reserved.</p>
                <p>Helping pets find loving homes</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send verification email: {e}")
        return False


def send_password_reset_email(user, reset_link):
    """
    Send password reset link to user
    
    Args:
        user: User object
        reset_link: URL for password reset
    """
    subject = 'Reset your Adopt Me password'
    
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #EF4444; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0; }}
            .content {{ background-color: #f9fafb; padding: 30px; border-radius: 0 0 5px 5px; }}
            .button {{ display: inline-block; padding: 12px 30px; background-color: #EF4444; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
            .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
            .warning {{ background-color: #FEF3C7; padding: 15px; border-left: 4px solid #F59E0B; margin: 15px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Password Reset Request</h1>
            </div>
            <div class="content">
                <h2>Hi {user.full_name},</h2>
                <p>We received a request to reset your password for your Adopt Me account.</p>
                <p>Click the button below to create a new password:</p>
                <p style="text-align: center;">
                    <a href="{reset_link}" class="button">Reset Password</a>
                </p>
                <p>Or copy and paste this link into your browser:</p>
                <p style="word-break: break-all; color: #EF4444;">{reset_link}</p>
                <div class="warning">
                    <strong>⚠️ Security Notice:</strong>
                    <p>If you didn't request this password reset, please ignore this email. Your password will remain unchanged.</p>
                </div>
                <p>This link will expire in 1 hour.</p>
            </div>
            <div class="footer">
                <p>© 2025 Adopt Me. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send password reset email: {e}")
        return False


def send_welcome_email(user):
    """
    Send welcome email after email verification
    
    Args:
        user: User object
    """
    subject = 'Welcome to Adopt Me!'
    
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #10B981; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0; }}
            .content {{ background-color: #f9fafb; padding: 30px; border-radius: 0 0 5px 5px; }}
            .feature-box {{ background-color: white; padding: 15px; margin: 10px 0; border-left: 4px solid #10B981; }}
            .button {{ display: inline-block; padding: 12px 30px; background-color: #10B981; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
            .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎉 Welcome to Adopt Me!</h1>
            </div>
            <div class="content">
                <h2>Hello {user.full_name},</h2>
                <p>Your email has been verified successfully! You're now part of our community.</p>
                
                <h3>What you can do now:</h3>
                
                <div class="feature-box">
                    <strong>🐕 List Pets for Adoption</strong>
                    <p>Help pets find loving homes by listing them on our platform.</p>
                </div>
                
                <div class="feature-box">
                    <strong>🔍 Report Missing Pets</strong>
                    <p>Lost your pet? Create a report to help find them quickly.</p>
                </div>
                
                <div class="feature-box">
                    <strong>❤️ Browse Available Pets</strong>
                    <p>Find your perfect companion from our listings.</p>
                </div>
                
                <div class="feature-box">
                    <strong>🏥 Find Rescue Contacts</strong>
                    <p>Access our directory of shelters and veterinarians.</p>
                </div>
                
                <p style="text-align: center;">
                    <a href="{settings.FRONTEND_URL}" class="button">Get Started</a>
                </p>
                
                <p>Thank you for joining our mission to help pets find loving homes!</p>
            </div>
            <div class="footer">
                <p>© 2025 Adopt Me. All rights reserved.</p>
                <p>Need help? Contact us at support@adoptme.com</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send welcome email: {e}")
        return False


def send_pet_listing_confirmation(user, pet):
    """
    Send confirmation email when user creates a pet listing
    
    Args:
        user: User object
        pet: Pet object
    """
    subject = 'Your pet listing is now live!'
    
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #3B82F6; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0; }}
            .content {{ background-color: #f9fafb; padding: 30px; border-radius: 0 0 5px 5px; }}
            .pet-info {{ background-color: white; padding: 20px; margin: 20px 0; border-radius: 5px; }}
            .button {{ display: inline-block; padding: 12px 30px; background-color: #3B82F6; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
            .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>✅ Listing Created Successfully!</h1>
            </div>
            <div class="content">
                <h2>Hi {user.full_name},</h2>
                <p>Your pet listing is now live on Adopt Me!</p>
                
                <div class="pet-info">
                    <h3>Listing Details:</h3>
                    <p><strong>Name:</strong> {pet.name}</p>
                    <p><strong>Category:</strong> {pet.get_category_display()}</p>
                    <p><strong>Breed:</strong> {pet.breed or 'Not specified'}</p>
                    <p><strong>Age:</strong> {pet.age} months</p>
                    <p><strong>Location:</strong> {pet.location}</p>
                </div>
                
                <p>Potential adopters can now see your listing and contact you directly.</p>
                
                <p style="text-align: center;">
                    <a href="{settings.FRONTEND_URL}/pets/{pet.id}" class="button">View Your Listing</a>
                </p>
                
                <p><strong>Tips for a successful adoption:</strong></p>
                <ul>
                    <li>Respond promptly to inquiries</li>
                    <li>Be honest about the pet's temperament and needs</li>
                    <li>Meet potential adopters in safe, public places</li>
                    <li>Ask questions to ensure a good match</li>
                </ul>
            </div>
            <div class="footer">
                <p>© 2025 Adopt Me. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send pet listing confirmation: {e}")
        return False


def send_missing_pet_confirmation(user, missing_pet):
    """
    Send confirmation email when user reports a missing pet
    
    Args:
        user: User object
        missing_pet: MissingPet object
    """
    subject = 'Your missing pet report has been posted'
    
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #F59E0B; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0; }}
            .content {{ background-color: #f9fafb; padding: 30px; border-radius: 0 0 5px 5px; }}
            .pet-info {{ background-color: white; padding: 20px; margin: 20px 0; border-radius: 5px; }}
            .button {{ display: inline-block; padding: 12px 30px; background-color: #F59E0B; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
            .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔍 Missing Pet Report Posted</h1>
            </div>
            <div class="content">
                <h2>Hi {user.full_name},</h2>
                <p>Your missing pet report is now live. We hope this helps you find your pet quickly!</p>
                
                <div class="pet-info">
                    <h3>Report Details:</h3>
                    <p><strong>Name:</strong> {missing_pet.name or 'Unknown'}</p>
                    <p><strong>Category:</strong> {missing_pet.get_category_display()}</p>
                    <p><strong>Last Seen:</strong> {missing_pet.last_seen_location}</p>
                    <p><strong>Date:</strong> {missing_pet.last_seen_date}</p>
                    {f'<p><strong>Reward:</strong> NPR {missing_pet.reward_offered}</p>' if missing_pet.reward_offered else ''}
                </div>
                
                <p style="text-align: center;">
                    <a href="{settings.FRONTEND_URL}/missing-pets/{missing_pet.id}" class="button">View Your Report</a>
                </p>
                
                <p><strong>What to do next:</strong></p>
                <ul>
                    <li>Share your report on social media</li>
                    <li>Check local shelters and veterinary clinics</li>
                    <li>Post flyers in the area where your pet was last seen</li>
                    <li>Keep your contact information up to date</li>
                </ul>
                
                <p>We're sending positive thoughts your way. Don't give up hope!</p>
            </div>
            <div class="footer">
                <p>© 2025 Adopt Me. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send missing pet confirmation: {e}")
        return False
