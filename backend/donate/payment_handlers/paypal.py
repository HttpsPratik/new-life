
#PayPal payment gateway handler


class PayPalHandler:
    
    
    def __init__(self):
        # Will be implemented when integrating PayPal
        pass
    
    def create_order(self, donation):
        
        #Create PayPal order
        #Returns: order details
        
        # TODO: Implement PayPal order creation
        pass
    
    def capture_payment(self, order_id):
        
        #Capture PayPal payment
        #Returns: payment details
        
        # TODO: Implement PayPal payment capture
        pass
    
    def verify_payment(self, payment_data):
        
        #Verify PayPal payment
        #Returns: verification status
        
        # TODO: Implement PayPal payment verification
        pass