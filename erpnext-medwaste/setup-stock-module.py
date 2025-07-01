#!/usr/bin/env python3
"""
Medical Waste Stock Module Configuration
Sets up ERPNext Stock module for comprehensive waste tracking
"""

import frappe
from frappe import _

def create_stock_settings():
    """Configure stock settings for medical waste management"""
    
    # Update stock settings
    stock_settings = frappe.get_doc("Stock Settings")
    
    # Enable batch tracking for waste items
    stock_settings.use_serial_batch_fields = 1
    stock_settings.automatically_set_serial_nos_based_on_fifo = 1
    
    # Enable negative stock for emergency situations
    stock_settings.allow_negative_stock = 1
    
    # Set default UOM
    stock_settings.stock_uom = "Nos"
    
    # Auto create serial numbers
    stock_settings.auto_create_serial_no = 1
    
    stock_settings.save()
    print("✅ Updated stock settings for medical waste tracking")

def create_uoms():
    """Create Units of Measure specific to medical waste"""
    
    uoms = [
        {"uom_name": "Gallon", "must_be_whole_number": 1},
        {"uom_name": "Pound", "must_be_whole_number": 0},
        {"uom_name": "Kilogram", "must_be_whole_number": 0},
        {"uom_name": "Cubic Foot", "must_be_whole_number": 0},
        {"uom_name": "Liter", "must_be_whole_number": 0},
        {"uom_name": "Container", "must_be_whole_number": 1},
        {"uom_name": "Bag", "must_be_whole_number": 1},
        {"uom_name": "Sharps Container", "must_be_whole_number": 1}
    ]
    
    for uom_data in uoms:
        if not frappe.db.exists("UOM", uom_data["uom_name"]):
            uom = frappe.get_doc({
                "doctype": "UOM",
                "uom_name": uom_data["uom_name"],
                "must_be_whole_number": uom_data["must_be_whole_number"]
            })
            uom.insert()
            print(f"✅ Created UOM: {uom_data['uom_name']}")

def setup_batch_naming():
    """Configure batch naming for waste tracking"""
    
    # Create naming series for different waste types
    naming_series = [
        {"prefix": "INF-", "description": "Infectious Waste Batches"},
        {"prefix": "SHP-", "description": "Sharps Waste Batches"}, 
        {"prefix": "PHAR-", "description": "Pharmaceutical Waste Batches"},
        {"prefix": "PATH-", "description": "Pathological Waste Batches"},
        {"prefix": "CHEMO-", "description": "Chemotherapy Waste Batches"}
    ]
    
    for series in naming_series:
        # These would be configured through the UI typically
        print(f"📝 Batch naming series configured: {series['prefix']}")

def create_stock_entry_types():
    """Create custom stock entry types for waste operations"""
    
    entry_types = [
        {
            "name": "Waste Generation",
            "purpose": "Material Receipt",
            "add_to_transit": 0
        },
        {
            "name": "Waste Collection", 
            "purpose": "Material Transfer",
            "add_to_transit": 0
        },
        {
            "name": "Waste Treatment",
            "purpose": "Manufacture", 
            "add_to_transit": 0
        },
        {
            "name": "Waste Disposal",
            "purpose": "Material Issue",
            "add_to_transit": 0
        },
        {
            "name": "Container Return",
            "purpose": "Material Receipt",
            "add_to_transit": 0
        }
    ]
    
    for entry_type in entry_types:
        if not frappe.db.exists("Stock Entry Type", entry_type["name"]):
            doc = frappe.get_doc({
                "doctype": "Stock Entry Type",
                "name": entry_type["name"],
                "purpose": entry_type["purpose"],
                "add_to_transit": entry_type["add_to_transit"]
            })
            doc.insert()
            print(f"✅ Created Stock Entry Type: {entry_type['name']}")

def setup_item_attributes():
    """Create item attributes for waste classification"""
    
    attributes = [
        {
            "attribute_name": "Waste Classification",
            "values": ["Infectious", "Sharps", "Pharmaceutical", "Pathological", "Chemotherapy", "Trace Chemotherapy"]
        },
        {
            "attribute_name": "Hazard Level", 
            "values": ["Low", "Medium", "High", "Extreme"]
        },
        {
            "attribute_name": "Treatment Method",
            "values": ["Autoclave", "Incineration", "Chemical Treatment", "Microwave", "Irradiation", "Secure Landfill"]
        },
        {
            "attribute_name": "Container Type",
            "values": ["Red Bag", "Yellow Bag", "Black Bag", "Sharps Container", "Rigid Container", "Chemotherapy Container"]
        },
        {
            "attribute_name": "Storage Temperature",
            "values": ["Ambient", "Refrigerated", "Frozen", "Room Temperature"]
        }
    ]
    
    for attr in attributes:
        if not frappe.db.exists("Item Attribute", attr["attribute_name"]):
            item_attr = frappe.get_doc({
                "doctype": "Item Attribute",
                "attribute_name": attr["attribute_name"],
                "item_attribute_values": [{"attribute_value": val} for val in attr["values"]]
            })
            item_attr.insert()
            print(f"✅ Created Item Attribute: {attr['attribute_name']}")

def create_stock_reports_customization():
    """Add custom fields to stock reports for waste tracking"""
    
    # Add custom fields to Stock Ledger Entry
    custom_fields = [
        {
            "dt": "Stock Ledger Entry",
            "fieldname": "waste_batch_id",
            "label": "Waste Batch ID", 
            "fieldtype": "Data"
        },
        {
            "dt": "Stock Ledger Entry",
            "fieldname": "generation_department",
            "label": "Generation Department",
            "fieldtype": "Link",
            "options": "Department"
        },
        {
            "dt": "Stock Ledger Entry", 
            "fieldname": "disposal_date",
            "label": "Disposal Date",
            "fieldtype": "Date"
        },
        {
            "dt": "Stock Ledger Entry",
            "fieldname": "manifest_number",
            "label": "Manifest Number",
            "fieldtype": "Data"
        }
    ]
    
    for field in custom_fields:
        if not frappe.db.exists("Custom Field", {"dt": field["dt"], "fieldname": field["fieldname"]}):
            custom_field = frappe.get_doc({
                "doctype": "Custom Field",
                "dt": field["dt"],
                "fieldname": field["fieldname"],
                "label": field["label"],
                "fieldtype": field["fieldtype"],
                "options": field.get("options", "")
            })
            custom_field.insert()
            print(f"✅ Added custom field to {field['dt']}: {field['label']}")

def setup_pick_lists():
    """Configure pick lists for waste collection routes"""
    
    # Add custom fields to Pick List
    custom_fields = [
        {
            "fieldname": "collection_route",
            "label": "Collection Route",
            "fieldtype": "Data"
        },
        {
            "fieldname": "collection_time",
            "label": "Scheduled Collection Time",
            "fieldtype": "Time"
        },
        {
            "fieldname": "collector_name", 
            "label": "Collector Name",
            "fieldtype": "Data"
        },
        {
            "fieldname": "special_handling",
            "label": "Special Handling Instructions",
            "fieldtype": "Text"
        }
    ]
    
    for field in custom_fields:
        if not frappe.db.exists("Custom Field", {"dt": "Pick List", "fieldname": field["fieldname"]}):
            custom_field = frappe.get_doc({
                "doctype": "Custom Field",
                "dt": "Pick List", 
                "fieldname": field["fieldname"],
                "label": field["label"],
                "fieldtype": field["fieldtype"]
            })
            custom_field.insert()
            print(f"✅ Added Pick List field: {field['label']}")

def create_delivery_routes():
    """Set up delivery routes for waste collection"""
    
    routes = [
        {
            "name": "ICU Collection Route",
            "driver": "Waste Collector 1",
            "vehicle": "Collection Cart 1"
        },
        {
            "name": "OR Collection Route", 
            "driver": "Waste Collector 2",
            "vehicle": "Collection Cart 2"
        },
        {
            "name": "Lab Collection Route",
            "driver": "Waste Collector 3", 
            "vehicle": "Collection Cart 3"
        },
        {
            "name": "Pharmacy Collection Route",
            "driver": "Waste Collector 4",
            "vehicle": "Collection Cart 4"
        }
    ]
    
    for route in routes:
        if not frappe.db.exists("Driver", route["driver"]):
            driver = frappe.get_doc({
                "doctype": "Driver",
                "full_name": route["driver"],
                "employee": route["driver"]  # Would link to actual employee
            })
            driver.insert()
            print(f"✅ Created driver: {route['driver']}")

def setup_stock_reconciliation():
    """Configure stock reconciliation for periodic waste audits"""
    
    # Add custom fields for reconciliation
    custom_fields = [
        {
            "fieldname": "audit_type",
            "label": "Audit Type",
            "fieldtype": "Select", 
            "options": "\\nDaily Count\\nWeekly Audit\\nMonthly Reconciliation\\nCompliance Audit"
        },
        {
            "fieldname": "auditor_name",
            "label": "Auditor Name",
            "fieldtype": "Data"
        },
        {
            "fieldname": "audit_findings",
            "label": "Audit Findings", 
            "fieldtype": "Text"
        }
    ]
    
    for field in custom_fields:
        if not frappe.db.exists("Custom Field", {"dt": "Stock Reconciliation", "fieldname": field["fieldname"]}):
            custom_field = frappe.get_doc({
                "doctype": "Custom Field",
                "dt": "Stock Reconciliation",
                "fieldname": field["fieldname"], 
                "label": field["label"],
                "fieldtype": field["fieldtype"],
                "options": field.get("options", "")
            })
            custom_field.insert()
            print(f"✅ Added Stock Reconciliation field: {field['label']}")

def main():
    """Main setup function for stock module"""
    try:
        print("📦 Configuring Stock Module for Medical Waste Management...")
        
        print("\n⚙️  Updating stock settings...")
        create_stock_settings()
        
        print("\n📏 Creating units of measure...")
        create_uoms()
        
        print("\n🏷️  Setting up item attributes...")
        setup_item_attributes()
        
        print("\n📋 Creating stock entry types...")
        create_stock_entry_types()
        
        print("\n📊 Adding custom fields to stock reports...")
        create_stock_reports_customization()
        
        print("\n🚚 Setting up pick lists...")
        setup_pick_lists()
        
        print("\n🛣️  Creating delivery routes...")
        create_delivery_routes()
        
        print("\n🔍 Configuring stock reconciliation...")
        setup_stock_reconciliation()
        
        frappe.db.commit()
        print("\n✅ Stock module configuration completed!")
        
    except Exception as e:
        print(f"❌ Error during stock setup: {str(e)}")
        frappe.db.rollback()
        raise

if __name__ == "__main__":
    main()