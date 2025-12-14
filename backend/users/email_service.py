"""Email service for sending verification and password reset emails"""

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class EmailService:
    """Service to handle all email operations"""
    
    @staticmethod
    def send_verification_email(user, token):
        """Send email verification link to user"""
        
        verification_link = f"{settings.FRONTEND_URL}/verify-email?token={token}"
        
        context = {
            'user': user,
            'verification_link': verification_link,
            'frontend_url': settings.FRONTEND_URL,
        }
        
        subject = 'Verify Your Email - Adopt Me'
        html_message = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">
                    <h2>Welcome to Adopt Me, {user.full_name}!</h2>
                    
                    <p>Thank you for signing up. Please verify your email address by clicking the link below:</p>
                    
                    <div style="margin: 30px 0;">
                        <a href="{verification_link}" 
                           style="display: inline-block; padding: 12px 30px; background-color: #007bff; color: white; text-decoration: none; border-radius: 5px;">
                            Verify Email
                        </a>
                    </div>
                    
                    <p style="color: #666; font-size: 12px;">
                        Or copy and paste this link in your browser:<br>
                        {verification_link}
                    </p>
                    
                    <p style="color: #999; font-size: 12px; margin-top: 30px;">
                        This link will expire in 24 hours.
                    </p>
                    
                    <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                    
                    <p style="color: #999; font-size: 11px;">
                        Adopt Me Platform | Help animals find loving homes
                    </p>
                </div>
            </body>
        </html>
        """
        
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
    
    @staticmethod
    def send_password_reset_email(user, token):
        """Send password reset link to user"""
        
        reset_link = f"{settings.FRONTEND_URL}/reset-password?token={token}"
        
        context = {
            'user': user,
            'reset_link': reset_link,
            'frontend_url': settings.FRONTEND_URL,
        }
        
        subject = 'Reset Your Password - Adopt Me'
        html_message = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">
                    <h2>Password Reset Request</h2>
                    
                    <p>Hi {user.full_name},</p>
                    
                    <p>We received a request to reset your password. Click the link below to set a new password:</p>
                    
                    <div style="margin: 30px 0;">
                        <a href="{reset_link}" 
                           style="display: inline-block; padding: 12px 30px; background-color: #28a745; color: white; text-decoration: none; border-radius: 5px;">
                            Reset Password
                        </a>
                    </div>
                    
                    <p style="color: #666; font-size: 12px;">
                        Or copy and paste this link in your browser:<br>
                        {reset_link}
                    </p>
                    
                    <p style="color: #d32f2f; font-weight: bold; margin-top: 20px;">
                        ⚠️ If you did not request a password reset, please ignore this email.
                    </p>
                    
                    <p style="color: #999; font-size: 12px; margin-top: 30px;">
                        This link will expire in 1 hour.
                    </p>
                    
                    <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                    
                    <p style="color: #999; font-size: 11px;">
                        Adopt Me Platform | Help animals find loving homes
                    </p>
                </div>
            </body>
        </html>
        """
        
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
