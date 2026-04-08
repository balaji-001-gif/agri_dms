import frappe
from frappe.utils import nowdate, add_months

def setup_demo_data():
    """Main function to setup demo data for Agri-DMS"""
    print("Starting Agri-DMS Demo Data Setup...")

    # 1. Machine Categories
    cat_map = {}  # readable name -> actual doc.name
    categories = [
        {"readable": "Tractor", "code": "TRAC"},
        {"readable": "Harvester", "code": "HARV"},
        {"readable": "Sprayer", "code": "SPRY"}
    ]
    for cat in categories:
        existing = frappe.db.get_value("Machine Category", {"category_name": cat["readable"]}, "name")
        if existing:
            cat_map[cat["readable"]] = existing
            print(f"Category already exists: {cat['readable']} ({existing})")
        else:
            doc = frappe.get_doc({
                "doctype": "Machine Category",
                "category_name": cat["readable"],
                "category_code": cat["code"],
                "is_active": 1
            })
            doc.insert(ignore_permissions=True)
            cat_map[cat["readable"]] = doc.name
            print(f"Created Category: {cat['readable']} ({doc.name})")
    frappe.db.commit()

    # 2. Manufacturers
    mfr_map = {}  # readable name -> actual doc.name
    manufacturers = [
        {"readable": "AgroPower Industrial", "code": "AGRI-001", "country": "India"},
        {"readable": "GreenField Mechanics", "code": "GFM-002", "country": "India"}
    ]
    for mfr in manufacturers:
        existing = frappe.db.get_value("Manufacturer", {"manufacturer_name": mfr["readable"]}, "name")
        if existing:
            mfr_map[mfr["readable"]] = existing
            print(f"Manufacturer already exists: {mfr['readable']} ({existing})")
        else:
            doc = frappe.get_doc({
                "doctype": "Manufacturer",
                "manufacturer_name": mfr["readable"],
                "manufacturer_code": mfr["code"],
                "country": mfr["country"],
                "status": "Active"
            })
            doc.insert(ignore_permissions=True)
            mfr_map[mfr["readable"]] = doc.name
            print(f"Created Manufacturer: {mfr['readable']} ({doc.name})")
    frappe.db.commit()

    # 3. Machines (Products)
    mac_map = {}  # readable name -> actual doc.name
    machines = [
        {"readable": "AgroPower T-500", "code": "AP-T500", "mfr": "AgroPower Industrial", "cat": "Tractor", "price": 1500000},
        {"readable": "AgroPower S-10", "code": "AP-S10", "mfr": "AgroPower Industrial", "cat": "Sprayer", "price": 450000},
        {"readable": "GreenField H-X1", "code": "GF-HX1", "mfr": "GreenField Mechanics", "cat": "Harvester", "price": 3200000}
    ]
    for mac in machines:
        existing = frappe.db.get_value("Machine", {"machine_name": mac["readable"]}, "name")
        if existing:
            mac_map[mac["readable"]] = existing
            print(f"Machine already exists: {mac['readable']} ({existing})")
        else:
            doc = frappe.get_doc({
                "doctype": "Machine",
                "machine_name": mac["readable"],
                "machine_code": mac["code"],
                "manufacturer": mfr_map[mac["mfr"]],
                "category": cat_map[mac["cat"]],
                "mrp": mac["price"] * 1.2,
                "dealer_price": mac["price"],
                "gst_rate_pct": 18,
                "status": "Active"
            })
            doc.insert(ignore_permissions=True)
            mac_map[mac["readable"]] = doc.name
            print(f"Created Machine: {mac['readable']} ({doc.name})")
    frappe.db.commit()

    # 4. Region
    region_name = frappe.db.get_value("Region", {"region_name": "South India"}, "name")
    if not region_name:
        region = frappe.get_doc({
            "doctype": "Region",
            "region_name": "South India",
            "region_code": "SI",
            "is_active": 1
        })
        region.insert(ignore_permissions=True)
        region_name = region.name
        print(f"Created Region: South India ({region_name})")
    else:
        print(f"Region already exists: South India ({region_name})")
    frappe.db.commit()

    # 5. Distributor
    dist_name = frappe.db.get_value("Distributor", {"distributor_name": "Global Agri-Solutions"}, "name")
    if not dist_name:
        dist = frappe.get_doc({
            "doctype": "Distributor",
            "distributor_name": "Global Agri-Solutions",
            "distributor_code": "DIST-KA-01",
            "distributor_type": "Primary",
            "region": region_name,
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
        dist_name = dist.name
        print(f"Created Distributor: Global Agri-Solutions ({dist_name})")
    else:
        print(f"Distributor already exists: Global Agri-Solutions ({dist_name})")
    frappe.db.commit()

    # 6. Sample Sales (Draft)
    existing_sale = frappe.db.get_value("Customer Sale", {"customer_name": "Farmer Venkat"}, "name")
    if not existing_sale:
        sale = frappe.get_doc({
            "doctype": "Customer Sale",
            "distributor": dist_name,
            "customer_name": "Farmer Venkat",
            "sale_date": nowdate(),
            "status": "Draft",
            "items": [{
                "machine": mac_map.get("AgroPower T-500"),
                "qty": 1,
                "selling_price": 1700000
            }]
        })
        sale.insert(ignore_permissions=True)
        print(f"Created Sample Sale (Draft): Farmer Venkat ({sale.name})")
    else:
        print(f"Sale already exists: Farmer Venkat ({existing_sale})")
    frappe.db.commit()

    print("Demo Data Setup Complete!")

if __name__ == "__main__":
    setup_demo_data()
