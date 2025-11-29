#!/usr/bin/env python3
"""
Script to update all templates from old permission_tags to new permissions system
"""

import os
import re

# Define the root directory
ROOT_DIR = "/home/kyra/personal/colleges/semester3/basis-data/school-management"

# Template files to update (from grep results)
TEMPLATE_FILES = [
    "apps/users/templates/users/guru_list.html",
    "apps/users/templates/users/akun_list.html", 
    "apps/users/templates/users/peran_list.html",
    "apps/users/templates/users/partials/peran_table_body.html",
    "apps/users/templates/users/partials/guru_table_body.html",
    "apps/users/templates/users/partials/akun_table_body.html",
    "apps/academics/templates/academics/mapel_list.html",
    "apps/academics/templates/academics/jurusan_list.html",
    "apps/academics/templates/academics/jadwal_list.html",
    "apps/academics/templates/academics/tahun_ajaran_list.html",
    "apps/academics/templates/academics/partials/tahun_ajaran_table_body.html",
    "apps/academics/templates/academics/partials/mapel_table_body.html",
    "apps/academics/templates/academics/partials/jurusan_table_body.html",
    "apps/academics/templates/academics/partials/jadwal_table_body.html",
]

def update_template_file(filepath):
    """Update a single template file"""
    full_path = os.path.join(ROOT_DIR, filepath)
    
    if not os.path.exists(full_path):
        print(f"❌ File not found: {filepath}")
        return False
    
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Replace {% load permission_tags %} with {% load permissions %}
        content = re.sub(r'{%\s*load\s+permission_tags\s*%}', '{% load permissions %}', content)
        
        # Replace old permission checks with new ones
        # Pattern: {% if user|can_add:"model.name" %}
        content = re.sub(
            r'{%\s*if\s+user\|can_add:"[^"]*"\s*%}',
            '{% if user|can_add_model:"MODEL_NAME" %}',
            content
        )
        
        # Pattern: {% if user|can_edit:"model.name" %}  
        content = re.sub(
            r'{%\s*if\s+user\|can_edit:"[^"]*"\s*%}',
            '{% if user|can_edit_model:"MODEL_NAME" %}',
            content
        )
        
        # Pattern: {% if user|can_delete:"model.name" %}
        content = re.sub(
            r'{%\s*if\s+user\|can_delete:"[^"]*"\s*%}',
            '{% if user|can_delete_model:"MODEL_NAME" %}',
            content
        )
        
        # Determine model name from file path
        model_name = "unknown"
        if "akun" in filepath:
            model_name = "akun"
        elif "peran" in filepath:
            model_name = "peran"
        elif "siswa" in filepath:
            model_name = "siswa"
        elif "guru" in filepath:
            model_name = "guru"
        elif "kelas" in filepath:
            model_name = "kelas"
        elif "mapel" in filepath:
            model_name = "mapel"
        elif "jurusan" in filepath:
            model_name = "jurusan"
        elif "jadwal" in filepath:
            model_name = "jadwal"
        elif "tahun" in filepath:
            model_name = "tahunajar"
            
        # Replace MODEL_NAME placeholder with actual model name
        content = content.replace("MODEL_NAME", model_name)
        
        if content != original_content:
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Updated: {filepath}")
            return True
        else:
            print(f"⏭️  No changes needed: {filepath}")
            return False
            
    except Exception as e:
        print(f"❌ Error updating {filepath}: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Starting template updates...")
    print("=" * 60)
    
    updated_count = 0
    
    for template_file in TEMPLATE_FILES:
        if update_template_file(template_file):
            updated_count += 1
    
    print("=" * 60)
    print(f"✅ Template update complete!")
    print(f"📊 Files updated: {updated_count}/{len(TEMPLATE_FILES)}")
    print()
    print("⚠️  NOTE: You may need to manually fix specific URLs and model names")
    print("   Check the updated files for any MODEL_NAME placeholders that weren't replaced")

if __name__ == "__main__":
    main()