import frappe

def create_roles():
    roles = ["DMS Admin", "DMS Distributor Manager", "DMS Sales Executive", "DMS Finance"]
    for role_name in roles:
        if not frappe.db.exists("Role", role_name):
            role = frappe.get_doc({
                "doctype": "Role",
                "role_name": role_name,
                "desk_access": 1
            })
            role.insert(ignore_permissions=True)
            print(f"Created Role: {role_name}")
        else:
            print(f"Role {role_name} already exists")

if __name__ == "__main__":
    # This script is meant to be run via 'bench execute'
    create_roles()
