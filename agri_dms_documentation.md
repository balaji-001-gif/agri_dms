# Agri-DMS Technical Documentation

## 1. System Overview

**Agri-DMS** (Agriculture Distributor Management System) is a specialized extension for **ERPNext v15** built on the **Frappe Framework**. It is designed to bridge the gap between Agriculture Machine Manufacturers and their Distributor networks, providing real-time visibility into inventory, sales performance, and commission payouts.

### Architectural Context
- **Base Framework**: Frappe v15
- **Primary Integration**: ERPNext v15
- **Target Audience**: Manufacturers of agricultural machinery (e.g., tractors, harvesters) and their primary/secondary distributors.

---

## 2. Functional Modules

### 2.1 Manufacturer & Product Catalog
Manages the upstream supply chain.
- **Manufacturer**: Defines machine manufacturers (integrated with ERPNext Suppliers).
- **Machine Category**: Groups machines by type (e.g., Tractors, Harvesters).
- **Machine**: The individual product record including technical specs, Dealer Price, and MRP (integrated with ERPNext Items).

### 2.2 Distributor Network
Manages the network of partners.
- **Distributor**: Detailed profiles for primary and secondary distributors (integrated with ERPNext Customers).
- **Region**: Geographical grouping for reporting and target tracking.
- **Distributor Target**: Annual or monthly sales targets defined at the distributor-region level.

### 2.3 Sales & Order Management
Handles the core transaction workflow.
- **Distributor Purchase Order (DPO)**: Order placed by a distributor to a manufacturer. Approval triggers an automated Purchase Order in ERPNext.
- **Customer Sale**: Sale logged by a distributor to an end customer. Confirmation triggers an automated Sales Invoice in ERPNext.

### 2.4 Inventory & Stock
Tracks physical machines in the field.
- **Distributor Stock**: Real-time ledger of machines available at each distributor's yard.
- **Goods Receipt Note (GRN)**: Incoming stock from manufacturers (Material Receipt).
- **Stock Transfer**: Lateral movement of stock between distributors.

### 2.5 Commission Engine
Automates financial incentives.
- **Commission Scheme**: Defines payout logic (e.g., Flat 5% or Slab-based).
- **Commission Ledger**: Automatically calculates and stores commission earned per sale.
- **Commission Payout**: Grouping of ledger entries for periodic payment processing.

---

## 3. Security Model & Role Permissions

The system uses a custom role-based access control (RBAC) model to ensure data integrity and confidentiality.

### Core Roles
1.  **DMS Admin**: Full administrative control over all DocTypes and Reports.
2.  **DMS Distributor Manager**: Manages distributors, regions, and approves DPOs.
3.  **DMS Sales Executive**: Logs customer sales and checks stock availability.
4.  **DMS Finance**: Manages commissions, payouts, and outstanding payments.

### Permission Matrix (Summary)

| DocType Group | DMS Admin | Distributor Manager | Sales Executive | Finance |
| :--- | :---: | :---: | :---: | :---: |
| **Master Data** | Full | Read/Write/Create | Read Only | Read Only |
| **Sales Docs** | Full | Full (Submit/Amend) | Create/Write/Read | Read Only |
| **Inventory** | Full | Full | Read Only | Read Only |
| **Commissions** | Full | Read Only | Read Only | Full |

---

## 4. ERPNext Integration (The Bridge)

Agri-DMS includes a robust background synchronization engine (`doctype_sync.py`) that ensures DMS transactions are reflected in ERPNext accounting and stock modules.

### Synchronized DocTypes
| Agri-DMS DocType | ERPNext DocType | Action Trigger |
| :--- | :--- | :--- |
| Manufacturer | Supplier | On Create/Update |
| Distributor | Customer | On Create/Update |
| Machine | Item | On Create/Update |
| DPO | Purchase Order | On Approval |
| Customer Sale | Sales Invoice | On Confirmation |

### Sync Logic Example (DPO to Purchase Order)
```python
def sync_po_to_erpnext(doc, method=None):
    if doc.status != "Approved" or doc.erpnext_po_id:
        return
    # Triggers ERPNext PO creation...
    epo = frappe.get_doc({
        "doctype": "Purchase Order",
        "supplier": manufacturer.erpnext_supplier_id,
        "transaction_date": doc.order_date or nowdate(),
        "items": items
    })
    epo.insert(ignore_permissions=True)
    epo.submit()
```

---

## 5. Analytics & Reporting

The system includes 8 standard reports designed for different business stakeholders.

1.  **Distributor Stock Ledger**: Real-time machine tracking per distributor (Admin, Manager, Sales).
2.  **Monthly Sales Trend**: Revenue and order count analysis over time (Admin, Manager).
3.  **Distributor Target vs Achievement**: Performance tracking against defined targets (Admin, Manager, Sales).
4.  **Commission Summary by Distributor**: Aggregated earnings per period (Admin, Finance).
5.  **Distributor Ageing and Outstanding**: Financial health and pending dues tracking (Admin, Finance, Manager).
6.  **Machine-wise Sales Analysis**: Popularity and volume analysis per machine model (Admin, Manager).
7.  **Slow Moving Stock**: Identifies inventory aging in distributor yards (Admin, Manager).
8.  **Distributor-wise Sales Summary**: Quick overview of sales performance (Admin, Manager).

---

## 6. Setup & Administration

### Initialization
After installing the app, run the following command to initialize custom roles:
```bash
bench --site [site-name] execute agri_dms.agri_dms.setup_roles.create_roles
```

### Training/Demo Data
To populate a fresh environment with sample manufacturers, machines, and distributors:
```bash
bench --site [site-name] execute agri_dms.agri_dms.demo_data.setup_demo_data
```

### Migration
Always ensure migration is run after pulling updates:
```bash
bench --site [site-name] migrate
```
