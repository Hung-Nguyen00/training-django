from rolepermissions.roles import AbstractUserRole


class Admin(AbstractUserRole):
    role = "Admin"
    description = "Manage Everything"
    available_permissions = {
        "manage_order": True,
        "manage_product": True,
    }


class Staff(AbstractUserRole):
    role = "Staff"
    description = "Manage self-product"
    available_permissions = {
        "manage_product": True,
    }
