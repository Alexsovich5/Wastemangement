#!/usr/bin/env python3
"""
Fix dropdown options for medical waste custom fields
"""
import frappe

def fix_custom_fields():
    """Fix the custom field options by removing double backslashes"""
    
    # Fields to fix
    fields_to_fix = [
        {
            'fieldname': 'waste_classification',
            'options': '\nInfectious\nSharps\nPharmaceutical\nPathological\nChemotherapy\nTrace Chemotherapy'
        },
        {
            'fieldname': 'hazard_level', 
            'options': '\nLow\nMedium\nHigh\nExtreme'
        },
        {
            'fieldname': 'treatment_method',
            'options': '\nAutoclave\nIncineration\nChemical Treatment\nMicrowave\nIrradiation\nSecure Landfill'
        }
    ]
    
    for field_data in fields_to_fix:
        # Find the existing custom field
        custom_field_name = f"Item-{field_data['fieldname']}"
        if frappe.db.exists('Custom Field', custom_field_name):
            custom_field = frappe.get_doc('Custom Field', custom_field_name)
            custom_field.options = field_data['options']
            custom_field.save()
            print(f"✅ Fixed options for {field_data['fieldname']}")
        else:
            print(f"❌ Custom field {field_data['fieldname']} not found")
    
    frappe.db.commit()
    print("🎉 All custom fields have been fixed!")

if __name__ == "__main__":
    frappe.init(site='frontend')
    frappe.connect()
    fix_custom_fields()