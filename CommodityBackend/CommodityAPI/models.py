from django.db import models


class CommodityDetails(models.Model):
    commodity_id = models.IntegerField()
    commodity_name = models.CharField(max_length=255)
    commodity_variety = models.CharField(max_length=255)
    commodity_grade = models.CharField(max_length=255)

class MarketStates(models.Model):
    market_state = models.CharField(max_length=255)
class MarketDistricts(models.Model):
    market_district = models.CharField(max_length=255)
class MarketDetails(models.Model):
    market_id = models.IntegerField()
    market_name = models.CharField(max_length=255)
class PriceDetails(models.Model):
    arrival_date_string = models.CharField(max_length=50)  # Adjust max_length as needed
    min_price = models.DecimalField(max_digits=10, decimal_places=2)
    max_price = models.DecimalField(max_digits=10, decimal_places=2)
    modal_price = models.DecimalField(max_digits=10, decimal_places=2)
    commodity_name = models.CharField(max_length=255)
    commodity_variety = models.CharField(max_length=255)
    commodity_grade = models.CharField(max_length=255)
    second_latest_arrival_date = models.CharField(max_length=50)  # Adjust max_length as needed
    second_latest_max_price = models.DecimalField(max_digits=10, decimal_places=2)
    price_change = models.DecimalField(max_digits=10, decimal_places=2)
    percentage_change = models.DecimalField(max_digits=10, decimal_places=2)

class Top6MarketPrices(models.Model):
    market_id = models.IntegerField()
    commodity_id = models.IntegerField()
    arrival_date_string = models.CharField(max_length=50)
    min_price = models.DecimalField(max_digits=10, decimal_places=2)
    max_price = models.DecimalField(max_digits=10, decimal_places=2)
    modal_price = models.DecimalField(max_digits=10, decimal_places=2)
    market_name = models.CharField(max_length=255)
    market_district = models.CharField(max_length=255)
    market_state = models.CharField(max_length=255)

class CommodityForecast(models.Model):
    week = models.IntegerField()  # Week number
    avg_modal_price = models.DecimalField(max_digits=10, decimal_places=2)  # Average Modal Price
    avg_predicted_price = models.DecimalField(max_digits=10, decimal_places=2)  # Average Predicted Price
    diff = models.DecimalField(max_digits=10, decimal_places=2)

class Commodity(models.Model):
    commodity_id = models.AutoField(primary_key=True)  # Use AutoField if it is auto-incremented
    arrival_date = models.DateField()  # Use DateField for storing date
    modal_price = models.DecimalField(max_digits=10, decimal_places=2)  # Adjust max_digits and decimal_places as necessary
    commodity_name = models.CharField(max_length=255)

class CommodityMarketData(models.Model):
    year_value = models.IntegerField()
    month_value = models.IntegerField()
    month_name = models.CharField(max_length=3)
    avg_min_price = models.DecimalField(max_digits=10, decimal_places=2)
    avg_max_price = models.DecimalField(max_digits=10, decimal_places=2)
    avg_modal_price = models.DecimalField(max_digits=10, decimal_places=2)

class SeasonalData(models.Model):
    season = models.CharField(max_length=10)
    year_value = models.IntegerField()
    avg_min_price = models.DecimalField(max_digits=10, decimal_places=2)
    avg_max_price = models.DecimalField(max_digits=10, decimal_places=2)
    avg_modal_price = models.DecimalField(max_digits=10, decimal_places=2)

class CommodityCount(models.Model):
    count = models.IntegerField()
    
