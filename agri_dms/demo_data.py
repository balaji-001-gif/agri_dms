import frappe
from frappe.utils import nowdate, add_months, getdate

def setup_demo_data():
    """Main function to setup full-suite demo data for Agri-DMS"""
    print("Starting Agri-DMS Full-Suite Demo Data Setup...")
    
    # 1. Fiscal Year (Prerequisite for targets)
    if not frappe.db.exists("Fiscal Year", "2024-25"):
        fy = frappe.get_doc({
            "doctype": "Fiscal Year",
            "year": "2024-25",
            "year_start_date": "2024-04-01",
            "year_end_date": "2025-03-31"
        })
        fy.insert(ignore_permissions=True)
        print("Created Fiscal Year: 2024-25")

    # 2. Machine Categories
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

    # 3. Manufacturers
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

    # 4. Machines (Products)
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

    # 5. Region & Distributors
    regions = ["South India", "North India"]
    for reg in regions:
        if not frappe.db.exists("Region", reg):
            frappe.get_doc({"doctype": "Region", "region_name": reg, "region_code": reg[:2].upper(), "is_active": 1}).insert(ignore_permissions=True)

    distributors = [
        {"name": "Global Agri-Solutions", "code": "DIST-KA-01", "state": "Karnataka", "region": "South India"},
        {"name": "Northern Farm Equip", "code": "DIST-PB-02", "state": "Punjab", "region": "North India"}
    ]
    for d in distributors:
        if not frappe.db.exists("Distributor", d["name"]):
            dist = frappe.get_doc({
                "doctype": "Distributor",
                "distributor_name": d["name"],
                "distributor_code": d["code"],
                "distributor_type": "Primary",
                "region": d["region"],
                "state": d["state"],
                "address": "Main Market Road",
                "owner_name": "Demo Partner",
                "contact_email": f"partner@{d['code'].lower()}.com",
                "contact_phone": "9000000000",
                "gst_number": "29AAAAA0000A1Z5",
                "pan_number": "AAAAA0000A",
                "kyc_status": "Verified",
                "status": "Active"
            })
            dist.insert(ignore_permissions=True)
            print(f"Created Distributor: {d['name']}")

    # 6. Distributor Target
    if not frappe.db.exists("Distributor Target", {"distributor": "Global Agri-Solutions"}):
        target = frappe.get_doc({
            "doctype": "Distributor Target",
            "distributor": "Global Agri-Solutions",
            "fiscal_year": "2024-25",
            "period": "Annual",
            "target_amount": 50000000,
            "status": "Confirmed"
        })
        target.insert(ignore_permissions=True)
        print("Created Distributor Target: Global Agri-Solutions")

    # 7. Procurement Workflow (DPO -> GRN -> Stock)
    if not frappe.db.exists("Distributor Purchase Order", {"distributor": "Global Agri-Solutions"}):
        dpo = frappe.get_doc({
            "doctype": "Distributor Purchase Order",
            "distributor": "Global Agri-Solutions",
            "manufacturer": "AgroPower Industrial",
            "order_date": nowdate(),
            "status": "Approved",
            "items": [{
                "machine": "AgroPower T-500",
                "qty": 5,
                "unit_price": 1500000
            }]
        })
        dpo.insert(ignore_permissions=True)
        print(f"Created DPO: {dpo.name}")

        # Create GRN against DPO
        grn = frappe.get_doc({
            "doctype": "Goods Receipt Note",
            "distributor": "Global Agri-Solutions",
            "purchase_order": dpo.name,
            "receipt_date": nowdate(),
            "status": "Received",
            "items": [{
                "machine": "AgroPower T-500",
                "qty": 5
            }]
        })
        grn.insert(ignore_permissions=True)
        print(f"Created GRN for DPO: {dpo.name}")

        # Initialize Stock
        if not frappe.db.exists("Distributor Stock", {"distributor": "Global Agri-Solutions", "machine": "AgroPower T-500"}):
            stock = frappe.get_doc({
                "doctype": "Distributor Stock",
                "distributor": "Global Agri-Solutions",
                "machine": "AgroPower T-500",
                "qty_in_hand": 5,
                "location": "Main Yard"
            })
            stock.insert(ignore_permissions=True)
            print("Initialized Stock for Global Agri-Solutions")

    # 8. Sales Workflow
    if not frappe.db.exists("Customer Sale", {"customer_name": "Farmer John"}):
        sale = frappe.get_doc({
            "doctype": "Customer Sale",
            "distributor": "Global Agri-Solutions",
            "customer_name": "Farmer John",
            "sale_date": nowdate(),
            "status": "Confirmed",
            "items": [{
                "machine": "AgroPower T-500",
                "qty": 1,
                "selling_price": 1750000
            }]
        })
        sale.insert(ignore_permissions=True)
        print(f"Created Confirmed Sale: {sale.name}")

    # 9. Stock Transfer
    if not frappe.db.exists("Stock Transfer", {"from_distributor": "Global Agri-Solutions"}):
        transfer = frappe.get_doc({
            "doctype": "Stock Transfer",
            "transfer_type": "Distributor-to-Distributor",
            "from_distributor": "Global Agri-Solutions",
            "to_distributor": "Northern Farm Equip",
            "status": "Received",
            "items": [{
                "machine": "AgroPower T-500",
                "qty": 1
            }]
        })
        transfer.insert(ignore_permissions=True)
        print(f"Created Stock Transfer: {transfer.name}")

    # 10. Commission Lifecycle
    if not frappe.db.exists("Commission Scheme", "Standard Dealer FY25"):
        scheme = frappe.get_doc({
            "doctype": "Commission Scheme",
            "scheme_name": "Standard Dealer FY25",
            "scheme_type": "Slab-Based",
            "is_active": 1,
            "slabs": [
                {"from_amount": 0, "to_amount": 1000000, "commission_pct": 5},
                {"from_amount": 1000001, "to_amount": 10000000, "commission_pct": 10}
            ]
        })
        scheme.insert(ignore_permissions=True)
        print("Created Commission Scheme: Standard Dealer FY25")

        # Assign to Distributor
        frappe.db.set_value("Distributor", "Global Agri-Solutions", "commission_scheme", "Standard Dealer FY25")

    # 11. Commission Ledger & Payout (Manual Entry for Demo)
    if not frappe.db.exists("Commission Ledger", {"distributor": "Global Agri-Solutions"}):
        sale_name = frappe.db.get_value("Customer Sale", {"customer_name": "Farmer John"}, "name")
        ledger = frappe.get_doc({
            "doctype": "Commission Ledger",
            "distributor": "Global Agri-Solutions",
            "customer_sale": sale_name,
            "commission_amount": 175000,
            "status": "Approved"
        })
        ledger.insert(ignore_permissions=True)
        print(f"Created Commission Ledger Entry for Sale: {sale_name}")

        # Batch Payout
        payout = frappe.get_doc({
            "doctype": "Commission Payout",
            "distributor": "Global Agri-Solutions",
            "status": "Paid",
            "entries": [{
                "commission_ledger": ledger.name,
                "amount": 175000
            }]
        })
        payout.insert(ignore_permissions=True)
        print(f"Created Commission Payout: {payout.name}")

    print("🏁 Full-Suite Demo Data Setup Complete!")

if __name__ == "__main__":
    setup_demo_data()
