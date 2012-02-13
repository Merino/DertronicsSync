from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA,\
    FileTransferSpeed, FormatLabel, Percentage,\
    ProgressBar, ReverseBar, RotatingMarker,\
    SimpleProgress, Timer

from django.core.management.base import BaseCommand

from dertronics.vendors.velleman.client import Client
from dertronics.shop.client import Shop

import random
import multiprocessing
import Queue
from Queue import Queue
import thread

import time

velleman = Client()
dertronics = Shop()

class Worker(multiprocessing.Process):

    def __init__(self, work_queue, result_queue):

        # base class initialization
        multiprocessing.Process.__init__(self)

        # job management stuff
        self.work_queue = work_queue
        self.result_queue = result_queue
        self.kill_received = False

    def run(self):
        while not self.kill_received:

            shop = Shop()

            # get a task
            #job = self.work_queue.get_nowait()
            try:
                job = self.work_queue.get_nowait()
            except Queue.Empty:
                break

            # the actual processing
            ##print("Starting " + str(job) + " ...")

            product = job

            stock = velleman.get_stock(product.sku)
            shop.update_stock(product.sku, stock)

            shop.client.close()

            #delay = random.randrange(1,3)
            #time.sleep(delay)

            # store the result
            self.result_queue.put(product)

def worker(product):
    #item = q.get()
    #product = item
    shop = Shop()
    stock = velleman.get_stock(product.sku)
    shop.update_stock(product.sku, stock)

class Command(BaseCommand):
    help = 'Velleman Stocklevel Sync'

    #num_processes = 4
    def new_progress_bar(self, title, max_val):
        return ProgressBar(widgets=['%s (%s): ' % (title, max_val), Percentage(), Bar(), ETA()], maxval=max_val).start()

    def handle(self, *args, **options):

        start = time.time()
        shop_products = dertronics.get_products_by_vendor(vendor=velleman.code)

#        print "Update Products %s" % (len(shop_products))
#
#        import threading
#
#        num_worker_threads = 4
#
#        def do_work(item):
#            print item
#            return item
#

            #q.task_done()
#
#        q = Queue()
#        for i in range(num_worker_threads):
#            t = threading.Thread(target=worker)
#            t.daemon = True
#            t.start()
#
#        for item in shop_products:
#            q.put(item)
#        from multiprocessing import Pool
#        pool = Pool(processes=5)
#        for product in shop_products:
#            result = pool.apply_async(worker, [product])
#            #print result.get()

#        q.join()


    # run
        # load up work queue
#        work_queue = multiprocessing.Queue()
#        for product in shop_products:
#            work_queue.put(product)
#
#        # create a queue to pass to workers to store the results
#        result_queue = multiprocessing.Queue()

        # spawn workers


#        for i in range(self.num_processes):
#            t = thread(target=Worker(work_queue, result_queue))
#            t.daemon = True
#            t.start()
#
#            #worker = Worker(work_queue, result_queue)
#            #worker.start()
#
#        for item in source():
#            work_queue.put(item)
#
#        work_queue.join()

        #elapsed = (time.time() - start)
        #print '-'+ '[%s] Total time ' % (elapsed)
        # collect the results off the queue
        #results = []
        #for i in range(num_jobs):
        #    print(result_queue.get())

        pbar = self.new_progress_bar('Stock Update', len(shop_products))
        for number, product in enumerate(shop_products):

            try:
                stock = velleman.get_stock(product.sku)
                dertronics.update_stock(product.sku, stock)
            except :
                print "FAILED: %s" % product
                pass

            pbar.update(number+1)
        pbar.finish()