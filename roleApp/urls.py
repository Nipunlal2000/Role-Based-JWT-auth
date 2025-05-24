from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('members/me/', MemberDetailView.as_view(), name='member-self-detail'),
    path('members/<int:member_id>/', MemberDetailView.as_view(), name='member-detail-by-id'),
    
    path('managers/me/', ManagerDetailView.as_view(), name='manager-self-detail'),
    path('managers/<int:manager_id>/', ManagerDetailView.as_view(), name='manager-detail-by-id'),
    
    path('admin-profile/', AdminDetailView.as_view(), name='admin-profile'),
    
    path('superadmin-profile/', SuperAdminDetailView.as_view(), name='superadmin-profile'),

    path('superadmin/users/', UserListView.as_view(), name='user-list'),
    path('superadmin/profiles/', ProfileListView.as_view(), name='profile-list'),
    path('superadmin/users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),


    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('otp/', OTPVerificationView.as_view(), name='otp'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    # path('password-reset/', RequestPasswordResetView.as_view(), name='password-reset'),
    # path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]  


