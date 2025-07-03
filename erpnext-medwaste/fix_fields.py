import frappe

def fix_dropdown_fields():
    """Fix custom field dropdown options"""
    
    # Update waste_classification field
    try:
        cf = frappe.get_doc("Custom Field", "Item-waste_classification")
        cf.options = "\nInfectious\nSharps\nPharmaceutical\nPathological\nChemotherapy\nTrace Chemotherapy"
        cf.save()
        print("✅ Fixed waste_classification field")
    except Exception as e:
        print(f"❌ Error updating waste_classification: {e}")
    
    # Update hazard_level field
    try:
        cf = frappe.get_doc("Custom Field", "Item-hazard_level")
        cf.options = "\nLow\nMedium\nHigh\nExtreme"
        cf.save()
        print("✅ Fixed hazard_level field")
    except Exception as e:
        print(f"❌ Error updating hazard_level: {e}")
    
    # Update treatment_method field
    try:
        cf = frappe.get_doc("Custom Field", "Item-treatment_method")
        cf.options = "\nAutoclave\nIncineration\nChemical Treatment\nMicrowave\nIrradiation\nSecure Landfill"
        cf.save()
        print("✅ Fixed treatment_method field")
    except Exception as e:
        print(f"❌ Error updating treatment_method: {e}")
    
    frappe.db.commit()
    print("🎉 All custom fields have been updated!")

fix_dropdown_fields()