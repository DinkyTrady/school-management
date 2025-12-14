import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.academics.models import TahunAjaran

# Target: 2024/2025 - Ganjil (ID 1)
target_ta = TahunAjaran.objects.filter(tahun='2024/2025', semester='Ganjil').first()

if target_ta:
    print(f"Found target TahunAjaran: {target_ta}")
    
    # Deactivate all
    TahunAjaran.objects.update(is_active=False)
    
    # Activate target
    target_ta.is_active = True
    target_ta.save()
    print(f"Activated {target_ta}")
else:
    print("Target TahunAjaran not found.")
