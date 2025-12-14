
#Bank transfer handler

class BankTransferHandler:
    
    
    @staticmethod
    def get_bank_details():
        
        #Get bank account details for display
        #eturns: dict with bank information
        
        return {
            'bank_name': 'Nepal Bank Limited',
            'account_name': 'Adopt Me Platform',
            'account_number': '0123456789',
            'branch': 'Kathmandu Branch',
            'swift_code': 'NBLNPKKA',
        }
    
    @staticmethod
    def process_submission(donation, receipt_image):
        
        #Process bank transfer submission
        #Saves receipt and marks donation as pending manual verification
        
        # TODO: Implement receipt upload and processing
        pass