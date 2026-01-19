from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from users.models import User, Organization, OrganizationUser
from .serializers import UserSerializer, OrganizationSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny] # Allow registration

class OrganizationViewSet(viewsets.ModelViewSet):
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return organizations where the user is a member or owner
        return Organization.objects.filter(members__user=self.request.user)

    def perform_create(self, serializer):
        org = serializer.save(owner=self.request.user)
        # Add creator as Admin
        OrganizationUser.objects.create(organization=org, user=self.request.user, role='ADMIN')
