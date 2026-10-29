from rest_framework import serializers
from .models import Category, Product, Order, OrderItem


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(
        source="products.count",
        read_only=True
    )

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "icon_name",
            "image_url",
            "products_count",
            "created_at",
        ]


class ProductSerializer(serializers.ModelSerializer):
    # Category information
    category_name = serializers.ReadOnlyField(
        source="category.name"
    )

    category_slug = serializers.ReadOnlyField(
        source="category.slug"
    )

    # Frontend-friendly images array
    images = serializers.SerializerMethodField()

    # Keep prices as numbers for React
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False
    )

    original_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        allow_null=True,
        coerce_to_string=False
    )

    class Meta:
        model = Product

        fields = [
            # Identification
            "id",
            "name",
            "slug",

            # Category
            "category",
            "category_name",
            "category_slug",

            # Product classification
            "brand",
            "sport",
            "gender",

            # Pricing
            "price",
            "original_price",
            "badge",

            # Reviews
            "rating",
            "reviews_count",

            # Product information
            "description",
            "features",
            "tech_specs",

            # Images
            "primary_image",
            "secondary_image",
            "additional_images",
            "images",

            # Variants
            "available_sizes",
            "colors",

            # Inventory
            "stock_quantity",
            "in_stock",

            # Featured
            "is_featured",
            "is_new",

            # Dates
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "category_name",
            "category_slug",
            "images",
            "in_stock",
        ]

    def get_images(self, obj):
        """
        Combines primary, secondary and additional images
        into one array for the frontend.
        """

        images = []

        if obj.primary_image:
            images.append(obj.primary_image)

        if obj.secondary_image:
            images.append(obj.secondary_image)

        if obj.additional_images:
            images.extend(obj.additional_images)

        return images


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem

        fields = [
            "id",
            "product",
            "product_name",
            "size",
            "color",
            "quantity",
            "price",
        ]

        read_only_fields = [
            "id",
        ]

        extra_kwargs = {
            "price": {
                "required": True
            }
        }


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(
        many=True,
        required=False
    )

    subtotal = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False
    )

    discount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False
    )

    shipping_fee = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False
    )

    total = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False
    )

    class Meta:
        model = Order

        fields = [
            "id",
            "order_number",

            # Customer
            "customer_name",
            "email",
            "phone",

            # Shipping
            "address",
            "city",
            "state",
            "pincode",

            # Payment
            "payment_method",
            "payment_status",

            # Pricing
            "subtotal",
            "discount",
            "shipping_fee",
            "total",

            # Order status
            "status",

            # Items
            "items",

            # Dates
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "order_number",
            "created_at",
            "updated_at",
        ]