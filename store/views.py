from decimal import Decimal, InvalidOperation

from django.db import transaction
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Category, Product, Order, OrderItem
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    OrderSerializer,
)


# ============================================================
# CATEGORY
# ============================================================

class CategoryListView(APIView):

    def get(self, request):
        categories = Category.objects.all().order_by("name")

        serializer = CategorySerializer(
            categories,
            many=True
        )

        return Response(serializer.data)


# ============================================================
# PRODUCTS
# ============================================================

class ProductListView(APIView):

    def get(self, request):

        queryset = Product.objects.select_related(
            "category"
        ).all()

        # ----------------------------------------------------
        # CATEGORY FILTER
        # ----------------------------------------------------

        category_slug = request.query_params.get("category")

        if category_slug and category_slug.lower() != "all":
            queryset = queryset.filter(
                category__slug__iexact=category_slug
            )

        # ----------------------------------------------------
        # BRAND FILTER
        # ----------------------------------------------------

        brand = request.query_params.get("brand")

        if brand and brand.lower() != "all":
            queryset = queryset.filter(
                brand__iexact=brand
            )

        # ----------------------------------------------------
        # SPORT FILTER
        # ----------------------------------------------------

        sport = request.query_params.get("sport")

        if sport and sport.lower() != "all":
            queryset = queryset.filter(
                sport__iexact=sport
            )

        # ----------------------------------------------------
        # GENDER FILTER
        # ----------------------------------------------------

        gender = request.query_params.get("gender")

        if gender and gender.upper() != "ALL":

            gender = gender.upper()

            queryset = queryset.filter(
                Q(gender=gender) |
                Q(gender="UNISEX")
            )

        # ----------------------------------------------------
        # SEARCH
        # ----------------------------------------------------

        search_query = request.query_params.get("search")

        if search_query:

            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(brand__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(sport__icontains=search_query) |
                Q(category__name__icontains=search_query)
            )

        # ----------------------------------------------------
        # PRICE RANGE
        # ----------------------------------------------------

        min_price = request.query_params.get("min_price")
        max_price = request.query_params.get("max_price")

        if min_price:

            try:
                min_price = Decimal(min_price)
                queryset = queryset.filter(
                    price__gte=min_price
                )
            except (InvalidOperation, ValueError):
                pass

        if max_price:

            try:
                max_price = Decimal(max_price)
                queryset = queryset.filter(
                    price__lte=max_price
                )
            except (InvalidOperation, ValueError):
                pass

        # ----------------------------------------------------
        # STOCK FILTER
        # ----------------------------------------------------

        in_stock = request.query_params.get("in_stock")

        if in_stock == "true":
            queryset = queryset.filter(
                stock_quantity__gt=0
            )

        elif in_stock == "false":
            queryset = queryset.filter(
                stock_quantity=0
            )

        # ----------------------------------------------------
        # FEATURED
        # ----------------------------------------------------

        featured = request.query_params.get("featured")

        if featured == "true":
            queryset = queryset.filter(
                is_featured=True
            )

        # ----------------------------------------------------
        # SORTING
        # ----------------------------------------------------

        sort_by = request.query_params.get(
            "ordering",
            "featured"
        )

        if sort_by == "price_asc":

            queryset = queryset.order_by(
                "price"
            )

        elif sort_by == "price_desc":

            queryset = queryset.order_by(
                "-price"
            )

        elif sort_by == "rating":

            queryset = queryset.order_by(
                "-rating",
                "-reviews_count"
            )

        elif sort_by == "newest":

            queryset = queryset.order_by(
                "-created_at"
            )

        elif sort_by == "name_asc":

            queryset = queryset.order_by(
                "name"
            )

        elif sort_by == "name_desc":

            queryset = queryset.order_by(
                "-name"
            )

        else:

            # Default frontend ordering
            queryset = queryset.order_by(
                "-is_featured",
                "-rating",
                "-created_at"
            )

        # ----------------------------------------------------
        # SERIALIZE
        # ----------------------------------------------------

        serializer = ProductSerializer(
            queryset,
            many=True
        )

        return Response({
            "count": queryset.count(),
            "products": serializer.data
        })


# ============================================================
# PRODUCT DETAIL
# ============================================================

class ProductDetailView(APIView):

    def get(self, request, pk_or_slug):

        try:

            if pk_or_slug.isdigit():

                product = Product.objects.select_related(
                    "category"
                ).get(
                    pk=int(pk_or_slug)
                )

            else:

                product = Product.objects.select_related(
                    "category"
                ).get(
                    slug=pk_or_slug
                )

            serializer = ProductSerializer(product)

            return Response(serializer.data)

        except Product.DoesNotExist:

            return Response(
                {
                    "error": "Product not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )


# ============================================================
# CREATE ORDER
# ============================================================

class CreateOrderView(APIView):

    @transaction.atomic
    def post(self, request):

        data = request.data
        items_data = data.get("items", [])

        # ----------------------------------------------------
        # BASIC VALIDATION
        # ----------------------------------------------------

        if not items_data:

            return Response(
                {
                    "error": "Order must contain at least one item."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        customer_name = data.get(
            "customer_name",
            "Valued Athlete"
        )

        email = data.get(
            "email",
            "customer@example.com"
        )

        phone = data.get("phone", "")
        address = data.get("address", "")
        city = data.get("city", "")
        state = data.get("state", "")
        pincode = data.get("pincode", "")

        payment_method = data.get(
            "payment_method",
            "UPI"
        ).upper()

        # ----------------------------------------------------
        # VALID PAYMENT METHOD
        # ----------------------------------------------------

        valid_payment_methods = {
            choice[0]
            for choice in Order.PAYMENT_METHODS
        }

        if payment_method not in valid_payment_methods:

            return Response(
                {
                    "error": "Invalid payment method."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # ----------------------------------------------------
        # BUILD ORDER ITEMS FROM DATABASE
        # ----------------------------------------------------

        order_items = []

        subtotal = Decimal("0.00")

        for item in items_data:

            product_id = item.get("product_id")

            if not product_id:

                return Response(
                    {
                        "error": "Each order item must contain product_id."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:

                quantity = int(
                    item.get("quantity", 1)
                )

            except (TypeError, ValueError):

                return Response(
                    {
                        "error": "Invalid product quantity."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            if quantity <= 0:

                return Response(
                    {
                        "error": "Quantity must be greater than zero."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Lock product row while processing order
            try:

                product = Product.objects.select_for_update().get(
                    pk=product_id
                )

            except Product.DoesNotExist:

                return Response(
                    {
                        "error": f"Product {product_id} not found."
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            # ------------------------------------------------
            # STOCK CHECK
            # ------------------------------------------------

            if product.stock_quantity < quantity:

                return Response(
                    {
                        "error": (
                            f"Only {product.stock_quantity} "
                            f"unit(s) of '{product.name}' "
                            f"are available."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # ------------------------------------------------
            # USE DATABASE PRICE
            # ------------------------------------------------

            item_price = product.price

            item_total = (
                item_price *
                Decimal(quantity)
            )

            subtotal += item_total

            order_items.append({
                "product": product,
                "product_name": product.name,
                "size": item.get("size", ""),
                "color": item.get("color", ""),
                "quantity": quantity,
                "price": item_price,
            })

        # ----------------------------------------------------
        # COUPON / DISCOUNT
        # ----------------------------------------------------

        coupon_code = data.get(
            "coupon_code",
            ""
        ).strip().upper()

        discount = Decimal("0.00")

        if coupon_code:

            coupon = ValidateCouponView.VALID_COUPONS.get(
                coupon_code
            )

            if coupon:

                discount = (
                    subtotal *
                    Decimal(coupon["percent"]) /
                    Decimal("100")
                )

                discount = discount.quantize(
                    Decimal("0.01")
                )

        # ----------------------------------------------------
        # SHIPPING
        # ----------------------------------------------------

        # Free shipping above ₹999
        # Otherwise ₹49

        if subtotal - discount >= Decimal("999.00"):

            shipping_fee = Decimal("0.00")

        else:

            shipping_fee = Decimal("49.00")

        # ----------------------------------------------------
        # FINAL TOTAL
        # ----------------------------------------------------

        total = (
            subtotal -
            discount +
            shipping_fee
        )

        # ----------------------------------------------------
        # PAYMENT STATUS
        # ----------------------------------------------------

        if payment_method == "COD":

            payment_status = "PENDING"

        else:

            # For the current frontend flow.
            # Real payment gateway verification should
            # eventually update this after successful payment.
            payment_status = "PAID"

        # ----------------------------------------------------
        # CREATE ORDER
        # ----------------------------------------------------

        order = Order.objects.create(

            customer_name=customer_name,

            email=email,

            phone=phone,

            address=address,

            city=city,

            state=state,

            pincode=pincode,

            payment_method=payment_method,

            payment_status=payment_status,

            subtotal=subtotal,

            discount=discount,

            shipping_fee=shipping_fee,

            total=total,

            status="CONFIRMED",
        )

        # ----------------------------------------------------
        # CREATE ORDER ITEMS + REDUCE STOCK
        # ----------------------------------------------------

        for item in order_items:

            product = item["product"]
            quantity = item["quantity"]

            OrderItem.objects.create(

                order=order,

                product=product,

                product_name=item["product_name"],

                size=item["size"],

                color=item["color"],

                quantity=quantity,

                price=item["price"],
            )

            # Reduce inventory
            product.stock_quantity -= quantity

            product.in_stock = (
                product.stock_quantity > 0
            )

            product.save(
                update_fields=[
                    "stock_quantity",
                    "in_stock",
                    "updated_at",
                ]
            )

        # ----------------------------------------------------
        # RESPONSE
        # ----------------------------------------------------

        serializer = OrderSerializer(order)

        return Response(
            {
                "message": "Order placed successfully!",
                "order": serializer.data
            },
            status=status.HTTP_201_CREATED
        )


# ============================================================
# COUPON VALIDATION
# ============================================================

class ValidateCouponView(APIView):

    VALID_COUPONS = {

        "MANGAL20": {
            "percent": 20,
            "description": (
                "20% OFF Anand Mangal Special Discount"
            ),
        },

        "PUMA15": {
            "percent": 15,
            "description": (
                "15% OFF Athletic Drop Discount"
            ),
        },

        "SPEED10": {
            "percent": 10,
            "description": (
                "10% OFF Forever Faster Promo"
            ),
        },

        "FIRSTBUY": {
            "percent": 12,
            "description": (
                "12% OFF First Order"
            ),
        },
    }

    def post(self, request):

        code = request.data.get(
            "code",
            ""
        ).strip().upper()

        if code in self.VALID_COUPONS:

            coupon = self.VALID_COUPONS[code]

            return Response({
                "valid": True,
                "code": code,
                "percent": coupon["percent"],
                "description": coupon["description"],
            })

        return Response(
            {
                "valid": False,
                "error": "Invalid or expired coupon code."
            },
            status=status.HTTP_400_BAD_REQUEST
        )