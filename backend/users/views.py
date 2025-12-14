from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserSerializer,
    UserUpdateSerializer, ChangePasswordSerializer, ForgotPasswordSerializer,
    ResetPasswordSerializer, VerifyEmailSerializer, VerifyPasswordResetTokenSerializer
)
from .models import PasswordResetToken, EmailVerificationToken
from .utils import (
    send_verification_email, send_password_reset_email, send_welcome_email
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'login', 'forgot_password', 'reset_password', 'verify_email', 'verify_password_reset_token']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    
    def get_serializer_class(self):
        #Return appropriate serializer based on action
     
        if self.action == 'create':
            return UserRegistrationSerializer
        elif self.action == 'login':
            return UserLoginSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        elif self.action == 'change_password':
            return ChangePasswordSerializer
        elif self.action == 'forgot_password':
            return ForgotPasswordSerializer
        elif self.action == 'reset_password':
            return ResetPasswordSerializer
        elif self.action == 'verify_email':
            return VerifyEmailSerializer
        elif self.action == 'verify_password_reset_token':
            return VerifyPasswordResetTokenSerializer
        return UserSerializer
    
    def create(self, request, *args, **kwargs):
        #Register a new user
        #POST /api/v1/auth/register/
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Create email verification token
        token = EmailVerificationToken.generate_token()
        expires_at = timezone.now() + timedelta(hours=24)
        EmailVerificationToken.objects.create(
            user=user,
            token=token,
            expires_at=expires_at
        )
        
        # Build verification link
        verification_link = f"{request.build_absolute_uri('/api/v1/auth/verify-email/')}?token={token}"
        
        # Send verification email
        try:
            send_verification_email(user, verification_link)
            message = 'Registration successful! Check your email to verify your account.'
        except Exception as e:
            message = f'Registration successful! (Email sending failed: {str(e)})'
        
        return Response(
            {
                'success': True,
                'message': message,
                'data': {
                    'id': str(user.id),
                    'email': user.email,
                    'full_name': user.full_name
                }
            },
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        #Login user and return JWT tokens
        #POST /api/v1/auth/login/
        
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'success': True,
            'message': 'Login successful',
            'data': {
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }
        })
    
    @action(detail=False, methods=['post'], url_path='logout')
    def logout(self, request):
        #Logout user (blacklist refresh token)
        #POST /api/v1/auth/logout/
       
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response({
                'success': True,
                'message': 'Logout successful'
            })
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        #Get current user profile
        #GET /api/v1/auth/me/
        
        serializer = UserSerializer(request.user)
        return Response({
            'success': True,
            'data': serializer.data
        })
    
    @action(detail=False, methods=['put', 'patch'], url_path='me/update')
    def update_me(self, request):
        #Update current user profile
        #PUT/PATCH /api/v1/auth/me/update/
       
        serializer = UserUpdateSerializer(
            request.user,
            data=request.data,
            partial=request.method == 'PATCH'
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            'success': True,
            'message': 'Profile updated successfully',
            'data': UserSerializer(request.user).data
        })
    
    @action(detail=False, methods=['post'], url_path='change-password')
    def change_password(self, request):
        #Change user password
        #POST /api/v1/auth/change-password/
       
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        
        # Set new password
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        
        return Response({
            'success': True,
            'message': 'Password changed successfully'
        })
    
    @action(detail=False, methods=['post'], url_path='forgot-password')
    def forgot_password(self, request):
        #Request password reset email
        #POST /api/v1/auth/forgot-password/
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        user = User.objects.get(email=email)
        
        # Delete any existing reset tokens for this user
        PasswordResetToken.objects.filter(user=user, is_used=False).delete()
        
        # Create new reset token
        token = PasswordResetToken.generate_token()
        expires_at = timezone.now() + timedelta(hours=1)
        reset_token = PasswordResetToken.objects.create(
            user=user,
            token=token,
            expires_at=expires_at
        )
        
        # Build reset link
        reset_link = f"{request.build_absolute_uri('/api/v1/auth/reset-password/')}?token={token}"
        
        # Send email
        try:
            send_password_reset_email(user, reset_link)
            return Response({
                'success': True,
                'message': 'Password reset email sent. Check your inbox.'
            })
        except Exception as e:
            reset_token.delete()
            return Response({
                'success': False,
                'error': f'Failed to send email: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['post'], url_path='verify-password-reset-token')
    def verify_password_reset_token(self, request):
        #Verify if password reset token is valid
        #POST /api/v1/auth/verify-password-reset-token/
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        token = serializer.validated_data['token']
        
        try:
            reset_token = PasswordResetToken.objects.get(token=token)
            if reset_token.is_valid():
                return Response({
                    'success': True,
                    'message': 'Token is valid',
                    'data': {
                        'email': reset_token.user.email,
                        'expires_at': reset_token.expires_at
                    }
                })
            else:
                return Response({
                    'success': False,
                    'error': 'Token has expired or already been used'
                }, status=status.HTTP_400_BAD_REQUEST)
        except PasswordResetToken.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Invalid token'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], url_path='reset-password')
    def reset_password(self, request):
        #Reset password using token
        #POST /api/v1/auth/reset-password/
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']
        
        try:
            reset_token = PasswordResetToken.objects.get(token=token)
            
            if not reset_token.is_valid():
                return Response({
                    'success': False,
                    'error': 'Token has expired or already been used'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Update user password
            user = reset_token.user
            user.set_password(new_password)
            user.save()
            
            # Mark token as used
            reset_token.mark_as_used()
            
            return Response({
                'success': True,
                'message': 'Password reset successful. You can now login with your new password.'
            })
        except PasswordResetToken.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Invalid token'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], url_path='verify-email')
    def verify_email(self, request):
        #Verify email using token
        #POST /api/v1/auth/verify-email/
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        token = serializer.validated_data['token']
        
        try:
            verification_token = EmailVerificationToken.objects.get(token=token)
            
            if not verification_token.is_valid():
                return Response({
                    'success': False,
                    'error': 'Email verification link has expired'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Mark user as verified
            user = verification_token.user
            user.is_verified = True
            user.save(update_fields=['is_verified'])
            
            # Delete verification token
            verification_token.delete()
            
            # Send welcome email
            try:
                send_welcome_email(user)
            except Exception as e:
                print(f"Failed to send welcome email: {e}")
            
            return Response({
                'success': True,
                'message': 'Email verified successfully. You can now login.'
            })
        except EmailVerificationToken.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Invalid verification token'
            }, status=status.HTTP_400_BAD_REQUEST)