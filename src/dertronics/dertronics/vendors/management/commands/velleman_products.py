
from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, \
                        FileTransferSpeed, FormatLabel, Percentage, \
                        ProgressBar, ReverseBar, RotatingMarker, \
                        SimpleProgress, Timer
import time

from django.core.management.base import BaseCommand
from dertronics.vendors.velleman.client import Client
from dertronics.shop.client import Shop

class Command(BaseCommand):
    help = 'Velleman Product Sync'

    def handle(self, *args, **options):

        velleman = Client()
        dertronics = Shop()

        shop_products = dertronics.get_products_by_vendor(vendor=velleman.code)
        velleman_products = velleman.get_products_list()

        products_add = velleman_products.difference(shop_products)
        products_delete = shop_products.difference(velleman_products)
        products_update = shop_products.intersection(velleman_products)

        if len(products_add) > 0:
            pbar = self.new_progress_bar('Add Products', len(products_add))
            for number, product in enumerate(products_add):
                #start = time.time()
                try:
                    vp = velleman.process_product_data(product)
                    dertronics.process_add_product(vp)
                except:
                    print "FAILD ADDING : %s" % product
                    pass

                #elapsed = (time.time() - start)
                #print 'One Product %s' % (elapsed)

                pbar.update(number+1)
            pbar.finish()

#        if len(products_update) > 0:
#            pbar = self.new_progress_bar('Update Products', len(products_update))
#            for number, product in enumerate(products_update):
#                print 36 * '-'
#                start = time.clock()
#                vp = velleman.process_update_product(product)
#                dertronics.process_update_product(vp)
#                elapsed = (time.clock() - start)
#                print 'One Product %s' % (elapsed)
#                print 36 * '-'
#                pbar.update(number+1)
#            pbar.finish()

#        if len(products_delete) > 0:
#            pbar = self.new_progress_bar('Delete Products', len(products_delete))
#            for number, product in enumerate(products_delete):
#                pbar.update(number+1)
#            pbar.finish()


    def new_progress_bar(self, title, max_val):
        return ProgressBar(widgets=['%s (%s): ' % (title, max_val), Percentage(), Bar(), ETA()], maxval=max_val).start()


#

#        for product in products_add:
#            vp = velleman.process_add_product(product)
#            dertronics.process_add_product(vp)
#
#        for product in products_delete:
#            vp = velleman.process_delete_product(product)
#            dertronics.process_delete_product(vp)


#        for popular_product in velleman.get_products_list():
#            product = velleman.get_product(popular_product.value)
#
#            # Description (short)
#            short_description = product.Description
#
#            # Description (long)
#            try:
#                long_description  = short_description
#                long_description += "\n"
#
#                for line in product.Features.Feature:
#                    if type(line) == tuple:
#                        long_description += "\n" + unicode(line[1])
#                    else:
#                        long_description += "\n" + unicode(line.value)
#            except :
#                long_description = short_description
#
#            # Weight
#            if product.Weight._unit == 'g':
#                weight = Decimal(product.Weight.value) / 1000
#            else:
#                weight = Decimal(product.Weight.value)
#
#            # Price
#            productprice = product.Prices.Price
#            if type(productprice) == list():
#                price = Decimal(productprice[0].value.replace(',','.'))
#            else:
#                price = Decimal(productprice.value.replace(',','.'))
#
#            # Update data
#            data = {
#                'sku': unicode(product.Name),
#                'name'    : unicode(product.Name),
#                'websites' : [1],
#                'short_description' : unicode(short_description),
#                'description'       : unicode(long_description),
#                'status'            : 1,
#                'weight'            : float(weight),
#                'tax_class_id'      : 2,
#                'price'             : float(price),
#                'manufacturer':   'velleman',
#            }
#
#            response = dertronics.create_product(data['sku'], data, producttypes[0]['set_id'])
#
#            # Images
#            for image in product.Images.Image:
#                dertronics.add_product_image(data['sku'], 'http://www.velleman.eu/images/products/{0}'.format(image))