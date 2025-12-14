"""
Feedback email utilities
"""
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import strip_tags


def send_feedback_confirmation_email(feedback):
    """
    Send feedback submission confirmation
    
    Args:
        feedback: Feedback object
    """
    subject = 'We received your message'
    
    email = feedback.user.email if feedback.user else feedback.email
    name = feedback.get_sender_display()
    
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #3B82F6; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0; }}
            .content {{ background-color: #f9fafb; padding: 30px; border-radius: 0 0 5px 5px; }}
            .feedback-box {{ background-color: white; padding: 20px; margin: 20px 0; border-radius: 5px; border-left: 4px solid #3B82F6; }}
            .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>✉️ Thank You for Your Feedback!</h1>
            </div>
            <div class="content">
                <h2>Hi {name},</h2>
                <p>We have received your message and appreciate you taking the time to contact us.</p>
                
                <div class="feedback-box">
                    <p><strong>Subject:</strong> {feedback.subject}</p>
                    <p><strong>Type:</strong> {feedback.get_type_display()}</p>
                    <p><strong>Submitted:</strong> {feedback.created_at.strftime('%B %d, %Y at %I:%M %p')}</p>
                </div>
                
                <p>Our team will review your message and get back to you if a response is needed.</p>
                
                <p>Your feedback helps us improve Adopt Me and serve our community better!</p>
                
                <p>Best regards,<br><strong>The Adopt Me Support Team</strong></p>
            </div>
            <div class="footer">
                <p>© 2025 Adopt Me. All rights reserved.</p>
                <p>Need urgent help? Email us at support@adoptme.com</p>
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
            recipient_list=[email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send feedback confirmation: {e}")
        return False
