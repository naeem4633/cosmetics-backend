from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from .models import Product, SavedItem
from .views import product_list, product_detail, saveditem_list, saveditem_detail, saveditem_create, saveditem_delete

class ProductViewTests(TestCase):

    def test_product_list(self):
        """
        Test that the product_list view returns a list of products.
        """
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_product_detail(self):
        """
        Test that the product_detail view returns a single product.
        """
        product = Product.objects.create(name='Test Product', price=100.00)
        response = self.client.get(reverse('product-detail', args=[product.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], product.name)
        self.assertEqual(response.data['price'], product.price)


class SavedItemViewTests(TestCase):

    def test_saveditem_list(self):
        """
        Test that the saveditem_list view returns a list of saved items.
        """
        saveditem = SavedItem.objects.create(product_id=1, quantity=1)
        response = self.client.get(reverse('saveditem-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_saveditem_detail(self):
        """
        Test that the saveditem_detail view returns a single saved item.
        """
        saveditem = SavedItem.objects.create(product_id=1, quantity=1)
        response = self.client.get(reverse('saveditem-detail', args=[saveditem.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['product_id'], saveditem.product_id)
        self.assertEqual(response.data['quantity'], saveditem.quantity)

    def test_saveditem_create(self):
        """
        Test that the saveditem_create view creates a new saved item.
        """
        data = {'product_id': 1, 'quantity': 1}
        response = self.client.post(reverse('saveditem-list'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['product_id'], data['product_id'])
        self.assertEqual(response.data['quantity'], data['quantity'])

    def test_saveditem_delete(self):
        """
        Test that the saveditem_delete view deletes a saved item.
        """
        saveditem = SavedItem.objects.create(product_id=1, quantity=1)
        response = self.client.delete(reverse('saveditem-detail', args=[saveditem.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(SavedItem.objects.count(), 0)
