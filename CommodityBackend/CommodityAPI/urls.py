# urls.py in your app
from django.urls import path
from . import views

urlpatterns = [
    path('get-commodity-details/', views.GetCommodityDetails.as_view(), name='get_commodity_details'),
    path('get-market-states/', views.GetMarketStates.as_view(), name='get_market_states'),
    path('get-market-districts/', views.GetMarketDistricts.as_view(), name='get_market_districts'),
    path('get-markets/', views.GetMarkets.as_view(), name='get_markets'),
    path('get-price-details/', views.GetPriceDetails.as_view(), name='get_price_details'),
    path('get-top6-market-prices/', views.GetTop6MarketPrices.as_view(), name='get_top6_market_prices'),
    path('get-commodity-forecast/', views.GetCommodityForecast.as_view(), name='get_commodity_forecast'),
    path('get-commodity/', views.GetAllCommoditiesInMarket.as_view(), name='get_commodity'),
    path('get-top6-forecast-price/', views.GetTop6CommodityForecast.as_view(), name='get_commodity_price'),
    path('commodity_prices/', views.CommodityPricesView.as_view(), name='commodity_prices'),
    path('seasonal-data/', views.SeasonalDataView.as_view(), name='seasonal-data'),
    path('commodities-count/', views.CommoditiesCount.as_view(), name='commodities-count'),
    path('nearest-market/', views.NearestMarketView.as_view(), name='nearest-market'),
]
