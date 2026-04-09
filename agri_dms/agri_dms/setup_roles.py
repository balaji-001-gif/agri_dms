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

    if not frappe.db.exists("Module Def", "Agri DMS"):
        print("Module Def 'Agri DMS' not found, creating it...")
        frappe.get_doc({
            "doctype": "Module Def",
            "module_name": "Agri DMS",
            "app_name": "agri_dms",
            "custom": 0,
            "restrict_to_domain": ""
        }).insert(ignore_permissions=True)
        print("Created Module Def: Agri DMS")

if __name__ == "__main__":
    # This script is meant to be run via 'bench execute'
    create_roles()
