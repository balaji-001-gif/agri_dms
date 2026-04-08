from . import __version__ as app_version

app_name = "agri_dms"
app_title = "Agri DMS"
app_publisher = "Agri-DMS Team"
app_description = "Distributor Management System for Agriculture Machine Manufacturers"
app_email = "admin@agri-dms.com"
app_license = "MIT"

# DocType Highlights
# -----------------
# Manufacturer
# Distributor
# Customer Sale
# Distributor Stock
# Commission Scheme

doc_events = {
    "Customer Sale": {
        "on_submit": "agri_dms.erpnext_bridge.doctype_sync.sync_sale_to_sinv",
    },
    "Manufacturer": {
        "on_update": "agri_dms.erpnext_bridge.doctype_sync.sync_manufacturer_to_supplier",
    },
    "Distributor": {
        "on_update": "agri_dms.erpnext_bridge.doctype_sync.sync_distributor_to_customer",
    },
    "Machine": {
        "on_update": "agri_dms.erpnext_bridge.doctype_sync.sync_machine_to_item",
    },
    "Distributor Purchase Order": {
        "on_update_after_submit": "agri_dms.erpnext_bridge.doctype_sync.sync_po_to_erpnext",
    },
    "Goods Receipt Note": {
        "on_submit": "agri_dms.erpnext_bridge.doctype_sync.sync_grn_to_stock_entry",
    }
}

# Reports
# -------
# scheduler_events = {
#     "daily": [
#         "agri_dms.agri_dms.report.slow_moving_stock.execute"
#     ]
# }
