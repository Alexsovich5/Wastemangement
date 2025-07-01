import frappe

print("🔗 Setting up basic medical waste management...")

# First, let's check what companies exist
companies = frappe.get_all("Company", fields=["name"])
print(f"Available companies: {[c.name for c in companies]}")

# Use the first available company for warehouses
if companies:
    company_name = companies[0].name
    print(f"Using company: {company_name}")
else:
    print("No companies found, creating default company")
    company = frappe.get_doc({
        "doctype": "Company",
        "company_name": "Medical Waste Management",
        "abbr": "MWM",
        "default_currency": "USD",
        "country": "United States"
    })
    company.insert()
    company_name = company.company_name
    print(f"✅ Created company: {company_name}")

# Create Medical Waste item group first
if not frappe.db.exists("Item Group", "Medical Waste"):
    medical_waste_group = frappe.get_doc({
        "doctype": "Item Group",
        "item_group_name": "Medical Waste",
        "parent_item_group": "All Item Groups",
        "is_group": 1
    })
    medical_waste_group.insert()
    print("✅ Created Medical Waste item group")
else:
    print("⚠️  Medical Waste item group already exists")

# Create sub-categories
sub_groups = [
    "Infectious Waste",
    "Sharps Waste", 
    "Pharmaceutical Waste",
    "Pathological Waste",
    "Chemotherapy Waste"
]

for group_name in sub_groups:
    if not frappe.db.exists("Item Group", group_name):
        item_group = frappe.get_doc({
            "doctype": "Item Group",
            "item_group_name": group_name,
            "parent_item_group": "Medical Waste",
            "is_group": 0
        })
        item_group.insert()
        print(f"✅ Created item group: {group_name}")
    else:
        print(f"⚠️  Item group already exists: {group_name}")

# Create basic UOMs needed for medical waste
uoms = ["Container", "Gallon", "Pound"]
for uom in uoms:
    if not frappe.db.exists("UOM", uom):
        uom_doc = frappe.get_doc({
            "doctype": "UOM",
            "uom_name": uom
        })
        uom_doc.insert()
        print(f"✅ Created UOM: {uom}")
    else:
        print(f"⚠️  UOM already exists: {uom}")

frappe.db.commit()
print("✅ Basic setup completed successfully!")