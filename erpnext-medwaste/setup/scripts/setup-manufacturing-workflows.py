#!/usr/bin/env python3
"""
Medical Waste Manufacturing Module Configuration
Sets up waste treatment and processing workflows
"""

import frappe
from frappe import _

def create_waste_treatment_items():
    """Create items for waste treatment processes"""
    
    treatment_items = [
        {
            "item_code": "AUTOCLAVE-SERVICE",
            "item_name": "Autoclave Treatment Service",
            "item_group": "Services",
            "stock_uom": "Hour",
            "is_stock_item": 0,
            "is_service_item": 1
        },
        {
            "item_code": "INCINERATION-SERVICE",
            "item_name": "Incineration Treatment Service", 
            "item_group": "Services",
            "stock_uom": "Kg",
            "is_stock_item": 0,
            "is_service_item": 1
        },
        {
            "item_code": "CHEMICAL-TREATMENT",
            "item_name": "Chemical Treatment Service",
            "item_group": "Services", 
            "stock_uom": "Liter",
            "is_stock_item": 0,
            "is_service_item": 1
        },
        {
            "item_code": "MICROWAVE-TREATMENT",
            "item_name": "Microwave Treatment Service",
            "item_group": "Services",
            "stock_uom": "Kg", 
            "is_stock_item": 0,
            "is_service_item": 1
        }
    ]
    
    for item_data in treatment_items:
        if not frappe.db.exists("Item", item_data["item_code"]):
            item = frappe.get_doc({
                "doctype": "Item",
                "item_code": item_data["item_code"],
                "item_name": item_data["item_name"],
                "item_group": item_data["item_group"],
                "stock_uom": item_data["stock_uom"],
                "is_stock_item": item_data["is_stock_item"],
                "is_service_item": item_data.get("is_service_item", 0)
            })
            item.insert()
            print(f"✅ Created treatment item: {item_data['item_name']}")

def create_workstations():
    """Create workstations for waste treatment"""
    
    workstations = [
        {
            "workstation_name": "Autoclave Station 1",
            "production_capacity": 50,
            "hour_rate_labour": 25.0,
            "hour_rate_electricity": 5.0
        },
        {
            "workstation_name": "Autoclave Station 2", 
            "production_capacity": 50,
            "hour_rate_labour": 25.0,
            "hour_rate_electricity": 5.0
        },
        {
            "workstation_name": "Incineration Facility",
            "production_capacity": 100,
            "hour_rate_labour": 50.0,
            "hour_rate_electricity": 15.0
        },
        {
            "workstation_name": "Chemical Treatment Area",
            "production_capacity": 75,
            "hour_rate_labour": 35.0,
            "hour_rate_electricity": 8.0
        },
        {
            "workstation_name": "Microwave Treatment Unit",
            "production_capacity": 30,
            "hour_rate_labour": 20.0,
            "hour_rate_electricity": 10.0
        },
        {
            "workstation_name": "Sorting and Segregation",
            "production_capacity": 200,
            "hour_rate_labour": 15.0,
            "hour_rate_electricity": 2.0
        }
    ]
    
    for ws_data in workstations:
        if not frappe.db.exists("Workstation", ws_data["workstation_name"]):
            workstation = frappe.get_doc({
                "doctype": "Workstation",
                "workstation_name": ws_data["workstation_name"],
                "production_capacity": ws_data["production_capacity"],
                "hour_rate_labour": ws_data["hour_rate_labour"],
                "hour_rate_electricity": ws_data["hour_rate_electricity"]
            })
            workstation.insert()
            print(f"✅ Created workstation: {ws_data['workstation_name']}")

def create_operations():
    """Create standard operations for waste treatment"""
    
    operations = [
        {
            "operation": "Waste Sorting",
            "description": "Sort and segregate waste by type and classification",
            "workstation": "Sorting and Segregation"
        },
        {
            "operation": "Autoclave Loading",
            "description": "Load waste into autoclave chamber",
            "workstation": "Autoclave Station 1"
        },
        {
            "operation": "Steam Sterilization",
            "description": "High-pressure steam sterilization process",
            "workstation": "Autoclave Station 1"
        },
        {
            "operation": "Autoclave Unloading",
            "description": "Remove treated waste from autoclave",
            "workstation": "Autoclave Station 1"
        },
        {
            "operation": "Incineration Prep",
            "description": "Prepare waste for incineration process",
            "workstation": "Incineration Facility"
        },
        {
            "operation": "High-Temp Incineration",
            "description": "Incinerate waste at high temperature",
            "workstation": "Incineration Facility"
        },
        {
            "operation": "Chemical Treatment",
            "description": "Chemical disinfection and treatment",
            "workstation": "Chemical Treatment Area"
        },
        {
            "operation": "Microwave Treatment",
            "description": "Moist heat and steam microwave treatment",
            "workstation": "Microwave Treatment Unit"
        },
        {
            "operation": "Final Inspection",
            "description": "Quality check of treated waste",
            "workstation": "Sorting and Segregation"
        },
        {
            "operation": "Documentation",
            "description": "Complete treatment certificates and manifests",
            "workstation": "Sorting and Segregation"
        }
    ]
    
    for op_data in operations:
        if not frappe.db.exists("Operation", op_data["operation"]):
            operation = frappe.get_doc({
                "doctype": "Operation",
                "operation": op_data["operation"],
                "description": op_data["description"],
                "workstation": op_data["workstation"]
            })
            operation.insert()
            print(f"✅ Created operation: {op_data['operation']}")

def create_routing_templates():
    """Create routing templates for different waste treatment methods"""
    
    routings = [
        {
            "routing": "Infectious Waste - Autoclave Treatment",
            "operations": [
                {"operation": "Waste Sorting", "time_in_mins": 10},
                {"operation": "Autoclave Loading", "time_in_mins": 15},
                {"operation": "Steam Sterilization", "time_in_mins": 60},
                {"operation": "Autoclave Unloading", "time_in_mins": 15},
                {"operation": "Final Inspection", "time_in_mins": 5},
                {"operation": "Documentation", "time_in_mins": 10}
            ]
        },
        {
            "routing": "Pharmaceutical Waste - Incineration",
            "operations": [
                {"operation": "Waste Sorting", "time_in_mins": 15},
                {"operation": "Incineration Prep", "time_in_mins": 20},
                {"operation": "High-Temp Incineration", "time_in_mins": 120},
                {"operation": "Final Inspection", "time_in_mins": 10},
                {"operation": "Documentation", "time_in_mins": 15}
            ]
        },
        {
            "routing": "Laboratory Waste - Chemical Treatment",
            "operations": [
                {"operation": "Waste Sorting", "time_in_mins": 20},
                {"operation": "Chemical Treatment", "time_in_mins": 90},
                {"operation": "Final Inspection", "time_in_mins": 10},
                {"operation": "Documentation", "time_in_mins": 10}
            ]
        },
        {
            "routing": "Sharps Waste - Microwave Treatment",
            "operations": [
                {"operation": "Waste Sorting", "time_in_mins": 5},
                {"operation": "Microwave Treatment", "time_in_mins": 45},
                {"operation": "Final Inspection", "time_in_mins": 5},
                {"operation": "Documentation", "time_in_mins": 10}
            ]
        }
    ]
    
    for routing_data in routings:
        if not frappe.db.exists("Routing", routing_data["routing"]):
            routing = frappe.get_doc({
                "doctype": "Routing",
                "routing": routing_data["routing"],
                "operations": [
                    {
                        "operation": op["operation"],
                        "time_in_mins": op["time_in_mins"],
                        "workstation": frappe.db.get_value("Operation", op["operation"], "workstation")
                    }
                    for op in routing_data["operations"]
                ]
            })
            routing.insert()
            print(f"✅ Created routing: {routing_data['routing']}")

def create_bom_templates():
    """Create Bill of Materials for waste treatment processes"""
    
    boms = [
        {
            "item": "AUTOCLAVE-SERVICE",
            "routing": "Infectious Waste - Autoclave Treatment",
            "raw_materials": [
                {"item_code": "RB-001", "qty": 1, "uom": "Nos"}  # Red Bag input
            ]
        },
        {
            "item": "INCINERATION-SERVICE", 
            "routing": "Pharmaceutical Waste - Incineration",
            "raw_materials": [
                {"item_code": "YB-001", "qty": 1, "uom": "Nos"}  # Yellow Bag input
            ]
        },
        {
            "item": "CHEMICAL-TREATMENT",
            "routing": "Laboratory Waste - Chemical Treatment", 
            "raw_materials": [
                {"item_code": "RB-001", "qty": 1, "uom": "Nos"}  # Red Bag input
            ]
        },
        {
            "item": "MICROWAVE-TREATMENT",
            "routing": "Sharps Waste - Microwave Treatment",
            "raw_materials": [
                {"item_code": "SC-001", "qty": 1, "uom": "Nos"}  # Sharps Container input
            ]
        }
    ]
    
    for bom_data in boms:
        if not frappe.db.exists("BOM", {"item": bom_data["item"]}):
            bom = frappe.get_doc({
                "doctype": "BOM",
                "item": bom_data["item"],
                "routing": bom_data["routing"],
                "items": [
                    {
                        "item_code": rm["item_code"],
                        "qty": rm["qty"],
                        "uom": rm["uom"]
                    }
                    for rm in bom_data["raw_materials"]
                ]
            })
            bom.insert()
            bom.submit()
            print(f"✅ Created BOM: {bom_data['item']}")

def setup_quality_inspections():
    """Set up quality inspection templates for waste treatment"""
    
    # Add custom fields to Quality Inspection
    custom_fields = [
        {
            "fieldname": "treatment_effectiveness",
            "label": "Treatment Effectiveness (%)",
            "fieldtype": "Percent"
        },
        {
            "fieldname": "sterilization_indicator",
            "label": "Sterilization Indicator Result",
            "fieldtype": "Select",
            "options": "\\nPass\\nFail\\nInconclusive"
        },
        {
            "fieldname": "biological_indicator", 
            "label": "Biological Indicator Result",
            "fieldtype": "Select",
            "options": "\\nNegative\\nPositive\\nNot Tested"
        },
        {
            "fieldname": "temperature_log",
            "label": "Temperature Log Verified",
            "fieldtype": "Check"
        },
        {
            "fieldname": "pressure_log",
            "label": "Pressure Log Verified", 
            "fieldtype": "Check"
        },
        {
            "fieldname": "treatment_duration",
            "label": "Treatment Duration (minutes)",
            "fieldtype": "Float"
        }
    ]
    
    for field in custom_fields:
        if not frappe.db.exists("Custom Field", {"dt": "Quality Inspection", "fieldname": field["fieldname"]}):
            custom_field = frappe.get_doc({
                "doctype": "Custom Field",
                "dt": "Quality Inspection",
                "fieldname": field["fieldname"],
                "label": field["label"],
                "fieldtype": field["fieldtype"],
                "options": field.get("options", "")
            })
            custom_field.insert()
            print(f"✅ Added Quality Inspection field: {field['label']}")

def create_work_order_templates():
    """Create work order templates for common waste treatment scenarios"""
    
    # Add custom fields to Work Order
    custom_fields = [
        {
            "fieldname": "waste_batch_number",
            "label": "Waste Batch Number",
            "fieldtype": "Data"
        },
        {
            "fieldname": "manifest_reference",
            "label": "Manifest Reference",
            "fieldtype": "Link",
            "options": "Medical Waste Manifest"
        },
        {
            "fieldname": "treatment_priority",
            "label": "Treatment Priority",
            "fieldtype": "Select",
            "options": "\\nLow\\nNormal\\nHigh\\nUrgent"
        },
        {
            "fieldname": "special_instructions",
            "label": "Special Treatment Instructions",
            "fieldtype": "Text"
        },
        {
            "fieldname": "regulatory_requirements",
            "label": "Regulatory Requirements",
            "fieldtype": "Text"
        }
    ]
    
    for field in custom_fields:
        if not frappe.db.exists("Custom Field", {"dt": "Work Order", "fieldname": field["fieldname"]}):
            custom_field = frappe.get_doc({
                "doctype": "Custom Field",
                "dt": "Work Order",
                "fieldname": field["fieldname"],
                "label": field["label"],
                "fieldtype": field["fieldtype"],
                "options": field.get("options", "")
            })
            custom_field.insert()
            print(f"✅ Added Work Order field: {field['label']}")

def main():
    """Main setup function for manufacturing workflows"""
    try:
        print("🏭 Setting up Manufacturing Workflows for Medical Waste Treatment...")
        
        print("\n🛠️  Creating treatment service items...")
        create_waste_treatment_items()
        
        print("\n🏭 Setting up workstations...")
        create_workstations()
        
        print("\n⚙️  Creating operations...")
        create_operations()
        
        print("\n🛣️  Creating routing templates...")
        create_routing_templates()
        
        print("\n📋 Creating BOM templates...")
        create_bom_templates()
        
        print("\n🔍 Setting up quality inspections...")
        setup_quality_inspections()
        
        print("\n📝 Creating work order templates...")
        create_work_order_templates()
        
        frappe.db.commit()
        print("\n✅ Manufacturing workflows setup completed!")
        
    except Exception as e:
        print(f"❌ Error during manufacturing setup: {str(e)}")
        frappe.db.rollback()
        raise

if __name__ == "__main__":
    main()