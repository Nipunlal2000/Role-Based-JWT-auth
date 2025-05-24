from django.shortcuts import render
from rest_framework.views import APIView,Response
from rest_framework import generics, status, filters
from rest_framework.permissions import AllowAny
from . serializers import *
from . utils import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .permissions import *
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            # Save the user but don't activate
            user = serializer.save(is_active=False)

            # Generate a 6-digit OTP
            otp = random.randint(100000, 999999)
            user.otp = str(otp)
            user.save()

            # Send the OTP to the email
            send_otp_email(user.email, otp)

            return Response(
                {"message": "Registration successful. OTP sent to your email. Please verify to activate your account."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 
    
class LoginView(generics.GenericAPIView):
    serializer_class = ProfileLoginSerializer
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)

        if user is None:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            return Response({'detail': 'User account is not active'}, status=status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'email': user.email,
                'role': user.role,
            }
        }, status=status.HTTP_200_OK)
    

class OTPVerificationView(APIView):
    permission_classes = (AllowAny, )
    
    
    def post(self, request):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            user.is_active = True
            user.is_email_verified = True
            user.otp = None  # Optional: clear OTP after verification
            user.save()
            return Response({"message": "User verified and activated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    



# 🟡 Role-Specific Profile Views -------------------------------------------------------------------------------------------------------------
  
    
class ManagerDetailView(APIView):
    permission_classes = [IsSuperAdmin | IsAdmin | IsManager]

    def get(self, request, manager_id=None):
        if request.user.role == 'MANAGER':
            try:
                manager = Manager.objects.get(user=request.user)
            except Manager.DoesNotExist:
                return Response({'detail': 'Manager profile not found.'}, status=404)
        else:
            if not manager_id:
                return Response({'detail': 'manager_id is required for this role.'}, status=400)
            try:
                manager = Manager.objects.get(user__id=manager_id)
            except Manager.DoesNotExist:
                return Response({'detail': 'Manager not found.'}, status=404)

        serializer = ManagerSerializer(manager)
        return Response(serializer.data, status=200)

    def patch(self, request, manager_id=None):
        if request.user.role == 'MANAGER':
            try:
                manager = Manager.objects.get(user=request.user)
            except Manager.DoesNotExist:
                return Response({'detail': 'Manager profile not found.'}, status=404)
        else:
            if not manager_id:
                return Response({'detail': 'manager_id is required for this role.'}, status=400)
            try:
                manager = Manager.objects.get(user__id=manager_id)
            except Manager.DoesNotExist:
                return Response({'detail': 'Manager not found.'}, status=404)

        serializer = ManagerSerializer(manager, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    
class MemberDetailView(APIView):
    permission_classes = [IsSuperAdmin | IsAdmin | IsManager | IsMember]
    
    def get(self, request, member_id=None):
        # Member accessing their own profile
        
        if request.user.role == 'MEMBER':
            
            try:
                member = Member.objects.get(user=request.user)
            except Member.DoesNotExist:
                return Response({'detail': 'Member profile not found.'}, status=404)
            
        # Others can fetch any member's profile using ID    
        
        else:            
            if not member_id:
                return Response({'detail': 'member_id is required for this role.'}, status=400)
            try:
                member = Member.objects.get(user__id=member_id)
            except Member.DoesNotExist:
                return Response({'detail': 'Member not found.'}, status=404)

        serializer = MemberSerializer(member)
        return Response(serializer.data, status=200)
    
    def patch(self, request, member_id=None):
        if request.user.role == 'MEMBER':
            try:
                member = Member.objects.get(user=request.user)
            except Member.DoesNotExist:
                return Response({'detail': 'Member profile not found.'}, status=404)
        else:
            if not member_id:
                return Response({'detail': 'member_id is required for this role.'}, status=400)
            try:
                member = Member.objects.get(user__id=member_id)
            except Member.DoesNotExist:
                return Response({'detail': 'Member not found.'}, status=404)

        serializer = MemberSerializer(member, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    
        
class AdminDetailView(APIView):

    def get(self, request):
        try:
            admin = Admin.objects.get(user=request.user)
        except Admin.DoesNotExist:
            return Response({'detail': 'Admin profile not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AdminSerializer(admin)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        try:
            admin = Admin.objects.get(user=request.user)
        except Admin.DoesNotExist:
            return Response({'detail': 'Admin profile not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AdminSerializer(admin, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SuperAdminDetailView(APIView):

    def get(self, request):
        try:
            superadmin = SuperAdmin.objects.get(user=request.user)
        except SuperAdmin.DoesNotExist:
            return Response({'detail': 'SuperAdmin profile not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = SuperAdminSerializer(superadmin)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        try:
            superadmin = SuperAdmin.objects.get(user=request.user)
        except SuperAdmin.DoesNotExist:
            return Response({'detail': 'SuperAdmin profile not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = SuperAdminSerializer(superadmin, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# 🟡 SuperAdmin Access Views -------------------------------------------------------------------------------------------------------------

class UserListView(APIView):
    permission_classes = [IsSuperAdmin]

    def get(self, request):
        users = Profile.objects.all()
        serializer = SuperAdminUserSerializer(users, many=True)
        return Response(serializer.data)

# Search and Filter

class ProfileListView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [ IsSuperAdmin]  # Optional restriction
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['email']  # Allow searching by email
    filterset_fields = ['role', 'is_active']

# Retrieve, Update, Delete a single user

class UserDetailView(APIView):
    permission_classes = [IsSuperAdmin]

    def get_object(self, pk):
        return get_object_or_404(Profile, pk=pk)

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = SuperAdminUserSerializer(user)
        return Response(serializer.data)

    def patch(self, request, pk):
        user = self.get_object(pk)
        if user.role == 'SUPERADMIN' and user != request.user:
            return Response({'detail': 'You cannot update another SuperAdmin.'}, status=403)
        serializer = SuperAdminUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        user = self.get_object(pk)
        if user.role == 'SUPERADMIN':
            return Response({'detail': 'Cannot delete a SuperAdmin.'}, status=403)
        user.delete()
        return Response({'detail': 'User deleted successfully.'}, status=204)