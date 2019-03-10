import os

def handler(event, context): 
  os.system("aws s3 sync s3://made-dev-competitor-analysis/category-product-pages/2019-03-08 /tmp/")
  print("Done that successfully")

