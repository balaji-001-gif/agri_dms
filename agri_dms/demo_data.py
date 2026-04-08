import frappe
from frappe.utils import nowdate, add_months

def setup_demo_data():
    """Main function to setup demo data for Agri-DMS"""
    print("Starting Agri-DMS Demo Data Setup...")
    
    # 1. Machine Categories
    categories = [
        {"name": "Tractor", "code": "TRAC"},
        {"name": "Harvester", "code": "HARV"},
        {"name": "Sprayer", "code": "SPRY"}
    ]
    for cat in categories:
        if not frappe.db.exists("Machine Category", cat["name"]):
            doc = frappe.get_doc({
                "doctype": "Machine Category",
                "category_name": cat["name"],
                "category_code": cat["code"],
                "is_active": 1
            })
            doc.insert(ignore_permissions=True)
            print(f"Created Category: {cat['name']}")
    frappe.db.commit()

    # 2. Manufacturers
    manufacturers = [
        {"name": "AgroPower Industrial", "code": "AGRI-001", "country": "India"},
        {"name": "GreenField Mechanics", "code": "GFM-002", "country": "India"}
    ]
    for mfr in manufacturers:
        if not frappe.db.exists("Manufacturer", mfr["name"]):
            doc = frappe.get_doc({
                "doctype": "Manufacturer",
                "manufacturer_name": mfr["name"],
                "manufacturer_code": mfr["code"],
                "country": mfr["country"],
                "status": "Active"
            })
            doc.insert(ignore_permissions=True)
            print(f"Created Manufacturer: {mfr['name']}")
    frappe.db.commit()

    # 3. Machines (Products)
    machines = [
        {"name": "AgroPower T-500", "code": "AP-T500", "mfr": "AgroPower Industrial", "cat": "Tractor", "price": 1500000},
        {"name": "AgroPower S-10", "code": "AP-S10", "mfr": "AgroPower Industrial", "cat": "Sprayer", "price": 450000},
        {"name": "GreenField H-X1", "code": "GF-HX1", "mfr": "GreenField Mechanics", "cat": "Harvester", "price": 3200000}
    ]
    for mac in machines:
        if not frappe.db.exists("Machine", mac["name"]):
            doc = frappe.get_doc({
                "doctype": "Machine",
                "machine_name": mac["name"],
                "machine_code": mac["code"],
                "manufacturer": mac["mfr"],
                "category": mac["cat"],
                "mrp": mac["price"] * 1.2,
                "dealer_price": mac["price"],
                "gst_rate_pct": 18,
                "status": "Active"
            })
            doc.insert(ignore_permissions=True)
            print(f"Created Machine: {mac['name']}")
    frappe.db.commit()

    # 4. Region
    if not frappe.db.exists("Region", "South India"):
        region = frappe.get_doc({
            "doctype": "Region",
            "region_name": "South India",
            "region_code": "SI",
            "is_active": 1
        })
        region.insert(ignore_permissions=True)
        print("Created Region: South India")
    frappe.db.commit()

    # 5. Distributor
    if not frappe.db.exists("Distributor", "Global Agri-Solutions"):
        dist = frappe.get_doc({
            "doctype": "Distributor",
            "distributor_name": "Global Agri-Solutions",
            "distributor_code": "DIST-KA-01",
            "distributor_type": "Primary",
            "region": "South India",
            "state": "Karnataka",
            "address": "Bangalore Industrial Area",
            "owner_name": "Rajesh Kumar",
            "contact_email": "rajesh@globalagri.com",
            "contact_phone": "9888877777",
            "gst_number": "29AAAAA0000A1Z5",
            "pan_number": "AAAAA0000A",
            "kyc_status": "Verified",
            "status": "Active"
        })
        dist.insert(ignore_permissions=True)
        print("Created Distributor: Global Agri-Solutions")
    frappe.db.commit()

    # 6. Sample Sales (Draft)
    if not frappe.db.exists("Customer Sale", {"customer_name": "Farmer Venkat"}):
        sale = frappe.get_doc({
            "doctype": "Customer Sale",
            "distributor": "Global Agri-Solutions",
            "customer_name": "Farmer Venkat",
            "sale_date": nowdate(),
            "status": "Draft",
            "items": [{
                "machine": "AgroPower T-500",
                "qty": 1,
                "selling_price": 1700000
            }]
        })
        sale.insert(ignore_permissions=True)
        print("Created Sample Sale (Draft): Farmer Venkat")

    print("Demo Data Setup Complete!")

if __name__ == "__main__":
    setup_demo_data()
