from boto.mws import connection

try:
    from settings import MWSAccessKeyId, MWSSecretKey, MerchantId, MarketplaceId
except ImportError:
    raise ImportError("settings.py is missing. Rename settings.py-example and add your MWS credentials")

def new_conn():
    conn = connection.MWSConnection(
        aws_access_key_id=MWSAccessKeyId,
        aws_secret_access_key=MWSSecretKey,
        Merchant=MerchantId,
    )
    return conn

def lookup(title):
    conn = new_conn()
    resp = conn.list_matching_products(MarketplaceId=MarketplaceId, Query=title)
    p = resp.ListMatchingProductsResult.Products.Product[0]

    return_data = {}
    return_data['title'] = p.AttributeSets.ItemAttributes[0].Title
    return_data['list_price'] = p.AttributeSets.ItemAttributes[0].ListPrice.Amount
    return_data['length'] = p.AttributeSets.ItemAttributes[0].PackageDimensions.Length.Value
    return_data['width'] = p.AttributeSets.ItemAttributes[0].PackageDimensions.Width.Value
    return_data['height'] = p.AttributeSets.ItemAttributes[0].PackageDimensions.Height.Value
    return_data['weight'] = p.AttributeSets.ItemAttributes[0].PackageDimensions.Weight.Value

    #         return_data['fees'] = calculate_fees(return_data['length'], return_data['width'], return_data['height'], return_data['weight'])
    return_data['asin'] = p.Identifiers.MarketplaceASIN.ASIN
    return return_data
