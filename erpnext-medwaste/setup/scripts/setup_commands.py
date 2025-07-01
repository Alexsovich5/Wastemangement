import frappe

# Item categories setup
print("📦 Setting up medical waste item categories...")

item_groups = [
    "Medical Waste",
    "Infectious Waste", 
    "Sharps Waste",
    "Pharmaceutical Waste",
    "Pathological Waste",
    "Chemotherapy Waste"
]

parent_group = "All Item Groups"

for i, group_name in enumerate(item_groups):
    if i > 0:
        parent_group = "Medical Waste"
        
    if not frappe.db.exists("Item Group", group_name):
        item_group = frappe.get_doc({
            "doctype": "Item Group",
            "item_group_name": group_name,
            "parent_item_group": parent_group,
            "is_group": 1
        })
        item_group.insert()
        print(f"✅ Created Item Group: {group_name}")
    else:
        print(f"⚠️  Item Group already exists: {group_name}")

# Create sample items
print("\n📄 Creating sample waste items...")

sample_items = [
    {
        "item_code": "RED-BAG-32GAL",
        "item_name": "Red Biohazard Bag 32 Gallon",
        "item_group": "Infectious Waste",
        "stock_uom": "Each"
    },
    {
        "item_code": "SHARPS-CONT-1GAL",
        "item_name": "Sharps Container 1 Gallon",
        "item_group": "Sharps Waste",
        "stock_uom": "Each"
    },
    {
        "item_code": "YELLOW-BAG-32GAL",
        "item_name": "Yellow Chemo Bag 32 Gallon",
        "item_group": "Chemotherapy Waste",
        "stock_uom": "Each"
    }
]

for item_data in sample_items:
    if not frappe.db.exists("Item", item_data["item_code"]):
        item = frappe.get_doc({
            "doctype": "Item",
            "item_code": item_data["item_code"],
            "item_name": item_data["item_name"],
            "item_group": item_data["item_group"],
            "stock_uom": item_data["stock_uom"],
            "is_stock_item": 1,
            "maintain_stock": 1
        })
        item.insert()
        print(f"✅ Created Item: {item_data['item_name']}")
    else:
        print(f"⚠️  Item already exists: {item_data['item_name']}")

# Create warehouses
print("\n🏢 Creating medical waste warehouses...")

warehouses = [
    "Medical Waste Collection - MWM",
    "Infectious Waste Storage - MWM", 
    "Sharps Collection - MWM",
    "Pharmaceutical Storage - MWM",
    "Treatment Facility - MWM"
]

for warehouse_name in warehouses:
    if not frappe.db.exists("Warehouse", warehouse_name):
        warehouse = frappe.get_doc({
            "doctype": "Warehouse",
            "warehouse_name": warehouse_name,
            "company": "Medical Waste Management"
        })
        warehouse.insert()
        print(f"✅ Created Warehouse: {warehouse_name}")
    else:
        print(f"⚠️  Warehouse already exists: {warehouse_name}")

frappe.db.commit()
print("\n✅ Medical waste setup completed!")