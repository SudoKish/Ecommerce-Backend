import uuid
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    description = models.TextField(blank=True)

    icon_name = models.CharField(
        max_length=50,
        default="Flame"
    )

    image_url = models.CharField(
        max_length=1000,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):

    GENDER_CHOICES = [
        ("MEN", "Men"),
        ("WOMEN", "Women"),
        ("UNISEX", "Unisex"),
        ("KIDS", "Kids"),
    ]

    name = models.CharField(max_length=200)

    # Frontend product ID / unique identifier
    slug = models.SlugField(
        unique=True,
        max_length=200
    )

    # Brand
    brand = models.CharField(
        max_length=100,
        default="Generic"
    )

    # Category
    category = models.ForeignKey(
        Category,
        related_name="products",
        on_delete=models.PROTECT
    )

    # Sport
    sport = models.CharField(
        max_length=100,
        default="General"
    )

    # Gender
    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES,
        default="UNISEX"
    )

    # Pricing
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Current selling price in INR"
    )

    original_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Original price before discount"
    )

    # Promotional badge
    badge = models.CharField(
        max_length=50,
        blank=True,
        help_text="Example: BEST SELLER, NEW DROP, VALUE PICK"
    )

    # Product rating
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=4.5
    )

    reviews_count = models.PositiveIntegerField(
        default=0
    )

    # Product information
    description = models.TextField(
        blank=True
    )

    features = models.JSONField(
        default=list,
        blank=True
    )

    tech_specs = models.JSONField(
        default=dict,
        blank=True
    )

    # Images
    # Using CharField instead of URLField because frontend
    # can use local paths such as /products/football/ball.png
    primary_image = models.CharField(
        max_length=1000,
        blank=True
    )

    secondary_image = models.CharField(
        max_length=1000,
        blank=True
    )

    additional_images = models.JSONField(
        default=list,
        blank=True
    )

    # Variants
    available_sizes = models.JSONField(
        default=list,
        blank=True
    )

    colors = models.JSONField(
        default=list,
        blank=True
    )

    # Inventory
    stock_quantity = models.PositiveIntegerField(
        default=0
    )

    in_stock = models.BooleanField(
        default=True
    )

    # Featured products
    is_featured = models.BooleanField(
        default=False
    )
    
    is_new = models.BooleanField(
    default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):

        # Keep in_stock synchronized with actual stock
        self.in_stock = self.stock_quantity > 0

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - ₹{self.price}"


class Order(models.Model):

    PAYMENT_METHODS = [
        ("UPI", "UPI / QR Code Scan"),
        ("CARD", "Credit / Debit Card"),
        ("NETBANKING", "Net Banking"),
        ("COD", "Cash On Delivery"),
    ]

    STATUS_CHOICES = [
        ("CONFIRMED", "Order Confirmed"),
        ("PROCESSING", "Processing in Warehouse"),
        ("SHIPPED", "Dispatched / In Transit"),
        ("DELIVERED", "Delivered"),
        ("CANCELLED", "Cancelled"),
    ]

    PAYMENT_STATUS_CHOICES = [
        ("PENDING", "Payment Pending"),
        ("PAID", "Payment Successful"),
        ("FAILED", "Payment Failed"),
        ("REFUNDED", "Refunded"),
    ]

    order_number = models.CharField(
        max_length=50,
        unique=True,
        editable=False
    )

    customer_name = models.CharField(
        max_length=150
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=20
    )

    address = models.TextField()

    city = models.CharField(
        max_length=100
    )

    state = models.CharField(
        max_length=100
    )

    pincode = models.CharField(
        max_length=10
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
        default="UPI"
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default="PENDING"
    )

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    shipping_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="CONFIRMED"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):

        if not self.order_number:
            self.order_number = (
                f"AMS-{uuid.uuid4().hex[:8].upper()}"
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_number} - ₹{self.total}"


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        related_name="items",
        on_delete=models.CASCADE
    )

    product = models.ForeignKey(
        Product,
        related_name="order_items",
        on_delete=models.SET_NULL,
        null=True
    )

    product_name = models.CharField(
        max_length=200
    )

    size = models.CharField(
        max_length=50,
        blank=True
    )

    color = models.CharField(
        max_length=100,
        blank=True
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        variant = []

        if self.size:
            variant.append(f"Size: {self.size}")

        if self.color:
            variant.append(f"Color: {self.color}")

        variant_text = ", ".join(variant)

        if variant_text:
            return f"{self.quantity}x {self.product_name} ({variant_text})"

        return f"{self.quantity}x {self.product_name}"