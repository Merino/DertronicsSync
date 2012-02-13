import copy
from decimal import Decimal
import os
import time
from suds.client import Client as SoapClient
from suds.transport.http import HttpAuthenticated

from dertronics.shop.client import Product, Image

class Client(object):

    code = 'velleman'

    def __init__(self):
        soap_url = 'https://portal.velleman.eu/ServicePortal/WebServices/ProductServices.asmx?WSDL'
        #wsdl_url = 'https://portal.velleman.eu/ServicePortal/WebServices/ProductServices.asmx?WSDL'
        wsdl_url = 'file://' + os.path.join(os.path.dirname(__file__), 'ProductServices.wsdl')



 #       self.client = SoapClient(url=wsdl_url, location=soap_url, transport=HttpAuthenticated(), username='cubeit01', password='dD2Bq7')
#
        self.client = SoapClient(url=wsdl_url, location=soap_url)
#
        cache = self.client.options.cache
        cache.setduration(days=10)
#
        token = self.client.factory.create('AuthenticationHeader')
        token.Username = 'cubeit01'
        token.Password = 'dD2Bq7'
        self.client.set_options(soapheaders=token)

        #from pysimplesoap.client import SoapClient
        #from pysimplesoap.simplexml import SimpleXMLElement

#        start = time.time()

        #self.client = SoapClient(wsdl=WSDL, action=soap_url, trace=False)
        #self.client['AuthenticationHeader'] = {'Username':'cubeit01', 'Password':'dD2Bq7'}
        #print self.client.xml_request

        #self.client['']

#        headers = SimpleXMLElement("<Header/>")
#        my_test_header = headers.add_child("AuthenticationHeader")
#        my_test_header.marshall('Username', 'cubeit01')
#        my_test_header.marshall('Password', 'dD2Bq7')

        #headers = SimpleXMLElement("<Headers/>")
        #my_test_header = headers.add_child("MyTestHeader")
        #my_test_header['xmlns'] = "service"
        #my_test_header.marshall('username', 'test')
        #my_test_header.marshall('password', 'password')

#        print headers.as_xml()
#
#        print headers
#
#        headers = SimpleXMLElement("<Header/>")
#        my_test_header = headers.add_child("MyTestHeader")
#        my_test_header['xmlns'] = "service"
#        my_test_header.marshall('username', 'test')
#        my_test_header.marshall('password', 'password')


#        result = self.client.service.GetProductStock('MK120', 10)
#
#        #print self.client.__dict__
#
#        #response = self.client.GetProductInfo('MK120', headers=headers)
#
#
#        elapsed = (time.time() - start)
#
#        print type(elapsed)
#
#        print 'stock request %s [%s]' % ('MK120', elapsed)


        #result = response['AddResult']#        print result


    def get_product(self, product_name):
        return self.client.service.GetProductInfo(product_name, 'nl').Product

    def get_products_list(self):
        product_set = set()
        for result in self.client.service.GetPopularProducts().ProductList.Products.Product:
            product = Product(sku=unicode(result.value), vendor=self.code, data=result)
            product_set.add(product)
        return product_set

    def get_stock(self, productName):

        start = time.time()

        client = copy.copy(self.client)

        result = client.service.GetProductStock(productName=productName, requiredQty=10).StockInfo
        elapsed = (time.time() - start)

        #print 5 * ' ' + '[%s] Get Stock Velleman' % (elapsed)

        return result

    def process_product_data(self, product):
        data = self.get_product(product.sku)

        # Title and Description
        product.title = "VELLEMAN %s - %s" % (data.Name, data.Description)
        product.short_description = data.Description

        long_description = ""

        # Description (technical)
        try:
            if unicode(data.TechnicalDescription):
                tech_description = data.TechnicalDescription + "<br /><br />"
                long_description += tech_description

        except AttributeError:
            pass
        
        try:
            # Description (features)
            long_description += "<h3>Kenmerken</h3>\n"
            long_description += "<ul>\n"

            for line in data.Features.Feature:
                if type(line) == tuple:
                    long_description +=  "<li>" + unicode(line[1]) + "</li> \n"
                else:
                    long_description +=  "<li>" + unicode(line.value) + "</li>\n"
    
            long_description += "</ul>\n"
        except :
            pass

        # Description (specifications)
        try:
            specs_description = "<br />"
            specs_description += "<h3>Specificaties</h3>\n"
            specs_description += "<ul>\n"

            for line in data.Specifications.Specification:
                if type(line) == tuple:
                    specs_description += "<li>" + unicode(line[1]) + "</li>\n"
                else:
                    specs_description += "<li>" + unicode(line.value) + "</li>\n"

            specs_description += "</ul>\n"

            long_description += specs_description
        except AttributeError:
            pass
        
        product.long_description = long_description

        # Price
        productprice = data.Prices.Price
        if isinstance(productprice, list):
            product.price = Decimal(productprice[0].value.replace(',','.'))
        else:
            product.price = Decimal(productprice.value.replace(',','.'))

        # Images
        images = data.Images.Image
        if isinstance(images, list):
            position = 0
            for image in images:
                new_image = Image(url='http://www.velleman.eu/images/products/{0}'.format(image))
                new_image.label = image.split('/')[-1]
                new_image.position = position + 1

                if new_image.label.split('.')[0].lower() == product.sku.lower():
                    new_image.frontpage = True

                if not new_image.frontpage:
                    if new_image.label.split('.')[0].lower() == ("%s_1" % product.sku.lower()):
                        new_image.frontpage = True

                product.images.append(new_image)
        else:
            new_image = Image(url='http://www.velleman.eu/images/products/{0}'.format(images))
            new_image.label = images.split('/')[-1]
            new_image.position = 1
            new_image.frontpage = True

            product.images.append(new_image)
        return product

    def process_update_product(self, product):
        data = self.get_stock(product.sku)
        product.stock = data.value
        return product

    #def process_delete_product(self, product):
    #    return product
