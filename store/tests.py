from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Category, Product, Order

class StoreAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(
            name="Running",
            slug="running",
            description="High speed road running gear"
        )
        self.product = Product.objects.create(
            name="AMS Velocity Nitro Test",
            slug="ams-velocity-nitro-test",
            category=self.category,
            sport="Running",
            price=5999.00,
            original_price=7999.00,
            primary_image="https://example.com/shoe.jpg",
            available_sizes=["UK 8", "UK 9"],
            in_stock=True,
            is_featured=True
        )

    def test_category_list_api(self):
        response = self.client.get('/api/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_product_list_api(self):
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_product_detail_api(self):
        response = self.client.get(f'/api/products/{self.product.slug}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "AMS Velocity Nitro Test")

    def test_coupon_validation_api(self):
        # Valid coupon
        response = self.client.post('/api/validate-coupon/', {'code': 'MANGAL20'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['valid'])
        self.assertEqual(response.data['percent'], 20)

        # Invalid coupon
        bad_response = self.client.post('/api/validate-coupon/', {'code': 'INVALID99'}, format='json')
        self.assertEqual(bad_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_api(self):
        order_payload = {
            'customer_name': 'Aarav Patel',
            'email': 'aarav@example.com',
            'phone': '9876543210',
            'address': 'Marine Drive',
            'city': 'Mumbai',
            'state': 'Maharashtra',
            'pincode': '400020',
            'payment_method': 'UPI',
            'subtotal': 5999.00,
            'discount': 1199.80,
            'shipping_fee': 0.00,
            'total': 4799.20,
            'items': [
                {
                    'product_id': self.product.id,
                    'name': self.product.name,
                    'size': 'UK 8',
                    'quantity': 1,
                    'price': 5999.00
                }
            ]
        }
        response = self.client.post('/api/orders/', order_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('order', response.data)
        self.assertTrue(response.data['order']['order_number'].startswith('AMS-'))
