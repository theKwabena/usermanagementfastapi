from app.models.roles import Role
from app.models.groups import Group

# Instances of Admin for the roles you want to check
admin_create = Role(name="admin_create_users")
admin_edit = Role(name="admin_edit_users")
admin_delete = Role(name="admin_delete_users")

admin= Group(name="admin")

admin.roles.extend([admin_create, admin_edit, admin_delete])