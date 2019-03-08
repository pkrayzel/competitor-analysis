# https://aws.amazon.com/blogs/compute/parallel-processing-in-python-with-aws-lambda/
import time
from multiprocessing import Process, Pipe
import boto3


class VolumesParallel(object):
    """Finds total volume size for all EC2 instances"""

    def __init__(self):
        self.ec2 = boto3.resource('ec2')

    def scraping(self, conn):
        print(f"doing some stuff - ideally scraping: {conn}")

        conn.send(["s"])
        conn.close()


    def run_spider(self):
        # create a pipe for communication
        parent_conn, child_conn = Pipe()

        # create the process, pass instance and connection
        process = Process(target=self.scraping, args=(child_conn,))

        process.start()
        process.join()

        return parent_conn.recv()[0]



def lambda_handler(event, context):
    volumes = VolumesParallel()
    _start = time.time()
    result = volumes.run_spider()

    print(f"Result: {result}")
    print("Sequential execution time: %s seconds" % (time.time() - _start))


if __name__ == "__main__":
    lambda_handler("", "")
