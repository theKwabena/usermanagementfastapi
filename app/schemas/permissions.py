from pydantic import BaseModel, constr


class Group(BaseModel):
    name: constr(min_length=2)


class GroupCreate(Group):
    pass


class Role(BaseModel):
    name: constr(min_length=2)


class RoleCreate(Role):
    pass


class RoleResponse(Role):
    id: int


class GroupResponse(Group):
    id: int
    roles: list[Role]
