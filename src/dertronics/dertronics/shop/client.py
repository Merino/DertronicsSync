from decimal import Decimal
import time
from pygento import Magento

import os

class Image(object):

    url = None
    label = None
    position = 0
    frontpage = False

    def __init__(self, url):
        self.url = url

class Product(object):

    sku = None
    id = None
    vendor = None
    data = None

    title = None
    short_description = None
    long_description = None

    weight = Decimal('0')
    price = Decimal('0')
    stock = Decimal('0')

    images = []

    def __init__(self, sku=None, vendor=None, data=None, id=None):
        self.sku = sku
        self.vendor = vendor
        self.data = data
        self.images = []
    
    def __unicode__(self):
        return '<Product: %s by %s>' % (self.sku, self.vendor.title())

    def __str__(self):
        return self.__unicode__()

    def __repr__(self):
        return self.__unicode__()

    def _get_key(self):
        return "%s-%s" % (self.vendor, self.sku)

    def __cmp__(self, other):
        return cmp(self.__hash__(), other.__hash__())

    def __hash__(self):
        return hash(self._get_key())

    def as_structure(self):
        data = {
            #'sku'               : unicode(self.sku),
            'name'              : unicode(self.title).encode('ascii', 'xmlcharrefreplace'),
            'websites'          : [1],
            'short_description' : unicode(self.short_description).encode('ascii', 'xmlcharrefreplace'),
            'description'       : unicode(self.long_description).encode('ascii', 'xmlcharrefreplace'),
            'status'            : 1,
            'weight'            : float(self.weight),
            'tax_class_id'      : 2,
            'price'             : float(self.price),
            'stock_data' : {
                'qty': int(self.stock),
                'manage_stock': 1,
                'use_config_manage_stock': 1
            }
        }
        return data

#class Shop(object):
#
#    def __init__(self):
#
#        from suds.client import Client
#        from suds.xsd.doctor import ImportDoctor, Import
#
#        #soap_url = 'http://dertronics.com/index.php/api/v2_soap/'
#        soap_url = 'http://www.vestax.nl/index.php/api/v2_soap/'
#        wsdl_url = 'file://' + os.path.join(os.path.dirname(__file__), 'Magento-1.wsdl')
#
#        imp = Import('http://schemas.xmlsoap.org/soap/encoding/')
#        d = ImportDoctor(imp)
#
#        self.client = Client(url=wsdl_url, location=soap_url, doctor=d)
#        self.session = self.client.service.login('api', 'Welkom01')
#
#    def productInfo(self, sku):
#        return self.client.service.catalogProductInfo(self.session, sku)
#
#    def get_products_by_filter(self, filter=None, store=1):
#        result = self.client.service.catalogProductList(self.session, filter, store)
#
#        print result
#
#        return self.client.service.catalogProductList(self.session, filter, store).complexObjectArray
#
##    def _call(self, req, *args, **kwargs):
##        return self.client.service.call('catalog_product.list', [])
##
##
##
##
##        from suds.client import Client
##        from suds.xsd.doctor import ImportDoctor, Import
##
##        #imp = Import('http://schemas.xmlsoap.org/soap/encoding/')
##        #imp.filter.add('http://schemas.xmlsoap.org/soap/envelope/')
##
##        self.client = Client(
##            url=wsdl_url,
##            doctor=ImportDoctor(Import('http://schemas.xmlsoap.org/soap/encoding/'))
##        )
##        self.session = self.client.service.login('api', 'Welkom01')
#
#    #def update_product(self, sku, data):
#    #    return self.client.updateProductData(sku, data)
#
#    #def create_product(self, sku, data):
#    #    '''Updates the products for the product with the given sku'''
#    #    return self.client.createProduct(sku, data, self.producttype)
#
##    def add_product_image(self, sku, image, exclude=False):
##        '''Adds an image to a product'''
##        import urllib2
##        import base64
##
##        if image.frontpage:
##            types = ['image', 'small_image']
##        else:
##            types = []
##
##        encoded_string = base64.b64encode(urllib2.build_opener().open(image.url).read())
##        image_data = {  'label':image.label,
##                        'exclude': exclude,
##                      'position': image.position,
##                      'types': types,
##                      'file': {'content': encoded_string,
##                               'mime': 'image/jpeg'}}
##        return self.client._call('catalog_product_attribute_media.create', [sku, image_data])
#
#    def get_all_products(self):
#
#        result = self.get_products_by_filter().__dict__
#
#        return result
#
##    def get_products_by_filter(self, filter=None):
##        return self.client.service.catelogProductList(self.session)
##
##        #return self.call('catalog_product.list', filter)
#
#    def get_products_by_vendor(self, vendor=None):
#        product_set = set()
#        for item in self.get_products_by_filter():
#            #print 'item---'
#            #print result
#            #item = result.catalogProductEntity
#            #print result.product_id
#
#            #for item in result.item:
#            #    if item.key[0] == 'sku':
#            #        sku = item.value[0]
#            product = Product(sku=item.sku, vendor=vendor, id=item.product_id)
#            product_set.add(product)
#        return product_set
#
##    def process_update_product(self, product):
##        self.client.updateProductStock(product.sku, product.stock)
##
##    def process_delete_product(self, product):
##        return product
##
#    def process_add_product(self, product):
#        #self.client.service.catalog_product.create(product.sku, product.as_structure(), int(1))
#        self.client.service.catalogProductCreate(self.session, 'simple', 4, product.sku, product.as_structure())
#
#        #for image in product.images:
#        #    self.add_product_image(product.sku, image)
#
#    def update_stock(self, sku, stock):
#        start = time.time()
#
#        is_in_stock = 0
#        if stock > 0:
#            is_in_stock = 1
#            stock = int(stock)
#        else:
#            stock = 0
#        data = {'qty':stock, 'is_in_stock':is_in_stock}
#
#        self.client.service.catalogInventoryStockItemUpdate(self.session, sku, data)
#
#        elapsed = (time.time() - start)
#
#        print 5 * ' ' + '[%s] Update Dertronics' % (elapsed)
#        return stock



class Shop(object):

    def __init__(self):
        self.client = Magento(url='http://www.vestax.nl/index.php/api/xmlrpc/',
            username="api",
            apikey="Welkom01")
        # default producttype
        self.producttype =  self.client.getProductTypes()

    def update_product(self, sku, data):
        return self.client.updateProductData(sku, data)

    def create_product(self, sku, data):
        '''Updates the products for the product with the given sku'''
        return self.client.createProduct(sku, data, self.producttype)

    def add_product_image(self, sku, image, exclude=False):
        '''Adds an image to a product'''
        import urllib2
        import base64

        if image.frontpage:
            types = ['image', 'small_image']
        else:
            types = []

        encoded_string = base64.b64encode(urllib2.build_opener().open(image.url).read())
        image_data = {  'label':image.label,
                        'exclude': exclude,
                        'position': image.position,
                        'types': types,
                        'file': {'content': encoded_string,
                        'mime': 'image/jpeg'}}
        return self.client._call('catalog_product_attribute_media.create', [sku, image_data])

    def get_all_products(self):
        return self.get_products_by_filter()

    def get_products_by_filter(self, filter=None):
        return self.client.listProduct()

    def get_products_by_vendor(self, vendor=None):
        product_set = set()
        for result in self.get_products_by_filter():
            product = Product(sku=result['sku'], vendor=vendor)
            product_set.add(product)
        return product_set

    def process_update_product(self, product):
        return self.client.updateProductData(product.sku, product.as_structure)

    def process_delete_product(self, product):
        return product

    def process_add_product(self, product):
        self.client.createProduct(product.sku, product.as_structure(), int(self.producttype[0]['set_id']))
        for image in product.images:
            self.add_product_image(product.sku, image)

    def update_stock(self, sku, stock):
        start = time.time()

        #is_in_stock = 0
        #if stock > 0:
        #    is_in_stock = 1
        #    stock = int(stock)
        #else:
        #    stock = 0
        #data = {'qty':stock, 'is_in_stock':is_in_stock}

        self.client.updateProductStock(sku, stock)

        elapsed = (time.time() - start)

        #print 5 * ' ' + '[%s] Update Dertronics' % (elapsed)
        return stock
