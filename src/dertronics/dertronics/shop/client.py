from decimal import Decimal
from pygento import Magento

class Product(object):

    sku = None
    vendor = None
    data = None

    title = None
    short_description = None
    long_description = None

    weight = Decimal('0')
    price = Decimal('0')

    images = list()

    def __init__(self, sku=None, vendor=None, data=None):
        self.sku = sku
        self.vendor = vendor
        self.data = None
    
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
            'sku'               : unicode(self.sku),
            'name'              : unicode(self.title),
            'websites'          : [1],
            'short_description' : unicode(self.short_description),
            'description'       : unicode(self.long_description),
            'status'            : 1,
            'weight'            : float(self.weight),
            'tax_class_id'      : 2,
            'price'             : float(self.price),
        }
        return data

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

    def add_product_image(self, sku, path_url, exclude=False, position=0, types=[]):
        '''Adds an image to a product'''
        import urllib2
        import base64

        #opener1 = urllib2.build_opener().open(path_url).read()
        #image = opener1
        encoded_string = base64.b64encode(urllib2.build_opener().open(path_url).read())
        image_data = {  'label':path_url,
                        'exclude': exclude,
                      'position': position,
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
