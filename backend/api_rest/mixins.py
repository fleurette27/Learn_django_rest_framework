from rest_framework import permissions
from .permissions import IsStaffPermission

class StaffEditorPermissionMixins():
    permission_classes=[permissions.IsAdminUser,IsStaffPermission]

class UserQuerrySetMixin():
    user_field = 'owner'
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        query_data = {} # {'user':'admin'} --> qs.filter(user=admin)
        query_data[self.user_field] = self.request.user
        return qs.filter(**query_data) 
