from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
from .DB_Operations import *
from .serializer import *

class GetCommodityDetails(APIView):
    def post(self, request):
        try:
            # Get the market_id from the request body
            market_id = request.data.get('market_id')
            if not market_id:
                return Response({'error': 'Market ID is required'}, status=status.HTTP_400_BAD_REQUEST)

            # Fetch commodity details using the market ID
            commodity_details = Commodity_Ops.get_commodity_by_market_id(market_id)

            # Serialize the data
            serializer = CommodityDetailsSerializer(commodity_details, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)  # Returns the serialized data
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetMarketStates(APIView):
    def get(self, request):
        try:
            # Fetch all market states
            market_states = Market_Ops.get_market_states()
            serializer = MarketStatesSerializer(market_states, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetMarketDistricts(APIView):
    def post(self, request):
        try:
            # Get the market state from the request body
            market_state = request.data.get('market_state')
            if not market_state:
                return Response({'error': 'Market state is required'}, status=status.HTTP_400_BAD_REQUEST)

            # Fetch market districts by state
            market_districts = Market_Ops.get_market_districts(market_state)
            serializer = MarketDistrictsSerializer(market_districts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetMarkets(APIView):
    def post(self, request):
        try:
            market_district = request.data.get('market_district')
            if not market_district:
                return Response({'error': 'Market district are required'}, status=status.HTTP_400_BAD_REQUEST)

            # Fetch markets by state and district
            markets = Market_Ops.get_markets(market_district)
            serializer = MarketSerializer(markets, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetPriceDetails(APIView):
    def post(self, request):
        try:
            # Get the commodity_id from the request body
            commodity_id = request.data.get('commodity_id')
            market_id = request.data.get('market_id')
            if not commodity_id:
                return Response({'error': 'Commodity ID is required'}, status=status.HTTP_400_BAD_REQUEST)
            if not market_id:
                return Response({'error': 'Market ID is required'}, status=status.HTTP_400_BAD_REQUEST)
            # Fetch price details using the commodity ID
            price_details = Price_Ops.get_price_details(commodity_id,market_id)

            # Serialize the data
            serializer = PriceDetailsSerializer(price_details, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetTop6MarketPrices(APIView):
    def post(self, request):
        try:
            # Get the commodity_id from the request body
            commodity_id = request.data.get('commodity_id')
            if not commodity_id:
                return Response({'error': 'Commodity ID is required'}, status=status.HTTP_400_BAD_REQUEST)

            # Fetch top 6 market prices using the commodity ID
            top6_market_prices = Price_Ops.get_top6_market_prices(commodity_id)

            # Serialize the data
            serializer = Top6MarketPricesSerializer(top6_market_prices, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetCommodityForecast(APIView):
    def post(self, request):
        try:
            # Get the commodity_id from the request body
            commodity_id = request.data.get('commodity_id')
            market_id = request.data.get('market_id')
            if not commodity_id:
                return Response({'error': 'Commodity ID is required'}, status=status.HTTP_400_BAD_REQUEST)

            # Fetch commodity forecast using the commodity ID
            commodity_forecast = Forecast_Ops.get_forecasted_price(commodity_id,market_id)

            # Serialize the data
            serializer = CommodityForecastSerializer(commodity_forecast, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetAllCommoditiesInMarket(APIView):
    def post(self, request):
        try:
            # Get the market_id from the request body
            market_id = request.data.get('market_id')
            if not market_id:
                return Response({'error': 'Market ID is required'}, status=status.HTTP_400_BAD_REQUEST)

            # Fetch all commodities in a market using the market ID
            commodities = Price_Ops.get_all_commodities_in_market(market_id)

            # Serialize the data
            serializer = CommoditySerializer(commodities, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetTop6CommodityForecast(APIView):
    def post(self, request):
        try:
            # Get the market_id from the request body
            market_id = request.data.get('market_id')
            commodity_id = request.data.get('commodity_id')
            if not market_id:
                return Response({'error': 'Market ID is required'}, status=status.HTTP_400_BAD_REQUEST)

            # Fetch all commodities in a market using the market ID
            commodities = Forecast_Ops.get_top6_forecasted_price(commodity_id,market_id)

            # Serialize the data
            serializer = CommodityForecastSerializer(commodities, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CommodityPricesView(APIView):
    def post(self, request):
        try:
            # Extract the required parameters from the request body
            date_range = request.data.get('dateRange', 'All')  # Default to 'All' if not provided
            market_id = request.data.get('market_id')
            commodity_id = request.data.get('commodity_id')

            # Validation of required parameters
            if not market_id:
                return Response({'error': 'Market ID is required'}, status=status.HTTP_400_BAD_REQUEST)
            if not commodity_id:
                return Response({'error': 'Commodity ID is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Fetch commodity prices based on the provided parameters
            commodity_prices = Price_Ops.get_commodity_prices(date_range, market_id, commodity_id)

            # Serialize the fetched data
            serializer = CommodityPriceSerializer(commodity_prices, many=True)

            # Return the serialized data as a JSON response
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            # Return a generic error message in case of any exception
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SeasonalDataView(APIView):
    def post(self, request):
        try:
            # Extract the required parameters
            market_id = request.data.get('market_id')
            commodity_id = request.data.get('commodity_id')

            # Validate parameters
            if not market_id:
                return Response({'error': 'Market ID is required'}, status=status.HTTP_400_BAD_REQUEST)
            if not commodity_id:
                return Response({'error': 'Commodity ID is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Fetch data
            seasonal_data = SeasonalDataOps.get_seasonal_data(market_id, commodity_id)

            # Serialize data
            serializer = SeasonalDataSerializer(seasonal_data, many=True)

            # Return response
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)