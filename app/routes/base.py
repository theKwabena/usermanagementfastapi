from app.models.roles import Role
from app.models.groups import Group

# Instances of Admin for the roles you want to check
admin_can_create = Role(name="admin_can_create")
admin_can_edit = Role(name="admin_can_remove")
admin_can_delete = Role(name="admin_can_delete")


admin= Group(name="admin")