from decimal import Decimal
from suds.client import Client as SoapClient
from suds.transport.http import HttpAuthenticated

from dertronics.shop.client import Product

class Client(object):

    code = 'velleman'

    def __init__(self):
        url = 'https://portal.velleman.eu/ServicePortal/WebServices/ProductServices.asmx?WSDL'

        self.client = SoapClient(url, transport=HttpAuthenticated(), username='cubeit01', password='dD2Bq7')

        token = self.client.factory.create('AuthenticationHeader')
        token.Username = 'cubeit01'
        token.Password = 'dD2Bq7'
        self.client.set_options(soapheaders=token)

    def get_product(self, product_name):
        return self.client.service.GetProductInfo(product_name, 'nl').Product

    def get_products_list(self):
        product_set = set()
        for result in self.client.service.GetPopularProducts().ProductList.Products.Product:
            product = Product(sku=unicode(result.value), vendor=self.code, data=result)
            product_set.add(product)
        return product_set

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
        except AttributeError:
            pass
        else:
            long_description += tech_description

        # Description (features)
        long_description += "<h3>Kenmerken</h3>"
        long_description += "<ul>"

        for line in data.Features.Feature:
            if type(line) == tuple:
                long_description +=  "<li>" + unicode(line[1]) + "</li>"
            else:
                long_description +=  "<li>" + unicode(line.value) + "</li>"

        long_description += "</ul>"

        # Description (specifications)
        try:
            specs_description = "<br />"
            specs_description += "<h3>Specificaties</h3>"
            specs_description += "<ul>"

            for line in data.Specifications.Specification:
                if type(line) == tuple:
                    specs_description += "<li>" + unicode(line[1]) + "</li>"
                else:
                    specs_description += "<li>" + unicode(line.value) + "</li>"

            specs_description += "</ul>"
        except AttributeError:
            pass
        else:
            long_description += specs_description

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
            for image in images:
                product.images.append('http://www.velleman.eu/images/products/{0}'.format(image))
        else:
            product.images.append('http://www.velleman.eu/images/products/{0}'.format(images))

        return product

    #def process_update_product(self, product):
    #    return product

    #def process_delete_product(self, product):
    #    return product
