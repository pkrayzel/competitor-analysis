from graphqlclient import GraphQLClient
import json

GRAPH_QL_API = "http://es-elastigraph.made.com/graphql"


def get_products_page(api_client, page):
    result = api_client.execute('''
    {
      productsList(store: NL, page: %s) {
        pageInfo {
          endCursor
          pageSize
          total
          hasNextPage
        }
        edges {
          node {
            name
            magentoId
            url
            sku
            details
            price {
              includingTax
            }
            dimensions
          }
        }
      }
    }
    ''' % page)

    data = json.loads(result)

    return data


def create_default_value():
    return {
        "value": 0
    }


def convert_edge_to_product(edge):
    node = edge["node"]
    details = node["details"]

    dimensions = node["dimensions"]

    return {
        'sku': node["sku"],
        'product_id': node["magentoId"],
        'detail_url': node["url"],
        'title': node["name"],
        'price': node["price"]["includingTax"],
        'competitor': 'made',
        'height': dimensions.get("height", create_default_value()).get("value"),
        'width': dimensions.get("width", create_default_value()).get("value"),
        'weight': dimensions.get("weight", create_default_value()).get("value"),
        'packaging_dimensions': dimensions.get("packagingDimensions", create_default_value()).get("value"),
        'colour': ",".join(details["colour"]),
        'materials': ",".join(details["mainMaterials"])
    }


def store_products_to_file(products):
    with open("output/made.json", 'w') as output_file:
        json.dump(products, output_file, indent=4)


client = GraphQLClient(GRAPH_QL_API)

hasNextPage = True

products = []
page = 1
while hasNextPage:
    print(f"scraping page... {page}")
    data = get_products_page(client, page)

    products_list = data["data"]["productsList"]

    edges = products_list["edges"]

    print(f"number of products found: {len(edges)}")

    for item in edges:
        products.append(convert_edge_to_product(item))

    hasNextPage = products_list["pageInfo"]["hasNextPage"]
    page += 1

store_products_to_file(products)
