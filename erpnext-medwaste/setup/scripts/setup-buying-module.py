#!/usr/bin/env python3
"""
Medical Waste Buying Module Configuration
Sets up vendor management for waste disposal partners
"""

import frappe
from frappe import _

def create_supplier_groups():
    """Create supplier groups for waste disposal vendors"""
    
    supplier_groups = [
        "Medical Waste Disposal",
        "Sharps Disposal", 
        "Pharmaceutical Waste Disposal",
        "Pathological Waste Disposal",
        "Chemotherapy Waste Disposal",
        "Hazmat Transportation",
        "Treatment Facilities",
        "Consulting Services"
    ]
    
    for group_name in supplier_groups:
        if not frappe.db.exists("Supplier Group", group_name):
            supplier_group = frappe.get_doc({
                "doctype": "Supplier Group",
                "supplier_group_name": group_name
            })
            supplier_group.insert()
            print(f"✅ Created supplier group: {group_name}")

def setup_supplier_custom_fields():
    """Add custom fields to Supplier for waste management"""
    
    custom_fields = [
        {
            "fieldname": "license_section",
            "label": "Licensing and Compliance",
            "fieldtype": "Section Break"
        },
        {
            "fieldname": "dot_license_number",
            "label": "DOT License Number",
            "fieldtype": "Data"
        },
        {
            "fieldname": "dot_license_expiry",
            "label": "DOT License Expiry",
            "fieldtype": "Date"
        },
        {
            "fieldname": "cb_license1",
            "fieldtype": "Column Break"
        },
        {
            "fieldname": "epa_permit_number",
            "label": "EPA Permit Number", 
            "fieldtype": "Data"
        },
        {
            "fieldname": "epa_permit_expiry",
            "label": "EPA Permit Expiry",
            "fieldtype": "Date"
        },
        {
            "fieldname": "certification_section",
            "label": "Certifications",
            "fieldtype": "Section Break"
        },
        {
            "fieldname": "waste_types_handled",
            "label": "Waste Types Handled",
            "fieldtype": "Table",
            "options": "Supplier Waste Type"
        },
        {
            "fieldname": "service_section",
            "label": "Service Information",
            "fieldtype": "Section Break"
        },
        {
            "fieldname": "pickup_frequency",
            "label": "Pickup Frequency",
            "fieldtype": "Select",
            "options": "\\nDaily\\nWeekly\\nBi-weekly\\nMonthly\\nOn-demand"
        },
        {
            "fieldname": "service_area",
            "label": "Service Area",
            "fieldtype": "Text"
        },
        {
            "fieldname": "cb_service1",
            "fieldtype": "Column Break"
        },
        {
            "fieldname": "emergency_contact",
            "label": "Emergency Contact",
            "fieldtype": "Data"
        },
        {
            "fieldname": "emergency_phone",
            "label": "Emergency Phone",
            "fieldtype": "Data"
        },
        {
            "fieldname": "compliance_section",
            "label": "Compliance Monitoring",
            "fieldtype": "Section Break"
        },
        {
            "fieldname": "last_audit_date",
            "label": "Last Audit Date",
            "fieldtype": "Date"
        },
        {
            "fieldname": "audit_score",
            "label": "Latest Audit Score",
            "fieldtype": "Percent"
        },
        {
            "fieldname": "cb_compliance1",
            "fieldtype": "Column Break"
        },
        {
            "fieldname": "insurance_amount",
            "label": "Insurance Coverage Amount",
            "fieldtype": "Currency"
        },
        {
            "fieldname": "insurance_expiry",
            "label": "Insurance Expiry",
            "fieldtype": "Date"
        }
    ]
    
    for field in custom_fields:
        if not frappe.db.exists("Custom Field", {"dt": "Supplier", "fieldname": field["fieldname"]}):
            custom_field = frappe.get_doc({
                "doctype": "Custom Field",
                "dt": "Supplier",
                "fieldname": field["fieldname"],
                "label": field["label"],
                "fieldtype": field["fieldtype"],
                "options": field.get("options", "")
            })
            custom_field.insert()
            print(f"✅ Added Supplier field: {field['label']}")

def create_supplier_waste_type_table():
    """Create child table for supplier waste types"""
    
    if frappe.db.exists("DocType", "Supplier Waste Type"):
        print("⚠️  Supplier Waste Type DocType already exists")
        return
    
    doctype = frappe.get_doc({
        "doctype": "DocType",
        "name": "Supplier Waste Type",
        "module": "Buying",
        "custom": 1,
        "istable": 1,
        "fields": [
            {
                "fieldname": "waste_classification",
                "label": "Waste Classification",
                "fieldtype": "Select",
                "options": "\\nInfectious\\nSharps\\nPharmaceutical\\nPathological\\nChemotherapy\\nTrace Chemotherapy",
                "reqd": 1
            },
            {
                "fieldname": "treatment_method",
                "label": "Treatment Method",
                "fieldtype": "Select", 
                "options": "\\nAutoclave\\nIncineration\\nChemical Treatment\\nMicrowave\\nIrradiation\\nSecure Landfill"
            },
            {
                "fieldname": "permit_required",
                "label": "Special Permit Required",
                "fieldtype": "Check"
            },
            {
                "fieldname": "rate_per_unit",
                "label": "Rate per Unit",
                "fieldtype": "Currency"
            },
            {
                "fieldname": "minimum_pickup",
                "label": "Minimum Pickup Quantity",
                "fieldtype": "Float"
            }
        ]
    })
    
    doctype.insert()
    print("✅ Created Supplier Waste Type DocType")

def create_sample_suppliers():
    """Create sample waste disposal suppliers"""
    
    suppliers = [
        {
            "supplier_name": "BioWaste Solutions Inc.",
            "supplier_group": "Medical Waste Disposal",
            "supplier_type": "Company",
            "dot_license_number": "US-DOT-12345",
            "epa_permit_number": "EPA-MW-6789",
            "pickup_frequency": "Weekly",
            "emergency_contact": "John Smith",
            "emergency_phone": "1-800-BIOWASTE"
        },
        {
            "supplier_name": "SafeSharp Disposal LLC",
            "supplier_group": "Sharps Disposal",
            "supplier_type": "Company", 
            "dot_license_number": "US-DOT-54321",
            "epa_permit_number": "EPA-SH-9876",
            "pickup_frequency": "Bi-weekly",
            "emergency_contact": "Mary Johnson",
            "emergency_phone": "1-800-SAFESHARP"
        },
        {
            "supplier_name": "PharmaWaste Pro",
            "supplier_group": "Pharmaceutical Waste Disposal",
            "supplier_type": "Company",
            "dot_license_number": "US-DOT-11111",
            "epa_permit_number": "EPA-PH-2222",
            "pickup_frequency": "Monthly",
            "emergency_contact": "Dr. Robert Brown",
            "emergency_phone": "1-800-PHARMAWASTE"
        },
        {
            "supplier_name": "ChemoSafe Disposal",
            "supplier_group": "Chemotherapy Waste Disposal", 
            "supplier_type": "Company",
            "dot_license_number": "US-DOT-33333",
            "epa_permit_number": "EPA-CH-4444",
            "pickup_frequency": "Weekly",
            "emergency_contact": "Lisa Wilson",
            "emergency_phone": "1-800-CHEMOSAFE"
        }
    ]
    
    for supplier_data in suppliers:
        if not frappe.db.exists("Supplier", supplier_data["supplier_name"]):
            supplier = frappe.get_doc({
                "doctype": "Supplier",
                "supplier_name": supplier_data["supplier_name"],
                "supplier_group": supplier_data["supplier_group"],
                "supplier_type": supplier_data["supplier_type"],
                "dot_license_number": supplier_data["dot_license_number"],
                "epa_permit_number": supplier_data["epa_permit_number"],
                "pickup_frequency": supplier_data["pickup_frequency"],
                "emergency_contact": supplier_data["emergency_contact"],
                "emergency_phone": supplier_data["emergency_phone"]
            })
            supplier.insert()
            print(f"✅ Created supplier: {supplier_data['supplier_name']}")

def setup_purchase_order_custom_fields():
    """Add custom fields to Purchase Order for waste disposal"""
    
    custom_fields = [
        {
            "fieldname": "waste_disposal_section",
            "label": "Waste Disposal Information",
            "fieldtype": "Section Break"
        },
        {
            "fieldname": "pickup_date",
            "label": "Scheduled Pickup Date",
            "fieldtype": "Date"
        },
        {
            "fieldname": "pickup_time",
            "label": "Pickup Time Window",
            "fieldtype": "Data"
        },
        {
            "fieldname": "cb_disposal1",
            "fieldtype": "Column Break"
        },
        {
            "fieldname": "pickup_location",
            "label": "Pickup Location",
            "fieldtype": "Data"
        },
        {
            "fieldname": "special_instructions",
            "label": "Special Handling Instructions",
            "fieldtype": "Text"
        },
        {
            "fieldname": "manifest_section", 
            "label": "Manifest Information",
            "fieldtype": "Section Break"
        },
        {
            "fieldname": "requires_manifest",
            "label": "Requires DOT Manifest",
            "fieldtype": "Check"
        },
        {
            "fieldname": "manifest_number",
            "label": "Manifest Number",
            "fieldtype": "Data"
        },
        {
            "fieldname": "cb_manifest1",
            "fieldtype": "Column Break"
        },
        {
            "fieldname": "treatment_facility",
            "label": "Treatment Facility",
            "fieldtype": "Data"
        },
        {
            "fieldname": "treatment_method",
            "label": "Treatment Method",
            "fieldtype": "Select",
            "options": "\\nAutoclave\\nIncineration\\nChemical Treatment\\nMicrowave\\nIrradiation"
        }
    ]
    
    for field in custom_fields:
        if not frappe.db.exists("Custom Field", {"dt": "Purchase Order", "fieldname": field["fieldname"]}):
            custom_field = frappe.get_doc({
                "doctype": "Custom Field",
                "dt": "Purchase Order",
                "fieldname": field["fieldname"],
                "label": field["label"],
                "fieldtype": field["fieldtype"],
                "options": field.get("options", "")
            })
            custom_field.insert()
            print(f"✅ Added Purchase Order field: {field['label']}")

def create_supplier_quotation_templates():
    """Set up supplier quotation templates for waste disposal services"""
    
    # Add custom fields to Supplier Quotation
    custom_fields = [
        {
            "fieldname": "service_details_section",
            "label": "Service Details",
            "fieldtype": "Section Break"
        },
        {
            "fieldname": "service_type",
            "label": "Service Type",
            "fieldtype": "Select",
            "options": "\\nRegular Pickup\\nEmergency Pickup\\nOne-time Removal\\nConsulting\\nTraining"
        },
        {
            "fieldname": "coverage_area",
            "label": "Coverage Area",
            "fieldtype": "Data"
        },
        {
            "fieldname": "cb_service1",
            "fieldtype": "Column Break"
        },
        {
            "fieldname": "response_time",
            "label": "Response Time (Hours)",
            "fieldtype": "Float"
        },
        {
            "fieldname": "minimum_order",
            "label": "Minimum Order Value",
            "fieldtype": "Currency"
        },
        {
            "fieldname": "pricing_section",
            "label": "Pricing Structure",
            "fieldtype": "Section Break"
        },
        {
            "fieldname": "pricing_model",
            "label": "Pricing Model",
            "fieldtype": "Select",
            "options": "\\nPer Container\\nPer Pound\\nPer Pickup\\nFlat Rate\\nTiered Pricing"
        },
        {
            "fieldname": "fuel_surcharge",
            "label": "Fuel Surcharge (%)",
            "fieldtype": "Percent"
        },
        {
            "fieldname": "cb_pricing1",
            "fieldtype": "Column Break"
        },
        {
            "fieldname": "emergency_rate_multiplier",
            "label": "Emergency Rate Multiplier",
            "fieldtype": "Float",
            "default": 1.5
        },
        {
            "fieldname": "volume_discount",
            "label": "Volume Discount Available",
            "fieldtype": "Check"
        }
    ]
    
    for field in custom_fields:
        if not frappe.db.exists("Custom Field", {"dt": "Supplier Quotation", "fieldname": field["fieldname"]}):
            custom_field = frappe.get_doc({
                "doctype": "Custom Field",
                "dt": "Supplier Quotation",
                "fieldname": field["fieldname"],
                "label": field["label"],
                "fieldtype": field["fieldtype"],
                "options": field.get("options", ""),
                "default": field.get("default", "")
            })
            custom_field.insert()
            print(f"✅ Added Supplier Quotation field: {field['label']}")

def setup_purchase_receipt_tracking():
    """Set up purchase receipt for waste disposal service confirmation"""
    
    # Add custom fields to Purchase Receipt
    custom_fields = [
        {
            "fieldname": "disposal_confirmation_section",
            "label": "Disposal Confirmation",
            "fieldtype": "Section Break"
        },
        {
            "fieldname": "actual_pickup_date",
            "label": "Actual Pickup Date",
            "fieldtype": "Date"
        },
        {
            "fieldname": "pickup_confirmed_by",
            "label": "Pickup Confirmed By",
            "fieldtype": "Data"
        },
        {
            "fieldname": "cb_confirmation1",
            "fieldtype": "Column Break"
        },
        {
            "fieldname": "vehicle_id",
            "label": "Collection Vehicle ID",
            "fieldtype": "Data"
        },
        {
            "fieldname": "driver_name",
            "label": "Driver Name",
            "fieldtype": "Data"
        },
        {
            "fieldname": "treatment_section",
            "label": "Treatment Confirmation",
            "fieldtype": "Section Break"
        },
        {
            "fieldname": "treatment_date",
            "label": "Treatment Date",
            "fieldtype": "Date"
        },
        {
            "fieldname": "treatment_facility_name",
            "label": "Treatment Facility Name",
            "fieldtype": "Data"
        },
        {
            "fieldname": "cb_treatment1",
            "fieldtype": "Column Break"
        },
        {
            "fieldname": "certificate_number",
            "label": "Certificate of Destruction Number",
            "fieldtype": "Data"
        },
        {
            "fieldname": "certificate_received",
            "label": "Certificate Received",
            "fieldtype": "Check"
        }
    ]
    
    for field in custom_fields:
        if not frappe.db.exists("Custom Field", {"dt": "Purchase Receipt", "fieldname": field["fieldname"]}):
            custom_field = frappe.get_doc({
                "doctype": "Custom Field",
                "dt": "Purchase Receipt",
                "fieldname": field["fieldname"],
                "label": field["label"],
                "fieldtype": field["fieldtype"]
            })
            custom_field.insert()
            print(f"✅ Added Purchase Receipt field: {field['label']}")

def create_vendor_evaluation_criteria():
    """Set up vendor evaluation criteria for waste disposal partners"""
    
    # This would typically be configured through Supplier Scorecard
    # Adding custom fields to support waste-specific evaluation
    
    # Add to Supplier Scorecard if it exists
    if frappe.db.exists("DocType", "Supplier Scorecard"):
        custom_fields = [
            {
                "fieldname": "compliance_score",
                "label": "Compliance Score (%)",
                "fieldtype": "Percent"
            },
            {
                "fieldname": "safety_record",
                "label": "Safety Record Score (%)",
                "fieldtype": "Percent"
            },
            {
                "fieldname": "environmental_score",
                "label": "Environmental Score (%)",
                "fieldtype": "Percent"
            },
            {
                "fieldname": "response_time_score",
                "label": "Response Time Score (%)",
                "fieldtype": "Percent"
            }
        ]
        
        for field in custom_fields:
            if not frappe.db.exists("Custom Field", {"dt": "Supplier Scorecard", "fieldname": field["fieldname"]}):
                custom_field = frappe.get_doc({
                    "doctype": "Custom Field",
                    "dt": "Supplier Scorecard",
                    "fieldname": field["fieldname"],
                    "label": field["label"],
                    "fieldtype": field["fieldtype"]
                })
                custom_field.insert()
                print(f"✅ Added Supplier Scorecard field: {field['label']}")

def main():
    """Main setup function for buying module"""
    try:
        print("🛒 Setting up Buying Module for Waste Disposal Partners...")
        
        print("\n🏢 Creating supplier groups...")
        create_supplier_groups()
        
        print("\n📋 Creating supplier waste type table...")
        create_supplier_waste_type_table()
        
        print("\n⚙️  Setting up supplier custom fields...")
        setup_supplier_custom_fields()
        
        print("\n🏭 Creating sample suppliers...")
        create_sample_suppliers()
        
        print("\n📑 Setting up purchase order fields...")
        setup_purchase_order_custom_fields()
        
        print("\n💰 Setting up supplier quotation templates...")
        create_supplier_quotation_templates()
        
        print("\n📦 Setting up purchase receipt tracking...")
        setup_purchase_receipt_tracking()
        
        print("\n📊 Creating vendor evaluation criteria...")
        create_vendor_evaluation_criteria()
        
        frappe.db.commit()
        print("\n✅ Buying module setup completed!")
        
    except Exception as e:
        print(f"❌ Error during buying setup: {str(e)}")
        frappe.db.rollback()
        raise

if __name__ == "__main__":
    main()