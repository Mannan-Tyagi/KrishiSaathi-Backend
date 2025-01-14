# urls.py in your app
from django.urls import path
from .views import *

urlpatterns = [
    path('get-commodity-details/', GetCommodityDetails.as_view(), name='get_commodity_details'),
    path('get-market-states/', GetMarketStates.as_view(), name='get_market_states'),
    path('get-market-districts/', GetMarketDistricts.as_view(), name='get_market_districts'),
    path('get-markets/', GetMarkets.as_view(), name='get_markets'),
    path('get-price-details/', GetPriceDetails.as_view(), name='get_price_details'),
    path('get-top6-market-prices/', GetTop6MarketPrices.as_view(), name='get_top6_market_prices'),
    path('get-commodity-forecast/', GetCommodityForecast.as_view(), name='get_commodity_forecast'),
    path('get-commodity/', GetAllCommoditiesInMarket.as_view(), name='get_commodity'),
    path('get-top6-forecast-price/', GetTop6CommodityForecast.as_view(), name='get_commodity_price'),
    path('commodity_prices/', CommodityPricesView.as_view(), name='commodity_prices'),
    path('seasonal-data/', SeasonalDataView.as_view(), name='seasonal-data'),

]
