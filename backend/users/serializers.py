from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta
from .models import User, PasswordResetToken, EmailVerificationToken
from .email_service import EmailService


class UserRegistrationSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        label="Confirm Password"
    )
    terms_accepted = serializers.BooleanField(required=True)
    
    class Meta:
        model = User
        fields = (
            'email', 'password', 'password2', 'full_name',
            'phone_number', 'location', 'terms_accepted'
        )
    
    def validate(self, attrs):
        #Validate passwords match and terms accepted
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password": "Password fields didn't match."
            })
        
        if not attrs.get('terms_accepted'):
            raise serializers.ValidationError({
                "terms_accepted": "You must accept the terms and conditions."
            })
        
        return attrs
    
    def create(self, validated_data):
        #Create user with validated data
        terms_accepted = validated_data.pop('terms_accepted')
        password2 = validated_data.pop('confirm password')
        
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            full_name=validated_data['full_name'],
            phone_number=validated_data.get('phone_number'),
            location=validated_data.get('location'),
            is_active=True,
            is_verified=False,  # Will be verified via email
            terms_accepted=terms_accepted,
            terms_accepted_at=timezone.now(),
            terms_version='1.0'
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    #Serializer for user login
    
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    
    def validate(self, attrs):
        #Validate credentials
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                email=email,
                password=password
            )
            
            if not user:
                raise serializers.ValidationError(
                    'Unable to log in with provided credentials.'
                )
            
            if not user.is_verified:
                raise serializers.ValidationError(
                    'Please verify your email before logging in.'
                )
            
            if not user.is_active:
                raise serializers.ValidationError(
                    'User account is disabled.'
                )
            
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError(
                'Must include "email" and "password".'
            )


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = (
            'id', 'email', 'full_name', 'phone_number', 'location',
            'profile_picture', 'role', 'is_verified', 'terms_accepted',
            'terms_accepted_at', 'terms_version', 'date_joined'
        )
        read_only_fields = (
            'id', 'email', 'role', 'is_verified', 'terms_accepted',
            'terms_accepted_at', 'terms_version', 'date_joined'
        )


class UserUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('full_name', 'phone_number', 'location', 'profile_picture')


class ChangePasswordSerializer(serializers.Serializer):
    
    
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password]
    )
    new_password2 = serializers.CharField(required=True, write_only=True)
    
    def validate(self, attrs):
        
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({
                "new_password": "Password fields didn't match."
            })
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value


class ForgotPasswordSerializer(serializers.Serializer):
    """Serializer to request password reset"""
    
    email = serializers.EmailField(required=True)
    
    def validate_email(self, value):
        """Check if user with this email exists"""
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "No user found with this email address."
            )
        return value


class VerifyPasswordResetTokenSerializer(serializers.Serializer):
    """Serializer to verify password reset token"""
    
    token = serializers.CharField(required=True)


class ResetPasswordSerializer(serializers.Serializer):
    """Serializer to reset password with token"""
    
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    new_password2 = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'},
        label="Confirm Password"
    )
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({
                "new_password": "Password fields didn't match."
            })
        
        # Verify token is valid
        token = attrs.get('token')
        try:
            reset_token = PasswordResetToken.objects.get(token=token)
            if not reset_token.is_valid():
                raise serializers.ValidationError(
                    "Password reset link has expired or already been used."
                )
        except PasswordResetToken.DoesNotExist:
            raise serializers.ValidationError("Invalid reset token.")
        
        return attrs


class VerifyEmailSerializer(serializers.Serializer):
    """Serializer to verify email with token"""
    
    token = serializers.CharField(required=True)
    
    def validate_token(self, value):
        """Verify email token is valid"""
        try:
            verification_token = EmailVerificationToken.objects.get(token=value)
            if not verification_token.is_valid():
                raise serializers.ValidationError(
                    "Email verification link has expired."
                )
        except EmailVerificationToken.DoesNotExist:
            raise serializers.ValidationError("Invalid verification token.")
        return value