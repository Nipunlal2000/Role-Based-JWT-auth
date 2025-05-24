from rest_framework import serializers
from .models import *
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate

# serializers.py



class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'email', 'role'] 

# 🟡 Role-Specific Profile Serializers -------------------------------------------------------------------------------------------------------------


class ManagerSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Manager
        fields = ['email', 'team_name', 'number_of_members']
      
        
class MemberSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Member
        fields = ['email', 'date_joined_team', 'assigned_project']
        

class AdminSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Admin
        fields = ['email', 'department', 'can_create_managers']
        

class SuperAdminSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = SuperAdmin
        fields = ['email','department']
        
        
# 🟡 User Management serializers -------------------------------------------------------------------------------------------------------------


class SuperAdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'email', 'role', 'is_active', 'is_email_verified', 'address', 'created_at']
        read_only_fields = ['created_at']


# 🟡 Authentication serializers -------------------------------------------------------------------------------------------------------------


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = Profile
        fields = ['email', 'password', 'confirm_password','address','role']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        role = validated_data.get('role')
        user = Profile.objects.create_user(**validated_data)

        # Automatically create role-specific model
        if role == 'SUPERADMIN':
            SuperAdmin.objects.create(user=user)
        elif role == 'ADMIN':
            Admin.objects.create(user=user)
        elif role == 'MANAGER':
            Manager.objects.create(user=user)
        elif role == 'MEMBER':
            Member.objects.create(user=user)

        return user
    
class ProfileLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid email or password.")
        return user


class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, attrs):
        email = attrs.get("email")
        otp = str(attrs.get("otp"))

        try:
            user = Profile.objects.get(email=email, otp=otp, is_active=False)
        except Profile.DoesNotExist:
            raise serializers.ValidationError("Invalid OTP or email, or user already verified.")
        
        attrs['user'] = user
        return attrs