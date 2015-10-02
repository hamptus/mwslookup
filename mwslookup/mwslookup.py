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

def get_competitive(asin, condition='New'):
    conn = new_conn()
    resp = conn.get_competitive_pricing_for_asin(MarketplaceId=MarketplaceId, ASINList=[asin])
    try:
        sales_rank = resp.GetCompetitivePricingForASINResult[0].Product.SalesRankings.SalesRank[0].Rank
    except IndexError:
        sales_rank = 0
    for i in resp.GetCompetitivePricingForASINResult[0].Product.CompetitivePricing[0].CompetitivePrices.CompetitivePrice:
        if i['subcondition'] == condition:
            return i.Price.LandedPrice.Amount, sales_rank

def lookup(title):
    conn = new_conn()
    resp = conn.list_matching_products(MarketplaceId=MarketplaceId, Query=title)
    try:
        p = resp.ListMatchingProductsResult.Products.Product[0]
    except IndexError:
        return {}

    return_data = {}
    return_data['title'] = p.AttributeSets.ItemAttributes[0].Title
    return_data['length'] = p.AttributeSets.ItemAttributes[0].PackageDimensions.Length.Value
    return_data['width'] = p.AttributeSets.ItemAttributes[0].PackageDimensions.Width.Value
    return_data['height'] = p.AttributeSets.ItemAttributes[0].PackageDimensions.Height.Value
    return_data['weight'] = p.AttributeSets.ItemAttributes[0].PackageDimensions.Weight.Value

    #         return_data['fees'] = calculate_fees(return_data['length'], return_data['width'], return_data['height'], return_data['weight'])
    return_data['asin'] = p.Identifiers.MarketplaceASIN.ASIN

    return return_data
