import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from core.api.models import Category, Subcategory, Product
from django.utils.text import slugify

# The new mapping structure
MAPPING = {
    "Living Room": {
        "new_name": "Sofas",
        "subcategories": ["Fabric sofas", "Wooden sofas", "L-shaped Sofas", "Sofas cum Bed", "Recliners"]
    },
    "Bedroom": {
        "new_name": "Dining",
        "subcategories": ["4 seater Dining sets", "6-Seater Dining Sets", "8-Seater Dining sets", "Extendable Dining"]
    },
    "Dining": {
        "new_name": "Beds",
        "subcategories": ["Solid wood Beds", "Upholstered Beds", "Beds with Storage", "King size g-beds", "Queen size beds"]
    },
    "Study": {
        "new_name": "Office Tables and Study Chairs",
        "subcategories": ["L-Shape Office - table", "Executive - chairs", "Waiting -chairs", "Study chair", "Single -Gaming -Chair"]
    }
}

def migrate():
    # Because there are name conflicts (e.g., Bedroom -> Dining, and Dining -> Beds)
    # We will first append a temporary suffix to all old ones to avoid uniqueness collisions
    
    # 1. Add suffixes to Categories
    for old_name in MAPPING.keys():
        try:
            cat = Category.objects.get(name=old_name)
            cat.name = f"{old_name}_OLD"
            cat.slug = slugify(f"{old_name}_OLD")
            cat.save()
            print(f"Temporarily renamed category: {old_name} -> {cat.name}")
        except Category.DoesNotExist:
            print(f"Category {old_name} does not exist, skipping temp rename.")
        except Category.MultipleObjectsReturned:
            print(f"Multiple categories named {old_name} exist. Skipping...")

    # 2. Rename them to their new names and create subcategories
    for old_name, data in MAPPING.items():
        new_name = data["new_name"]
        subs = data["subcategories"]
        
        # Try to find the temporarily renamed category
        try:
            cat = Category.objects.get(name=f"{old_name}_OLD")
            cat.name = new_name
            cat.slug = slugify(new_name)
            cat.save()
            print(f"Renamed category: {old_name}_OLD -> {new_name}")
        except Category.DoesNotExist:
            # If it didn't exist, maybe it was already migrated or we just create it
            cat, created = Category.objects.get_or_create(
                name=new_name,
                defaults={'slug': slugify(new_name)}
            )
            print(f"{'Created' if created else 'Found'} category: {new_name}")
        except Category.MultipleObjectsReturned:
            cat = Category.objects.filter(name=f"{old_name}_OLD").first()
            cat.name = new_name
            cat.slug = slugify(new_name)
            cat.save()

        # Clear existing subcategories for this category just in case
        cat.subcategories.all().delete()
        
        # Create subcategories
        for i, sub_name in enumerate(subs):
            Subcategory.objects.create(
                category=cat,
                name=sub_name,
                slug=slugify(sub_name),
                display_order=i
            )
        print(f"  Created {len(subs)} subcategories for {new_name}")

        # 3. Update Product string fields
        # Update products that had the old category string
        products_updated = Product.objects.filter(category=old_name).update(category=new_name)
        print(f"  Updated {products_updated} products from {old_name} to {new_name}")

    print("Migration complete!")

if __name__ == '__main__':
    migrate()
