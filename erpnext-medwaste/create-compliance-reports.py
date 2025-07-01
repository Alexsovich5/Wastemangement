#!/usr/bin/env python3
"""
Medical Waste Compliance Reporting Templates
Creates standard reports and dashboards for regulatory compliance
"""

import frappe
from frappe import _

def create_custom_reports():
    """Create custom reports for medical waste compliance"""
    
    reports = [
        {
            "report_name": "Medical Waste Generation Report",
            "report_type": "Script Report",
            "module": "Stock",
            "script": """
def execute(filters=None):
    columns = [
        {"fieldname": "date", "label": "Date", "fieldtype": "Date", "width": 100},
        {"fieldname": "item_code", "label": "Item Code", "fieldtype": "Link", "options": "Item", "width": 120},
        {"fieldname": "item_name", "label": "Item Name", "fieldtype": "Data", "width": 200},
        {"fieldname": "waste_classification", "label": "Waste Type", "fieldtype": "Data", "width": 120},
        {"fieldname": "qty", "label": "Quantity", "fieldtype": "Float", "width": 100},
        {"fieldname": "uom", "label": "UOM", "fieldtype": "Data", "width": 80},
        {"fieldname": "warehouse", "label": "Location", "fieldtype": "Link", "options": "Warehouse", "width": 150},
        {"fieldname": "department", "label": "Department", "fieldtype": "Data", "width": 120}
    ]
    
    data = frappe.db.sql('''
        SELECT 
            sle.posting_date as date,
            sle.item_code,
            i.item_name,
            i.waste_classification,
            sle.actual_qty as qty,
            i.stock_uom as uom,
            sle.warehouse,
            sle.generation_department as department
        FROM `tabStock Ledger Entry` sle
        JOIN `tabItem` i ON sle.item_code = i.name
        WHERE sle.actual_qty > 0 
        AND i.item_group LIKE '%Medical Waste%'
        AND (%(from_date)s IS NULL OR sle.posting_date >= %(from_date)s)
        AND (%(to_date)s IS NULL OR sle.posting_date <= %(to_date)s)
        ORDER BY sle.posting_date DESC
    ''', filters, as_dict=1)
    
    return columns, data
            """
        },
        {
            "report_name": "Waste Disposal Tracking Report",
            "report_type": "Script Report", 
            "module": "Stock",
            "script": """
def execute(filters=None):
    columns = [
        {"fieldname": "manifest_number", "label": "Manifest #", "fieldtype": "Link", "options": "Medical Waste Manifest", "width": 120},
        {"fieldname": "manifest_date", "label": "Date", "fieldtype": "Date", "width": 100},
        {"fieldname": "supplier", "label": "Disposal Company", "fieldtype": "Data", "width": 150},
        {"fieldname": "waste_type", "label": "Waste Type", "fieldtype": "Data", "width": 120},
        {"fieldname": "quantity", "label": "Quantity", "fieldtype": "Float", "width": 100},
        {"fieldname": "weight", "label": "Weight (lbs)", "fieldtype": "Float", "width": 100},
        {"fieldname": "treatment_method", "label": "Treatment", "fieldtype": "Data", "width": 120},
        {"fieldname": "status", "label": "Status", "fieldtype": "Data", "width": 100}
    ]
    
    data = frappe.db.sql('''
        SELECT 
            m.manifest_number,
            m.manifest_date,
            m.transporter_name as supplier,
            mi.waste_classification as waste_type,
            mi.quantity,
            mi.weight_lbs as weight,
            m.treatment_method,
            m.status
        FROM `tabMedical Waste Manifest` m
        JOIN `tabMedical Waste Manifest Item` mi ON m.name = mi.parent
        WHERE (%(from_date)s IS NULL OR m.manifest_date >= %(from_date)s)
        AND (%(to_date)s IS NULL OR m.manifest_date <= %(to_date)s)
        ORDER BY m.manifest_date DESC
    ''', filters, as_dict=1)
    
    return columns, data
            """
        },
        {
            "report_name": "Training Compliance Report",
            "report_type": "Script Report",
            "module": "HR",
            "script": """
def execute(filters=None):
    columns = [
        {"fieldname": "employee", "label": "Employee", "fieldtype": "Link", "options": "Employee", "width": 120},
        {"fieldname": "employee_name", "label": "Name", "fieldtype": "Data", "width": 150},
        {"fieldname": "department", "label": "Department", "fieldtype": "Data", "width": 120},
        {"fieldname": "training_type", "label": "Training Type", "fieldtype": "Data", "width": 150},
        {"fieldname": "training_date", "label": "Training Date", "fieldtype": "Date", "width": 100},
        {"fieldname": "expiration_date", "label": "Expires", "fieldtype": "Date", "width": 100},
        {"fieldname": "status", "label": "Status", "fieldtype": "Data", "width": 100},
        {"fieldname": "days_until_expiry", "label": "Days to Expiry", "fieldtype": "Int", "width": 120}
    ]
    
    data = frappe.db.sql('''
        SELECT 
            tr.employee,
            tr.employee_name,
            tr.department,
            tr.training_type,
            tr.training_date,
            tr.expiration_date,
            tr.status,
            DATEDIFF(tr.expiration_date, CURDATE()) as days_until_expiry
        FROM `tabTraining Record` tr
        WHERE tr.expiration_date IS NOT NULL
        AND (%(department)s IS NULL OR tr.department = %(department)s)
        ORDER BY tr.expiration_date ASC
    ''', filters, as_dict=1)
    
    return columns, data
            """
        },
        {
            "report_name": "Incident Summary Report", 
            "report_type": "Script Report",
            "module": "Stock",
            "script": """
def execute(filters=None):
    columns = [
        {"fieldname": "incident_date", "label": "Date", "fieldtype": "Datetime", "width": 150},
        {"fieldname": "incident_type", "label": "Type", "fieldtype": "Data", "width": 120},
        {"fieldname": "severity", "label": "Severity", "fieldtype": "Data", "width": 100},
        {"fieldname": "location", "label": "Location", "fieldtype": "Data", "width": 150},
        {"fieldname": "department", "label": "Department", "fieldtype": "Data", "width": 120},
        {"fieldname": "reported_by", "label": "Reported By", "fieldtype": "Data", "width": 120},
        {"fieldname": "status", "label": "Status", "fieldtype": "Data", "width": 100}
    ]
    
    data = frappe.db.sql('''
        SELECT 
            ir.incident_date,
            ir.incident_type,
            ir.severity,
            ir.location,
            ir.department,
            e.employee_name as reported_by,
            CASE 
                WHEN ir.docstatus = 0 THEN 'Draft'
                WHEN ir.docstatus = 1 THEN 'Submitted'
                ELSE 'Cancelled'
            END as status
        FROM `tabIncident Report` ir
        LEFT JOIN `tabEmployee` e ON ir.reported_by = e.name
        WHERE (%(from_date)s IS NULL OR DATE(ir.incident_date) >= %(from_date)s)
        AND (%(to_date)s IS NULL OR DATE(ir.incident_date) <= %(to_date)s)
        ORDER BY ir.incident_date DESC
    ''', filters, as_dict=1)
    
    return columns, data
            """
        }
    ]
    
    for report_data in reports:
        if not frappe.db.exists("Report", report_data["report_name"]):
            report = frappe.get_doc({
                "doctype": "Report",
                "report_name": report_data["report_name"],
                "report_type": report_data["report_type"],
                "module": report_data["module"],
                "is_standard": "No"
            })
            report.insert()
            print(f"✅ Created report: {report_data['report_name']}")

def create_dashboards():
    """Create dashboards for medical waste management"""
    
    # Dashboard for Medical Waste Overview
    dashboard_data = {
        "dashboard_name": "Medical Waste Management",
        "module": "Stock",
        "charts": [
            {
                "chart_name": "Waste Generation Trends",
                "chart_type": "Line",
                "timeseries": 1,
                "based_on": "posting_date",
                "time_interval": "Daily",
                "value_based_on": "actual_qty",
                "source": "Stock Ledger Entry",
                "filters": [
                    {"fieldname": "actual_qty", "operator": ">", "value": "0"},
                    {"fieldname": "item_group", "operator": "like", "value": "%Medical Waste%"}
                ]
            },
            {
                "chart_name": "Waste by Classification",
                "chart_type": "Donut",
                "based_on": "waste_classification",
                "value_based_on": "count",
                "source": "Stock Ledger Entry"
            },
            {
                "chart_name": "Monthly Disposal Costs",
                "chart_type": "Bar", 
                "timeseries": 1,
                "based_on": "posting_date",
                "time_interval": "Monthly",
                "value_based_on": "total",
                "source": "Purchase Invoice"
            }
        ]
    }
    
    print("📊 Dashboard configuration prepared (would be created through UI)")

def create_print_formats():
    """Create print formats for compliance documents"""
    
    print_formats = [
        {
            "name": "Medical Waste Manifest Print",
            "doc_type": "Medical Waste Manifest",
            "print_format_type": "Jinja"
        },
        {
            "name": "Training Certificate",
            "doc_type": "Training Record", 
            "print_format_type": "Jinja"
        },
        {
            "name": "Incident Report Form",
            "doc_type": "Incident Report",
            "print_format_type": "Jinja"
        },
        {
            "name": "Compliance Inspection Report",
            "doc_type": "Compliance Inspection",
            "print_format_type": "Jinja"
        }
    ]
    
    for pf in print_formats:
        print(f"📄 Print format template ready: {pf['name']}")

def setup_notification_templates():
    """Set up email notifications for compliance alerts"""
    
    notifications = [
        {
            "name": "Training Expiry Alert",
            "document_type": "Training Record",
            "event": "Days Before",
            "days_in_advance": 30,
            "condition": "doc.status == 'Active'",
            "subject": "Training Expiring Soon: {{doc.training_type}}",
            "message": "Training for {{doc.employee_name}} expires on {{doc.expiration_date}}"
        },
        {
            "name": "Manifest Overdue Alert",
            "document_type": "Medical Waste Manifest", 
            "event": "Days After",
            "days_in_advance": 3,
            "condition": "doc.status != 'Completed'",
            "subject": "Overdue Manifest: {{doc.manifest_number}}",
            "message": "Manifest {{doc.manifest_number}} is overdue for completion"
        },
        {
            "name": "Container Full Alert",
            "document_type": "Waste Container Tracking",
            "event": "Value Change",
            "condition": "doc.fill_level >= 80",
            "subject": "Container Nearing Full: {{doc.container_id}}",
            "message": "Container {{doc.container_id}} is {{doc.fill_level}}% full and needs collection"
        },
        {
            "name": "Incident Report Notification",
            "document_type": "Incident Report",
            "event": "On Submit", 
            "subject": "New Incident Report: {{doc.incident_type}}",
            "message": "A new {{doc.severity}} incident has been reported at {{doc.location}}"
        }
    ]
    
    for notification in notifications:
        print(f"🔔 Notification template ready: {notification['name']}")

def create_workflow_templates():
    """Create workflow templates for approval processes"""
    
    workflows = [
        {
            "workflow_name": "Incident Report Approval",
            "document_type": "Incident Report",
            "states": [
                {"state": "Draft", "doc_status": 0, "allow_edit": "System Manager"},
                {"state": "Under Review", "doc_status": 0, "allow_edit": "Safety Manager"},
                {"state": "Approved", "doc_status": 1, "allow_edit": ""},
                {"state": "Rejected", "doc_status": 0, "allow_edit": "System Manager"}
            ],
            "transitions": [
                {"state": "Draft", "action": "Submit for Review", "next_state": "Under Review"},
                {"state": "Under Review", "action": "Approve", "next_state": "Approved"},
                {"state": "Under Review", "action": "Reject", "next_state": "Rejected"},
                {"state": "Rejected", "action": "Resubmit", "next_state": "Under Review"}
            ]
        },
        {
            "workflow_name": "Compliance Inspection Approval",
            "document_type": "Compliance Inspection", 
            "states": [
                {"state": "Draft", "doc_status": 0, "allow_edit": "Quality Manager"},
                {"state": "Review Required", "doc_status": 0, "allow_edit": "Compliance Officer"},
                {"state": "Approved", "doc_status": 1, "allow_edit": ""},
                {"state": "Requires Action", "doc_status": 0, "allow_edit": "Quality Manager"}
            ],
            "transitions": [
                {"state": "Draft", "action": "Submit", "next_state": "Review Required"},
                {"state": "Review Required", "action": "Approve", "next_state": "Approved"},
                {"state": "Review Required", "action": "Request Action", "next_state": "Requires Action"},
                {"state": "Requires Action", "action": "Resubmit", "next_state": "Review Required"}
            ]
        }
    ]
    
    for workflow in workflows:
        print(f"⚙️ Workflow template ready: {workflow['workflow_name']}")

def setup_kpi_indicators():
    """Set up Key Performance Indicators for waste management"""
    
    kpis = [
        {
            "indicator_name": "Waste Generation Rate",
            "formula": "Total waste generated / Patient days",
            "unit": "lbs/patient day",
            "target": "< 15",
            "frequency": "Monthly"
        },
        {
            "indicator_name": "Disposal Cost per Pound",
            "formula": "Total disposal costs / Total weight disposed",
            "unit": "$/lb",
            "target": "< $3.50",
            "frequency": "Monthly"
        },
        {
            "indicator_name": "Training Compliance Rate",
            "formula": "(Current trained employees / Total employees) * 100",
            "unit": "%",
            "target": "> 95%",
            "frequency": "Quarterly"
        },
        {
            "indicator_name": "Manifest Completion Rate",
            "formula": "(Completed manifests / Total manifests) * 100",
            "unit": "%", 
            "target": "100%",
            "frequency": "Monthly"
        },
        {
            "indicator_name": "Incident Rate",
            "formula": "Number of incidents / 100,000 work hours",
            "unit": "incidents/100k hours",
            "target": "< 2",
            "frequency": "Quarterly"
        }
    ]
    
    for kpi in kpis:
        print(f"📈 KPI template ready: {kpi['indicator_name']}")

def main():
    """Main function to create compliance reporting templates"""
    try:
        print("📊 Creating Compliance Reporting Templates...")
        
        print("\n📋 Creating custom reports...")
        create_custom_reports()
        
        print("\n📊 Setting up dashboards...")
        create_dashboards()
        
        print("\n📄 Creating print formats...")
        create_print_formats()
        
        print("\n🔔 Setting up notifications...")
        setup_notification_templates()
        
        print("\n⚙️ Creating workflows...")
        create_workflow_templates()
        
        print("\n📈 Setting up KPIs...")
        setup_kpi_indicators()
        
        frappe.db.commit()
        print("\n✅ Compliance reporting templates created!")
        
        print("\n📝 Additional Setup Required:")
        print("  - Configure dashboard charts through ERPNext UI")
        print("  - Create custom print format HTML templates")
        print("  - Set up email notification templates")
        print("  - Configure workflow states and transitions")
        print("  - Create KPI tracking dashboards")
        
    except Exception as e:
        print(f"❌ Error creating compliance templates: {str(e)}")
        frappe.db.rollback()
        raise

if __name__ == "__main__":
    main()