"""
Donation email utilities
"""
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import strip_tags


def send_donation_confirmation_email(donation):
    """
    Send donation confirmation email
    
    Args:
        donation: Donation object
    """
    subject = 'Thank you for your donation!'
    
    donor_email = donation.donor.email if donation.donor else donation.donor_email
    donor_name = (
        donation.donor.full_name if donation.donor 
        else donation.donor_name or 'Generous Donor'
    )
    
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #10B981; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0; }}
            .content {{ background-color: #f9fafb; padding: 30px; border-radius: 0 0 5px 5px; }}
            .donation-details {{ background-color: white; padding: 20px; margin: 20px 0; border-radius: 5px; border: 2px solid #10B981; }}
            .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
            .amount {{ font-size: 32px; color: #10B981; font-weight: bold; text-align: center; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>❤️ Thank You for Your Donation!</h1>
            </div>
            <div class="content">
                <h2>Dear {donor_name},</h2>
                <p>We are incredibly grateful for your generous donation to Adopt Me!</p>
                
                <div class="amount">{donation.currency} {donation.amount}</div>
                
                <div class="donation-details">
                    <h3>Transaction Details:</h3>
                    <p><strong>Amount:</strong> {donation.currency} {donation.amount}</p>
                    <p><strong>Payment Method:</strong> {donation.get_payment_method_display()}</p>
                    <p><strong>Date:</strong> {donation.completed_at.strftime('%B %d, %Y at %I:%M %p') if donation.completed_at else 'Processing'}</p>
                    <p><strong>Transaction ID:</strong> {donation.payment_reference or 'N/A'}</p>
                </div>
                
                {f'<p><strong>Your Message:</strong> "{donation.message}"</p>' if donation.message else ''}
                
                <p>Your contribution directly helps us:</p>
                <ul>
                    <li>Connect pets with loving families</li>
                    <li>Support animal rescue operations</li>
                    <li>Maintain our platform for the community</li>
                    <li>Spread awareness about pet adoption</li>
                </ul>
                
                <p>Every donation, no matter the size, makes a real difference in the lives of animals in need.</p>
                
                <p>With heartfelt gratitude,<br><strong>The Adopt Me Team</strong></p>
            </div>
            <div class="footer">
                <p>© 2025 Adopt Me. All rights reserved.</p>
                <p>This email serves as your donation receipt.</p>
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
            recipient_list=[donor_email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send donation confirmation: {e}")
        return False
