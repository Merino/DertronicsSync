"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from client import Product

class ProductTest(TestCase):

    def test_basic_product_compares(self):

        product_A = Product(sku="new product", vendor="vendor_A")
        product_B = Product(sku="new product", vendor="vendor_A")
        product_C = Product(sku="different product", vendor="vendor_A")

        self.assertTrue(product_A == product_B)
        self.assertFalse(product_A == product_C)

        product_D = Product(sku="same sku", vendor="Vendor A")
        product_E = Product(sku="same sku", vendor="Vendor B")

        self.assertFalse(product_D == product_E)

    def test_compare_product_set(self):

        product_A = Product(sku="AA", vendor="vendor_A")
        product_B = Product(sku="BB", vendor="vendor_A")
        product_C = Product(sku="CC", vendor="vendor_A")
        product_D = Product(sku="DD", vendor="vendor_A")
        product_E = Product(sku="EE", vendor="vendor_A")
        product_F = Product(sku="FF", vendor="vendor_A")

        set_A = set([product_A, product_B, product_C])
        set_B = set([product_D, product_E, product_F])

        sub_A = set([product_A, product_B])
        sub_B = set([product_D, product_E])

        sub_AB = set([product_A,product_D])

        print set_A.difference(sub_AB)

        #self.assertEqual(set_A.difference(sub_AB), set_A)

        
