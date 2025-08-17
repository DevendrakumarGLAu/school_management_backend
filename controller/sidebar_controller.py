# controller/sidebar_controller.py
from sidebar.models import Sidebar
from role.models import Role
from fastapi import HTTPException
from django.utils import timezone

class SidebarController:

    @staticmethod
    def create_sidebar(title, path, icon=None, parent_id=None, role_ids=None, created_by=None):
        parent = None
        if parent_id:
            try:
                parent = Sidebar.objects.get(id=parent_id)
            except Sidebar.DoesNotExist:
                raise HTTPException(status_code=404, detail="Parent sidebar not found")

        sidebar = Sidebar.objects.create(
            title=title,
            path=path,
            icon=icon,
            parent=parent,
            created_by=created_by
        )

        if role_ids:
            roles = Role.objects.filter(id__in=role_ids, is_active=True)
            sidebar.roles.set(roles)

        return sidebar

    @staticmethod
    def get_sidebar(user_roles=None):
        """
        If user_roles is provided, return only sidebars for those roles
        """
        qs = Sidebar.objects.filter(is_active=True)
        if user_roles:
            qs = qs.filter(roles__id__in=user_roles).distinct()
        return qs

    @staticmethod
    def update_sidebar(sidebar_id, title=None, path=None, icon=None, parent_id=None, role_ids=None, updated_by=None):
        try:
            sidebar = Sidebar.objects.get(id=sidebar_id, is_active=True)
        except Sidebar.DoesNotExist:
            raise HTTPException(status_code=404, detail="Sidebar not found")

        if title:
            sidebar.title = title
        if path:
            sidebar.path = path
        if icon:
            sidebar.icon = icon
        if parent_id:
            try:
                parent = Sidebar.objects.get(id=parent_id)
                sidebar.parent = parent
            except Sidebar.DoesNotExist:
                raise HTTPException(status_code=404, detail="Parent sidebar not found")
        if role_ids is not None:
            roles = Role.objects.filter(id__in=role_ids, is_active=True)
            sidebar.roles.set(roles)

        sidebar.updated_by = updated_by
        sidebar.updated_at = timezone.now()
        sidebar.save()
        return sidebar

    @staticmethod
    def delete_sidebar(sidebar_id, deleted_by=None):
        try:
            sidebar = Sidebar.objects.get(id=sidebar_id, is_active=True)
        except Sidebar.DoesNotExist:
            raise HTTPException(status_code=404, detail="Sidebar not found")
        sidebar.is_active = False
        sidebar.deleted_by = deleted_by
        sidebar.deleted_at = timezone.now()
        sidebar.save()
        return sidebar
