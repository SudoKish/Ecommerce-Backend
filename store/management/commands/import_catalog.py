from pathlib import Path
import json
import subprocess

from django.core.management.base import BaseCommand
from django.db import transaction

from store.models import Product, Category


class Command(BaseCommand):
    help = "Synchronize Django products with the AMS frontend catalog"

    def handle(self, *args, **options):

        # =========================================================
        # 1. Locate frontend catalog
        # =========================================================

        backend_dir = Path(__file__).resolve().parents[3]

        frontend_file = (
            backend_dir.parent
            / "frontend"
            / "src"
            / "data"
            / "sportsData.js"
        )

        if not frontend_file.exists():
            self.stdout.write(
                self.style.ERROR(
                    f"Catalog not found:\n{frontend_file}"
                )
            )
            return

        # =========================================================
        # 2. Read PRODUCTS from sportsData.js
        # =========================================================

        js_code = r"""
import fs from "fs";

const filePath = process.argv[1];

let source = fs.readFileSync(filePath, "utf8");

source = source.replace(
    /\bexport\s+const\s+/g,
    "const "
);

source += `
globalThis.__AMS_PRODUCTS = PRODUCTS;
`;

const encoded = Buffer
    .from(source, "utf8")
    .toString("base64");

await import(`data:text/javascript;base64,${encoded}`);

console.log(JSON.stringify(globalThis.__AMS_PRODUCTS));
"""

        try:
            result = subprocess.run(
                [
                    "node",
                    "--input-type=module",
                    "-e",
                    js_code,
                    str(frontend_file),
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )

        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(
                    "Node.js was not found."
                )
            )
            return

        if result.returncode != 0:
            self.stdout.write(
                self.style.ERROR(
                    "Could not read sportsData.js"
                )
            )
            self.stdout.write(result.stderr)
            return

        try:
            products = json.loads(result.stdout)

        except json.JSONDecodeError:
            self.stdout.write(
                self.style.ERROR(
                    "Could not convert catalog to JSON."
                )
            )
            return

        # =========================================================
        # 3. Category mapping
        # =========================================================

        categories = {
            category.slug: category
            for category in Category.objects.all()
        }

        # =========================================================
        # 4. Validate catalog before touching database
        # =========================================================

        category_map = {
            "cricket": "cricket",
            "football": "football",
            "badminton": "badminton",
            "shoes": "shoes",
            "fitness": "fitness",
            "apparels": "apparels",
            "accessories": "accessories",
        }

        for product in products:

            product_id = product.get("id")

            if not product_id:
                raise ValueError(
                    "A catalog product is missing its id."
                )

            if product_id.startswith("apparel-"):
                category_slug = "apparels"
            else:
                category_slug = product_id.split("-")[0]

            if category_slug not in category_map:
                raise ValueError(
                    f"Unknown category for product {product_id}: "
                    f"{category_slug}"
                )

            if category_slug not in categories:
                raise ValueError(
                    f"Django category '{category_slug}' does not exist."
                )

        # =========================================================
        # 5. Start transaction
        # =========================================================

        with transaction.atomic():

            # -----------------------------------------------------
            # Preserve products 1 and 2 because of order history.
            # Remove only old products that are NOT part of orders.
            # -----------------------------------------------------

            protected_ids = {1, 2}

            old_products = Product.objects.exclude(
                id__in=protected_ids
            )

            old_count = old_products.count()

            old_products.delete()

            self.stdout.write(
                f"Removed {old_count} old products."
            )

            # -----------------------------------------------------
            # Import new catalog
            # -----------------------------------------------------

            created_count = 0

            for data in products:

                frontend_id = data["id"]

                if frontend_id.startswith("apparel-"):
                    category_slug = "apparels"
                else:
                    category_slug = frontend_id.split("-")[0]

                category = categories[category_slug]

                # -------------------------------------------------
                # Safe defaults
                # -------------------------------------------------

                price = data.get("price", 0)

                original_price = data.get(
                    "original_price"
                )

                rating = data.get(
                    "rating",
                    4.5
                )

                reviews_count = data.get(
                    "reviews_count",
                    0
                )

                stock_quantity = data.get(
                    "stock_count",
                    data.get("stock_quantity", 0)
                )

                # -------------------------------------------------
                # Create product
                # -------------------------------------------------

                Product.objects.create(
                    name=data.get(
                        "name",
                        "Unnamed Product"
                    ),

                    slug=frontend_id,

                    brand=data.get(
                        "brand",
                        "Generic"
                    ),

                    category=category,

                    sport=data.get(
                        "sport",
                        category.name
                    ),

                    gender=data.get(
                        "gender",
                        "UNISEX"
                    ),

                    price=price,

                    original_price=original_price,

                    badge=data.get(
                        "badge",
                        ""
                    ),

                    rating=rating,

                    reviews_count=reviews_count,

                    description=data.get(
                        "description",
                        ""
                    ),

                    features=data.get(
                        "features",
                        []
                    ),

                    tech_specs=data.get(
                        "tech_specs",
                        {}
                    ),

                    primary_image=data.get(
                        "primary_image",
                        ""
                    ),

                    secondary_image=data.get(
                        "secondary_image",
                        ""
                    ),

                    additional_images=data.get(
                        "additional_images",
                        []
                    ),

                    available_sizes=data.get(
                        "available_sizes",
                        []
                    ),

                    colors=data.get(
                        "colors",
                        []
                    ),

                    stock_quantity=stock_quantity,

                    in_stock=stock_quantity > 0,

                    is_featured=data.get(
                        "is_featured",
                        False
                    ),

                    is_new=data.get(
                        "is_new",
                        False
                    ),
                )

                created_count += 1

            # -----------------------------------------------------
            # Restore transaction protection for historical items
            # -----------------------------------------------------

            self.stdout.write(
                f"Created {created_count} new catalog products."
            )

        # =========================================================
        # 6. Final result
        # =========================================================

        total = Product.objects.count()

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                "============================================"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "AMS CATALOG SYNCHRONIZATION COMPLETE"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"New catalog products: {created_count}"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Total products in database: {total}"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Historical products DB 1 and DB 2 were preserved."
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                "============================================"
            )
        )