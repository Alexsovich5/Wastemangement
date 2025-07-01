#!/usr/bin/env python3
"""
Medical Waste Custom DocTypes Creation
Creates specialized doctypes for medical waste compliance and tracking
"""

import frappe
from frappe import _

def create_medical_waste_manifest():
    """Create Medical Waste Manifest DocType"""
    
    if frappe.db.exists("DocType", "Medical Waste Manifest"):
        print("⚠️  Medical Waste Manifest DocType already exists")
        return
    
    doctype = frappe.get_doc({
        "doctype": "DocType",
        "name": "Medical Waste Manifest",
        "module": "Stock",
        "custom": 1,
        "is_submittable": 1,
        "naming_rule": "By fieldname",
        "autoname": "field:manifest_number",
        "title_field": "manifest_number",
        "fields": [
            # Basic Information
            {
                "fieldname": "manifest_number",
                "label": "Manifest Number",
                "fieldtype": "Data",
                "reqd": 1,
                "unique": 1
            },
            {
                "fieldname": "manifest_date",
                "label": "Manifest Date", 
                "fieldtype": "Date",
                "reqd": 1,
                "default": "Today"
            },
            {
                "fieldname": "cb1",
                "fieldtype": "Column Break"
            },
            {
                "fieldname": "status",
                "label": "Status",
                "fieldtype": "Select",
                "options": "\\nDraft\\nIn Transit\\nReceived\\nTreated\\nCompleted",
                "default": "Draft"
            },
            {
                "fieldname": "sb1",
                "fieldtype": "Section Break",
                "label": "Generator Information"
            },
            {
                "fieldname": "generator_name",
                "label": "Generator Name",
                "fieldtype": "Data",
                "reqd": 1
            },
            {
                "fieldname": "generator_address",
                "label": "Generator Address",
                "fieldtype": "Text",
                "reqd": 1
            },
            {
                "fieldname": "cb2",
                "fieldtype": "Column Break"
            },
            {
                "fieldname": "generator_epa_id",
                "label": "Generator EPA ID",
                "fieldtype": "Data"
            },
            {
                "fieldname": "generator_phone",
                "label": "Generator Phone",
                "fieldtype": "Data"
            },
            {
                "fieldname": "sb2",
                "fieldtype": "Section Break",
                "label": "Transporter Information"
            },
            {
                "fieldname": "transporter_name",
                "label": "Transporter Name",
                "fieldtype": "Data"
            },
            {
                "fieldname": "transporter_license",
                "label": "Transporter License",
                "fieldtype": "Data"
            },
            {
                "fieldname": "cb3",
                "fieldtype": "Column Break"
            },
            {
                "fieldname": "pickup_date",
                "label": "Pickup Date",
                "fieldtype": "Date"
            },
            {
                "fieldname": "driver_name",
                "label": "Driver Name",
                "fieldtype": "Data"
            },
            {
                "fieldname": "sb3",
                "fieldtype": "Section Break",
                "label": "Treatment Facility"
            },
            {
                "fieldname": "facility_name",
                "label": "Treatment Facility Name",
                "fieldtype": "Data"
            },
            {
                "fieldname": "facility_permit",
                "label": "Facility Permit Number",
                "fieldtype": "Data"
            },
            {
                "fieldname": "cb4",
                "fieldtype": "Column Break"
            },
            {
                "fieldname": "treatment_date",
                "label": "Treatment Date",
                "fieldtype": "Date"
            },
            {
                "fieldname": "treatment_method",
                "label": "Treatment Method",
                "fieldtype": "Select",
                "options": "\\nAutoclave\\nIncineration\\nChemical Treatment\\nMicrowave\\nIrradiation"
            },
            {
                "fieldname": "sb4",
                "fieldtype": "Section Break",
                "label": "Waste Items"
            },
            {
                "fieldname": "waste_items",
                "label": "Waste Items",
                "fieldtype": "Table",
                "options": "Medical Waste Manifest Item"
            },
            {
                "fieldname": "sb5",
                "fieldtype": "Section Break",
                "label": "Totals"
            },
            {
                "fieldname": "total_weight",
                "label": "Total Weight (lbs)",
                "fieldtype": "Float",
                "read_only": 1
            },
            {
                "fieldname": "cb5",
                "fieldtype": "Column Break"
            },
            {
                "fieldname": "total_containers",
                "label": "Total Containers",
                "fieldtype": "Int",
                "read_only": 1
            }
        ]
    })
    
    doctype.insert()
    print("✅ Created Medical Waste Manifest DocType")

def create_manifest_item_table():
    """Create child table for manifest items"""
    
    if frappe.db.exists("DocType", "Medical Waste Manifest Item"):
        print("⚠️  Medical Waste Manifest Item DocType already exists")
        return
    
    doctype = frappe.get_doc({
        "doctype": "DocType",
        "name": "Medical Waste Manifest Item",
        "module": "Stock",
        "custom": 1,
        "istable": 1,
        "fields": [
            {
                "fieldname": "item_code",
                "label": "Item Code",
                "fieldtype": "Link",
                "options": "Item",
                "reqd": 1
            },
            {
                "fieldname": "item_name",
                "label": "Item Name",
                "fieldtype": "Data",
                "fetch_from": "item_code.item_name",
                "read_only": 1
            },
            {
                "fieldname": "waste_classification",
                "label": "Waste Classification",
                "fieldtype": "Data",
                "fetch_from": "item_code.waste_classification",
                "read_only": 1
            },
            {
                "fieldname": "quantity",
                "label": "Quantity",
                "fieldtype": "Float",
                "reqd": 1
            },
            {
                "fieldname": "uom",
                "label": "UOM",
                "fieldtype": "Link",
                "options": "UOM",
                "fetch_from": "item_code.stock_uom"
            },
            {
                "fieldname": "weight_lbs",
                "label": "Weight (lbs)",
                "fieldtype": "Float"
            },
            {
                "fieldname": "container_type",
                "label": "Container Type",
                "fieldtype": "Data"
            },
            {
                "fieldname": "dot_code",
                "label": "DOT Code",
                "fieldtype": "Data"
            }
        ]
    })
    
    doctype.insert()
    print("✅ Created Medical Waste Manifest Item DocType")

def create_waste_container_tracking():
    """Create Waste Container Tracking DocType"""
    
    if frappe.db.exists("DocType", "Waste Container Tracking"):
        print("⚠️  Waste Container Tracking DocType already exists")
        return
    
    doctype = frappe.get_doc({
        "doctype": "DocType",
        "name": "Waste Container Tracking",
        "module": "Stock",
        "custom": 1,
        "naming_rule": "By fieldname",
        "autoname": "field:container_id",
        "title_field": "container_id",
        "fields": [
            {
                "fieldname": "container_id",
                "label": "Container ID",
                "fieldtype": "Data",
                "reqd": 1,
                "unique": 1
            },
            {
                "fieldname": "container_type",
                "label": "Container Type",
                "fieldtype": "Select",
                "options": "\\nRed Bag\\nYellow Bag\\nSharps Container\\nRigid Container\\nChemotherapy Container",
                "reqd": 1
            },
            {
                "fieldname": "cb1",
                "fieldtype": "Column Break"
            },
            {
                "fieldname": "size",
                "label": "Size",
                "fieldtype": "Data"
            },
            {
                "fieldname": "status",
                "label": "Status",
                "fieldtype": "Select",
                "options": "\\nEmpty\\nIn Use\\nFull\\nCollected\\nTreated\\nDisposed",
                "default": "Empty"
            },
            {
                "fieldname": "sb1",
                "fieldtype": "Section Break",
                "label": "Location Information"
            },
            {
                "fieldname": "current_location",
                "label": "Current Location",
                "fieldtype": "Link",
                "options": "Warehouse"
            },
            {
                "fieldname": "department",
                "label": "Department",
                "fieldtype": "Link",
                "options": "Department"
            },
            {
                "fieldname": "cb2",
                "fieldtype": "Column Break"
            },
            {
                "fieldname": "room_number",
                "label": "Room Number",
                "fieldtype": "Data"
            },
            {
                "fieldname": "assigned_to",
                "label": "Assigned To",
                "fieldtype": "Link",
                "options": "Employee"
            },
            {
                "fieldname": "sb2",
                "fieldtype": "Section Break",
                "label": "Fill Information"
            },
            {
                "fieldname": "fill_level",
                "label": "Fill Level (%)",
                "fieldtype": "Percent"
            },
            {
                "fieldname": "weight_kg",
                "label": "Weight (kg)",
                "fieldtype": "Float"
            },
            {
                "fieldname": "cb3",
                "fieldtype": "Column Break"
            },
            {
                "fieldname": "start_date",
                "label": "Start Date",
                "fieldtype": "Date"
            },
            {
                "fieldname": "full_date",
                "label": "Full Date",
                "fieldtype": "Date"
            },
            {
                "fieldname": "sb3",
                "fieldtype": "Section Break",
                "label": "Collection Information"
            },
            {
                "fieldname": "collection_date",
                "label": "Collection Date",
                "fieldtype": "Date"
            },
            {
                "fieldname": "collected_by",
                "label": "Collected By",
                "fieldtype": "Data"
            },
            {
                "fieldname": "cb4",
                "fieldtype": "Column Break"
            },
            {
                "fieldname": "manifest_number",
                "label": "Manifest Number",
                "fieldtype": "Link",
                "options": "Medical Waste Manifest"
            },
            {
                "fieldname": "treatment_date",
                "label": "Treatment Date",
                "fieldtype": "Date"
            }
        ]
    })
    
    doctype.insert()
    print("✅ Created Waste Container Tracking DocType")

def create_compliance_inspection():
    """Create Compliance Inspection DocType"""
    
    if frappe.db.exists("DocType", "Compliance Inspection"):
        print("⚠️  Compliance Inspection DocType already exists")
        return
    
    doctype = frappe.get_doc({
        "doctype": "DocType",
        "name": "Compliance Inspection",
        "module": "Stock",
        "custom": 1,
        "is_submittable": 1,
        "fields": [
            {
                "fieldname": "inspection_date",
                "label": "Inspection Date",
                "fieldtype": "Date",
                "reqd": 1,
                "default": "Today"
            },
            {
                "fieldname": "inspector_name",
                "label": "Inspector Name",
                "fieldtype": "Data",
                "reqd": 1
            },
            {
                "fieldname": "cb1",
                "fieldtype": "Column Break"
            },
            {
                "fieldname": "inspection_type",
                "label": "Inspection Type",
                "fieldtype": "Select",
                "options": "\\nInternal Audit\\nRegulatory Inspection\\nVendor Audit\\nCompliance Review",
                "reqd": 1
            },
            {
                "fieldname": "regulatory_agency",
                "label": "Regulatory Agency",
                "fieldtype": "Select",
                "options": "\\nOSHA\\nEPA\\nDOT\\nState Environmental\\nLocal Health Department"
            },
            {
                "fieldname": "sb1",
                "fieldtype": "Section Break",
                "label": "Areas Inspected"
            },
            {
                "fieldname": "areas_inspected",
                "label": "Areas Inspected",
                "fieldtype": "Table",
                "options": "Inspection Area"
            },
            {
                "fieldname": "sb2",
                "fieldtype": "Section Break",
                "label": "Findings"
            },
            {
                "fieldname": "overall_result",
                "label": "Overall Result",
                "fieldtype": "Select",
                "options": "\\nPass\\nPass with Minor Issues\\nFail\\nRequires Follow-up"
            },
            {
                "fieldname": "findings",
                "label": "Findings",
                "fieldtype": "Text"
            },
            {
                "fieldname": "cb2",
                "fieldtype": "Column Break"
            },
            {
                "fieldname": "corrective_actions",
                "label": "Corrective Actions Required",
                "fieldtype": "Text"
            },
            {
                "fieldname": "due_date",
                "label": "Corrective Action Due Date",
                "fieldtype": "Date"
            },
            {
                "fieldname": "sb3",
                "fieldtype": "Section Break",
                "label": "Follow-up"
            },
            {
                "fieldname": "follow_up_required",
                "label": "Follow-up Required",
                "fieldtype": "Check"
            },
            {
                "fieldname": "follow_up_date",
                "label": "Follow-up Date",
                "fieldtype": "Date"
            },
            {
                "fieldname": "cb3",
                "fieldtype": "Column Break"
            },
            {
                "fieldname": "responsible_person",
                "label": "Responsible Person",
                "fieldtype": "Link",
                "options": "Employee"
            },
            {
                "fieldname": "completion_status",
                "label": "Completion Status",
                "fieldtype": "Select",
                "options": "\\nPending\\nIn Progress\\nCompleted\\nOverdue"
            }
        ]
    })
    
    doctype.insert()
    print("✅ Created Compliance Inspection DocType")

def create_inspection_area_table():
    """Create child table for inspection areas"""
    
    if frappe.db.exists("DocType", "Inspection Area"):
        print("⚠️  Inspection Area DocType already exists")
        return
    
    doctype = frappe.get_doc({
        "doctype": "DocType",
        "name": "Inspection Area",
        "module": "Stock",
        "custom": 1,
        "istable": 1,
        "fields": [
            {
                "fieldname": "area_name",
                "label": "Area Name",
                "fieldtype": "Data",
                "reqd": 1
            },
            {
                "fieldname": "checklist_item",
                "label": "Checklist Item",
                "fieldtype": "Data",
                "reqd": 1
            },
            {
                "fieldname": "compliance_status",
                "label": "Compliance Status",
                "fieldtype": "Select",
                "options": "\\nCompliant\\nNon-Compliant\\nNeeds Improvement\\nN/A"
            },
            {
                "fieldname": "notes",
                "label": "Notes",
                "fieldtype": "Text"
            }
        ]
    })
    
    doctype.insert()
    print("✅ Created Inspection Area DocType")

def create_training_record():
    """Create Training Record DocType"""
    
    if frappe.db.exists("DocType", "Training Record"):
        print("⚠️  Training Record DocType already exists")
        return
    
    doctype = frappe.get_doc({
        "doctype": "DocType",
        "name": "Training Record",
        "module": "HR",
        "custom": 1,
        "fields": [
            {
                "fieldname": "employee",
                "label": "Employee",
                "fieldtype": "Link",
                "options": "Employee",
                "reqd": 1
            },
            {
                "fieldname": "employee_name",
                "label": "Employee Name",
                "fieldtype": "Data",
                "fetch_from": "employee.employee_name",
                "read_only": 1
            },
            {
                "fieldname": "cb1",
                "fieldtype": "Column Break"
            },
            {
                "fieldname": "department",
                "label": "Department",
                "fieldtype": "Link",
                "options": "Department",
                "fetch_from": "employee.department"
            },
            {
                "fieldname": "designation",
                "label": "Designation",
                "fieldtype": "Link",
                "options": "Designation",
                "fetch_from": "employee.designation"
            },
            {
                "fieldname": "sb1",
                "fieldtype": "Section Break",
                "label": "Training Information"
            },
            {
                "fieldname": "training_type",
                "label": "Training Type",
                "fieldtype": "Select",
                "options": "\\nBloodborne Pathogen\\nHazmat Transportation\\nWaste Segregation\\nSpill Response\\nPersonal Protective Equipment\\nCompliance Training",
                "reqd": 1
            },
            {
                "fieldname": "training_provider",
                "label": "Training Provider",
                "fieldtype": "Data"
            },
            {
                "fieldname": "cb2",
                "fieldtype": "Column Break"
            },
            {
                "fieldname": "training_date",
                "label": "Training Date",
                "fieldtype": "Date",
                "reqd": 1
            },
            {
                "fieldname": "expiration_date",
                "label": "Expiration Date",
                "fieldtype": "Date"
            },
            {
                "fieldname": "sb2",
                "fieldtype": "Section Break",
                "label": "Certification"
            },
            {
                "fieldname": "certification_number",
                "label": "Certification Number",
                "fieldtype": "Data"
            },
            {
                "fieldname": "training_hours",
                "label": "Training Hours",
                "fieldtype": "Float"
            },
            {
                "fieldname": "cb3",
                "fieldtype": "Column Break"
            },
            {
                "fieldname": "pass_score",
                "label": "Pass Score (%)",
                "fieldtype": "Percent"
            },
            {
                "fieldname": "status",
                "label": "Status",
                "fieldtype": "Select",
                "options": "\\nActive\\nExpired\\nNeeds Renewal",
                "default": "Active"
            },
            {
                "fieldname": "sb3",
                "fieldtype": "Section Break",
                "label": "Notes"
            },
            {
                "fieldname": "training_notes",
                "label": "Training Notes",
                "fieldtype": "Text"
            }
        ]
    })
    
    doctype.insert()
    print("✅ Created Training Record DocType")

def create_incident_report():
    """Create Incident Report DocType"""
    
    if frappe.db.exists("DocType", "Incident Report"):
        print("⚠️  Incident Report DocType already exists")
        return
    
    doctype = frappe.get_doc({
        "doctype": "DocType",
        "name": "Incident Report",
        "module": "Stock",
        "custom": 1,
        "is_submittable": 1,
        "fields": [
            {
                "fieldname": "incident_date",
                "label": "Incident Date",
                "fieldtype": "Datetime",
                "reqd": 1
            },
            {
                "fieldname": "reported_by",
                "label": "Reported By",
                "fieldtype": "Link",
                "options": "Employee",
                "reqd": 1
            },
            {
                "fieldname": "cb1",
                "fieldtype": "Column Break"
            },
            {
                "fieldname": "incident_type",
                "label": "Incident Type",
                "fieldtype": "Select",
                "options": "\\nSpill\\nNeedlestick\\nExposure\\nImproper Disposal\\nContainer Overflow\\nTransportation Incident",
                "reqd": 1
            },
            {
                "fieldname": "severity",
                "label": "Severity",
                "fieldtype": "Select",
                "options": "\\nLow\\nMedium\\nHigh\\nCritical",
                "reqd": 1
            },
            {
                "fieldname": "sb1",
                "fieldtype": "Section Break",
                "label": "Location Information"
            },
            {
                "fieldname": "location",
                "label": "Location",
                "fieldtype": "Data",
                "reqd": 1
            },
            {
                "fieldname": "department",
                "label": "Department",
                "fieldtype": "Link",
                "options": "Department"
            },
            {
                "fieldname": "cb2",
                "fieldtype": "Column Break"
            },
            {
                "fieldname": "room_number",
                "label": "Room Number",
                "fieldtype": "Data"
            },
            {
                "fieldname": "witnesses",
                "label": "Witnesses",
                "fieldtype": "Text"
            },
            {
                "fieldname": "sb2",
                "fieldtype": "Section Break",
                "label": "Incident Description"
            },
            {
                "fieldname": "description",
                "label": "Incident Description",
                "fieldtype": "Text",
                "reqd": 1
            },
            {
                "fieldname": "immediate_actions",
                "label": "Immediate Actions Taken",
                "fieldtype": "Text"
            },
            {
                "fieldname": "sb3",
                "fieldtype": "Section Break",
                "label": "Personnel Involved"
            },
            {
                "fieldname": "personnel_affected",
                "label": "Personnel Affected",
                "fieldtype": "Table",
                "options": "Affected Personnel"
            },
            {
                "fieldname": "sb4",
                "fieldtype": "Section Break",
                "label": "Investigation and Follow-up"
            },
            {
                "fieldname": "root_cause",
                "label": "Root Cause Analysis",
                "fieldtype": "Text"
            },
            {
                "fieldname": "corrective_actions",
                "label": "Corrective Actions",
                "fieldtype": "Text"
            },
            {
                "fieldname": "cb3",
                "fieldtype": "Column Break"
            },
            {
                "fieldname": "preventive_actions",
                "label": "Preventive Actions",
                "fieldtype": "Text"
            },
            {
                "fieldname": "follow_up_date",
                "label": "Follow-up Date",
                "fieldtype": "Date"
            }
        ]
    })
    
    doctype.insert()
    print("✅ Created Incident Report DocType")

def create_affected_personnel_table():
    """Create child table for affected personnel"""
    
    if frappe.db.exists("DocType", "Affected Personnel"):
        print("⚠️  Affected Personnel DocType already exists")
        return
    
    doctype = frappe.get_doc({
        "doctype": "DocType",
        "name": "Affected Personnel",
        "module": "Stock",
        "custom": 1,
        "istable": 1,
        "fields": [
            {
                "fieldname": "employee",
                "label": "Employee",
                "fieldtype": "Link",
                "options": "Employee"
            },
            {
                "fieldname": "employee_name",
                "label": "Employee Name",
                "fieldtype": "Data",
                "fetch_from": "employee.employee_name"
            },
            {
                "fieldname": "injury_type",
                "label": "Injury/Exposure Type",
                "fieldtype": "Select",
                "options": "\\nNone\\nNeedlestick\\nCut\\nSkin Contact\\nInhalation\\nIngestion\\nOther"
            },
            {
                "fieldname": "medical_attention",
                "label": "Medical Attention Required",
                "fieldtype": "Check"
            },
            {
                "fieldname": "notes",
                "label": "Notes",
                "fieldtype": "Text"
            }
        ]
    })
    
    doctype.insert()
    print("✅ Created Affected Personnel DocType")

def main():
    """Main function to create all custom doctypes"""
    try:
        print("📋 Creating Custom DocTypes for Medical Waste Compliance...")
        
        print("\n📄 Creating manifest-related doctypes...")
        create_manifest_item_table()
        create_medical_waste_manifest()
        
        print("\n📦 Creating container tracking...")
        create_waste_container_tracking()
        
        print("\n🔍 Creating compliance inspection...")
        create_inspection_area_table()
        create_compliance_inspection()
        
        print("\n🎓 Creating training records...")
        create_training_record()
        
        print("\n⚠️  Creating incident reporting...")
        create_affected_personnel_table()
        create_incident_report()
        
        frappe.db.commit()
        print("\n✅ All custom DocTypes created successfully!")
        
    except Exception as e:
        print(f"❌ Error creating custom DocTypes: {str(e)}")
        frappe.db.rollback()
        raise

if __name__ == "__main__":
    main()