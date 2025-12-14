from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from .models import User, EmailVerificationToken, PasswordResetToken


class UserCreationForm(forms.ModelForm):
    #Form for creating new users
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'full_name', 'phone_number', 'location', 'role')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    #Form for updating users
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'full_name', 'phone_number', 'location', 
                  'profile_picture', 'is_active', 'is_verified', 'is_staff', 'role')


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'full_name', 'role', 'is_verified', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'is_verified', 'role', 'date_joined')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('full_name', 'phone_number', 'location', 'profile_picture')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_verified', 'is_staff', 'is_superuser', 
                                     'groups', 'user_permissions')}),
        ('Terms', {'fields': ('terms_accepted', 'terms_accepted_at', 'terms_version')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'phone_number', 'location', 
                      'role', 'password1', 'password2'),
        }),
    )
    
    search_fields = ('email', 'full_name', 'phone_number')
    ordering = ('-date_joined',)
    filter_horizontal = ('groups', 'user_permissions',)
    readonly_fields = ('date_joined', 'last_login', 'terms_accepted_at')


@admin.register(EmailVerificationToken)
class EmailVerificationTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'expires_at', 'is_valid')
    list_filter = ('created_at', 'expires_at')
    search_fields = ('user__email', 'token')
    readonly_fields = ('token', 'created_at', 'user')
    
    fieldsets = (
        ('Token Information', {
            'fields': ('user', 'token')
        }),
        ('Validity', {
            'fields': ('created_at', 'expires_at')
        }),
    )
    
    def has_add_permission(self, request):
        return False
    
    def is_valid(self, obj):
        return obj.is_valid()
    is_valid.boolean = True
    is_valid.short_description = 'Is Valid'


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'expires_at', 'is_used', 'is_valid')
    list_filter = ('created_at', 'expires_at', 'is_used')
    search_fields = ('user__email', 'token')
    readonly_fields = ('token', 'created_at', 'user')
    
    fieldsets = (
        ('Token Information', {
            'fields': ('user', 'token')
        }),
        ('Validity', {
            'fields': ('created_at', 'expires_at', 'is_used')
        }),
    )
    
    def has_add_permission(self, request):
        return False
    
    def is_valid(self, obj):
        return obj.is_valid()
    is_valid.boolean = True
    is_valid.short_description = 'Is Valid'