#!/usr/bin/env python3
"""
Simple test script to verify ERPNext connectivity
"""

import frappe

def main():
    """Test ERPNext connection and create basic item groups"""
    print("🔗 Testing ERPNext connection...")
    
    # Create basic medical waste item groups
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
        if i > 0:  # Sub-groups go under Medical Waste
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
    
    frappe.db.commit()
    print("✅ Basic item groups setup completed!")

if __name__ == "__main__":
    main()