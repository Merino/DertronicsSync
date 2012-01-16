
from suds.client import Client as SoapClient
from suds.transport.http import HttpAuthenticated


class Client(object):

    def __init__(self):
        url = 'https://portal.velleman.eu/ServicePortal/WebServices/ProductServices.asmx?WSDL'

        self.client = SoapClient(url, transport=HttpAuthenticated(), username='cubeit01', password='dD2Bq7')

        token = self.client.factory.create('AuthenticationHeader')
        token.Username = 'cubeit01'
        token.Password = 'dD2Bq7'
        self.client.set_options(soapheaders=token)

    def get_product(self, product_name):
        return self.client.service.GetProductInfo(product_name, 'nl').Product

    def get_popular_products(self):
        return self.client.service.GetPopularProducts().ProductList.Products.Product
