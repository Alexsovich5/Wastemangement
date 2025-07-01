#!/usr/bin/env python3
"""
Medical Waste Item Categories Setup Script
Configures ERPNext with medical waste management item categories and groups
"""

import frappe
from frappe import _

def create_item_group(name, parent_group="All Item Groups", is_group=1):
    """Create an item group if it doesn't exist"""
    if not frappe.db.exists("Item Group", name):
        item_group = frappe.get_doc({
            "doctype": "Item Group",
            "item_group_name": name,
            "parent_item_group": parent_group,
            "is_group": is_group
        })
        item_group.insert()
        print(f"✅ Created Item Group: {name}")
        return item_group
    else:
        print(f"⚠️  Item Group already exists: {name}")
        return frappe.get_doc("Item Group", name)

def create_medical_waste_item_groups():
    """Create hierarchical item groups for medical waste management"""
    
    # Main medical waste group
    medical_waste = create_item_group("Medical Waste", "All Item Groups", 1)
    
    # Primary waste categories
    infectious_waste = create_item_group("Infectious Waste", "Medical Waste", 1)
    sharps_waste = create_item_group("Sharps Waste", "Medical Waste", 1)
    pharmaceutical_waste = create_item_group("Pharmaceutical Waste", "Medical Waste", 1)
    pathological_waste = create_item_group("Pathological Waste", "Medical Waste", 1)
    chemotherapy_waste = create_item_group("Chemotherapy Waste", "Medical Waste", 1)
    
    # Infectious waste subcategories
    create_item_group("Blood Products", "Infectious Waste", 1)
    create_item_group("Cultures and Stocks", "Infectious Waste", 1)
    create_item_group("Laboratory Waste", "Infectious Waste", 1)
    create_item_group("Surgery Waste", "Infectious Waste", 1)
    create_item_group("Isolation Waste", "Infectious Waste", 1)
    
    # Sharps waste subcategories
    create_item_group("Needles and Syringes", "Sharps Waste", 1)
    create_item_group("Scalpels and Blades", "Sharps Waste", 1)
    create_item_group("Glass Waste", "Sharps Waste", 1)
    create_item_group("Other Sharp Objects", "Sharps Waste", 1)
    
    # Pharmaceutical waste subcategories
    create_item_group("Expired Medications", "Pharmaceutical Waste", 1)
    create_item_group("Controlled Substances", "Pharmaceutical Waste", 1)
    create_item_group("Vaccines and Biologicals", "Pharmaceutical Waste", 1)
    create_item_group("IV Solutions", "Pharmaceutical Waste", 1)
    
    # Pathological waste subcategories
    create_item_group("Human Tissues", "Pathological Waste", 1)
    create_item_group("Organs and Body Parts", "Pathological Waste", 1)
    create_item_group("Placental Material", "Pathological Waste", 1)
    create_item_group("Anatomical Remains", "Pathological Waste", 1)
    
    # Chemotherapy waste subcategories
    create_item_group("Chemo Drugs", "Chemotherapy Waste", 1)
    create_item_group("Chemo Contaminated Items", "Chemotherapy Waste", 1)
    create_item_group("Chemo PPE", "Chemotherapy Waste", 1)
    
    # Waste containers
    containers = create_item_group("Waste Containers", "Medical Waste", 1)
    create_item_group("Red Bags", "Waste Containers", 1)
    create_item_group("Sharps Containers", "Waste Containers", 1)
    create_item_group("Yellow Bags", "Waste Containers", 1)
    create_item_group("Black Bags", "Waste Containers", 1)
    create_item_group("Rigid Containers", "Waste Containers", 1)

def create_waste_item_template():
    """Create a template item for medical waste with custom fields"""
    
    # Custom fields for waste items
    custom_fields = [
        {
            "fieldname": "waste_classification",
            "label": "Waste Classification",
            "fieldtype": "Select",
            "options": "\\nInfectious\\nSharps\\nPharmaceutical\\nPathological\\nChemotherapy\\nTrace Chemotherapy",
            "reqd": 1
        },
        {
            "fieldname": "hazard_level",
            "label": "Hazard Level",
            "fieldtype": "Select",
            "options": "\\nLow\\nMedium\\nHigh\\nExtreme",
            "reqd": 1
        },
        {
            "fieldname": "treatment_method",
            "label": "Required Treatment Method",
            "fieldtype": "Select",
            "options": "\\nAutoclave\\nIncineration\\nChemical Treatment\\nMicrowave\\nIrradiation\\nSecure Landfill",
            "reqd": 1
        },
        {
            "fieldname": "regulatory_code",
            "label": "Regulatory Code",
            "fieldtype": "Data",
            "description": "EPA/DOT waste code"
        },
        {
            "fieldname": "storage_requirements",
            "label": "Storage Requirements",
            "fieldtype": "Text",
            "description": "Special storage conditions required"
        },
        {
            "fieldname": "max_storage_days",
            "label": "Maximum Storage Days",
            "fieldtype": "Int",
            "description": "Maximum days before disposal required"
        },
        {
            "fieldname": "generates_manifest",
            "label": "Generates Manifest",
            "fieldtype": "Check",
            "description": "Requires DOT hazardous waste manifest"
        }
    ]
    
    # Add custom fields to Item doctype
    for field in custom_fields:
        if not frappe.db.exists("Custom Field", {"dt": "Item", "fieldname": field["fieldname"]}):
            custom_field = frappe.get_doc({
                "doctype": "Custom Field",
                "dt": "Item",
                "fieldname": field["fieldname"],
                "label": field["label"],
                "fieldtype": field["fieldtype"],
                "options": field.get("options", ""),
                "reqd": field.get("reqd", 0),
                "description": field.get("description", "")
            })
            custom_field.insert()
            print(f"✅ Added custom field: {field['label']}")

def create_sample_waste_items():
    """Create sample waste items for testing"""
    
    sample_items = [
        {
            "item_code": "RB-001",
            "item_name": "Red Bag - Infectious Waste (Small)",
            "item_group": "Red Bags",
            "stock_uom": "Nos",
            "waste_classification": "Infectious",
            "hazard_level": "High",
            "treatment_method": "Autoclave",
            "max_storage_days": 7,
            "generates_manifest": 1
        },
        {
            "item_code": "SC-001", 
            "item_name": "Sharps Container - 1 Gallon",
            "item_group": "Sharps Containers",
            "stock_uom": "Nos",
            "waste_classification": "Sharps",
            "hazard_level": "High", 
            "treatment_method": "Incineration",
            "max_storage_days": 30,
            "generates_manifest": 1
        },
        {
            "item_code": "YB-001",
            "item_name": "Yellow Bag - Pharmaceutical Waste",
            "item_group": "Yellow Bags", 
            "stock_uom": "Nos",
            "waste_classification": "Pharmaceutical",
            "hazard_level": "Medium",
            "treatment_method": "Incineration",
            "max_storage_days": 30,
            "generates_manifest": 1
        },
        {
            "item_code": "CHEMO-001",
            "item_name": "Chemotherapy Contaminated Supplies",
            "item_group": "Chemo Contaminated Items",
            "stock_uom": "Kg",
            "waste_classification": "Chemotherapy", 
            "hazard_level": "Extreme",
            "treatment_method": "Incineration",
            "max_storage_days": 7,
            "generates_manifest": 1
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
                "include_item_in_manufacturing": 0,
                "waste_classification": item_data["waste_classification"],
                "hazard_level": item_data["hazard_level"],
                "treatment_method": item_data["treatment_method"],
                "max_storage_days": item_data["max_storage_days"],
                "generates_manifest": item_data["generates_manifest"]
            })
            item.insert()
            print(f"✅ Created sample item: {item_data['item_name']}")

def setup_warehouses():
    """Create warehouses for different waste storage areas"""
    
    warehouses = [
        {
            "warehouse_name": "Infectious Waste Storage",
            "parent_warehouse": "All Warehouses",
            "warehouse_type": "Transit"
        },
        {
            "warehouse_name": "Sharps Storage", 
            "parent_warehouse": "All Warehouses",
            "warehouse_type": "Transit"
        },
        {
            "warehouse_name": "Pharmaceutical Waste Storage",
            "parent_warehouse": "All Warehouses", 
            "warehouse_type": "Transit"
        },
        {
            "warehouse_name": "Chemotherapy Waste Storage",
            "parent_warehouse": "All Warehouses",
            "warehouse_type": "Transit"
        },
        {
            "warehouse_name": "Pathological Waste Storage",
            "parent_warehouse": "All Warehouses",
            "warehouse_type": "Transit"
        },
        {
            "warehouse_name": "Treatment Facility",
            "parent_warehouse": "All Warehouses",
            "warehouse_type": "Transit"
        }
    ]
    
    for wh_data in warehouses:
        if not frappe.db.exists("Warehouse", wh_data["warehouse_name"]):
            warehouse = frappe.get_doc({
                "doctype": "Warehouse",
                "warehouse_name": wh_data["warehouse_name"],
                "parent_warehouse": wh_data["parent_warehouse"],
                "warehouse_type": wh_data["warehouse_type"]
            })
            warehouse.insert()
            print(f"✅ Created warehouse: {wh_data['warehouse_name']}")

def main():
    """Main setup function for bench execute"""
    try:
        print("🏗️  Setting up Medical Waste Item Categories...")
        
        create_medical_waste_item_groups()
        print("\n📦 Setting up custom fields...")
        
        create_waste_item_template()
        print("\n🏭 Setting up warehouses...")
        
        setup_warehouses()
        print("\n📋 Creating sample items...")
        
        create_sample_waste_items()
        
        frappe.db.commit()
        print("\n✅ Medical waste item categories setup completed!")
        
    except Exception as e:
        print(f"❌ Error during setup: {str(e)}")
        frappe.db.rollback()
        raise

# For bench execute compatibility - function is called directly
if __name__ == "__main__":
    # Standalone execution with Frappe initialization
    import frappe
    frappe.init(site='frontend')
    frappe.connect()
    main()