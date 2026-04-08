import frappe
from frappe.utils import nowdate

def sync_manufacturer_to_supplier(doc, method=None):
    """Sync Manufacturer to ERPNext Supplier"""
    if doc.erpnext_supplier_id:
        supplier = frappe.get_doc("Supplier", doc.erpnext_supplier_id)
    else:
        supplier = frappe.new_doc("Supplier")
        supplier.supplier_name = doc.manufacturer_name
    
    supplier.supplier_group = "Distributor" # Default group
    supplier.country = doc.country
    supplier.tax_id = doc.gst_number
    supplier.save(ignore_permissions=True)
    
    if not doc.erpnext_supplier_id:
        doc.db_set("erpnext_supplier_id", supplier.name)

def sync_distributor_to_customer(doc, method=None):
    """Sync Distributor to ERPNext Customer"""
    if doc.erpnext_customer_id:
        customer = frappe.get_doc("Customer", doc.erpnext_customer_id)
    else:
        customer = frappe.new_doc("Customer")
        customer.customer_name = doc.distributor_name
    
    customer.customer_group = "Distributor"
    customer.territory = doc.territory or "All Territories"
    customer.tax_id = doc.gst_number
    customer.save(ignore_permissions=True)
    
    if not doc.erpnext_customer_id:
        doc.db_set("erpnext_customer_id", customer.name)

def sync_machine_to_item(doc, method=None):
    """Sync Machine to ERPNext Item"""
    if doc.erpnext_item_code:
        item = frappe.get_doc("Item", doc.erpnext_item_code)
    else:
        item = frappe.new_doc("Item")
        item.item_code = doc.machine_code
    
    item.item_name = doc.machine_name

    # Resolve category hash to readable name for ERPNext Item Group
    category_name = "All Item Groups"
    if doc.category:
        category_name = frappe.db.get_value("Machine Category", doc.category, "category_name") or "All Item Groups"
        # Ensure the Item Group exists in ERPNext
        if not frappe.db.exists("Item Group", category_name):
            ig = frappe.get_doc({
                "doctype": "Item Group",
                "item_group_name": category_name,
                "parent_item_group": "All Item Groups"
            })
            ig.insert(ignore_permissions=True)
            frappe.db.commit()

    item.item_group = category_name
    item.stock_uom = "Nos"
    item.is_stock_item = 1
    item.valuation_rate = doc.dealer_price
    item.standard_rate = doc.mrp
    item.save(ignore_permissions=True)
    
    if not doc.erpnext_item_code:
        doc.db_set("erpnext_item_code", item.name)

def sync_po_to_erpnext(doc, method=None):
    """Sync Approved DPO to ERPNext Purchase Order"""
    if doc.status != "Approved" or doc.erpnext_po_id:
        return
    
    manufacturer = frappe.get_doc("Manufacturer", doc.manufacturer)
    items = []
    for item in doc.items:
        machine = frappe.get_doc("Machine", item.machine)
        items.append({
            "item_code": machine.erpnext_item_code,
            "qty": item.qty,
            "rate": item.unit_price
        })
    
    epo = frappe.get_doc({
        "doctype": "Purchase Order",
        "supplier": manufacturer.erpnext_supplier_id,
        "transaction_date": doc.order_date or nowdate(),
        "items": items
    })
    epo.insert(ignore_permissions=True)
    epo.submit()
    
    doc.db_set("erpnext_po_id", epo.name)

def sync_grn_to_stock_entry(doc, method=None):
    """Sync GRN to ERPNext Stock Entry (Material Receipt)"""
    # Logic to create Stock Entry type 'Material Receipt'
    pass

def sync_sale_to_sinv(doc, method=None):
    """Sync Confirmed Customer Sale to ERPNext Sales Invoice"""
    if doc.erpnext_sinv_id or doc.status != "Confirmed":
        return
    
    distributor = frappe.get_doc("Distributor", doc.distributor)
    items = []
    for item in doc.items:
        machine = frappe.get_doc("Machine", item.machine)
        items.append({
            "item_code": machine.erpnext_item_code,
            "qty": item.qty,
            "rate": item.selling_price,
            "serial_no": item.serial_no
        })
    
    sinv = frappe.get_doc({
        "doctype": "Sales Invoice",
        "customer": distributor.erpnext_customer_id,
        "posting_date": doc.sale_date or nowdate(),
        "items": items
    })
    sinv.insert(ignore_permissions=True)
    sinv.submit()
    
    doc.db_set("erpnext_sinv_id", sinv.name)
