from .models import *  # Import the model class
from .DB_Connection import DBConnection

class Commodity_Ops:
        
    @staticmethod
    def get_commodities_count():
        connection = DBConnection.database_connection()

        if connection is None:
            raise Exception("Failed to establish database connection.")

        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT COUNT(*) AS count FROM commoditydataanaylsis.dim_commoditydetails;")
            result = cursor.fetchone()  # Use fetchone since you only need one record

            if result:
                commodity_count_instance = CommodityCount()
                commodity_count_instance.count = result['count']
                return [commodity_count_instance]  # Return a list containing the instance
            else:
                raise Exception("Failed to fetch count from the database.")
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def get_commodity_by_market_id(cls, market_id):
        connection = DBConnection.database_connection()

        if connection is None:
            raise Exception("Failed to establish database connection.")

        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT Distinct d.* 
                FROM commoditydataanaylsis.dim_commoditydetails d
                INNER JOIN commoditydataanaylsis.fact_indiancommoditymarketdata_2024 f
                ON d.commodity_id = f.commodity_id
                WHERE f.market_id = %s;
            """, (market_id,))
            results = cursor.fetchall()

            CommodityDetails_list = []

            for row in results:
                commodity_instance = CommodityDetails()
                commodity_instance.commodity_id = row['commodity_id']
                commodity_instance.commodity_name = row['commodity_name']
                commodity_instance.commodity_variety = row['commodity_variety']
                commodity_instance.commodity_grade = row['commodity_grade']

                CommodityDetails_list.append(commodity_instance)

            return CommodityDetails_list
        finally:
            cursor.close()
            connection.close()
    
class Market_Ops:
    @classmethod
    def get_market_states(cls):
        connection = DBConnection.database_connection()

        if connection is None:
            raise Exception("Failed to establish database connection.")

        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT DISTINCT market_state FROM commoditydataanaylsis.dim_marketdetails order by market_state;")
            results = cursor.fetchall()

            MarketStates_list = []

            for row in results:
                MarketStates_instance = MarketStates()
                MarketStates_instance.market_state = row['market_state']
                MarketStates_list.append(MarketStates_instance)

            return MarketStates_list
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def get_market_districts(cls,market_state):
        connection = DBConnection.database_connection()

        if connection is None:
            raise Exception("Failed to establish database connection.")

        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT Distinct market_district FROM commoditydataanaylsis.dim_marketdetails where market_state = %s order by market_district;", (market_state,))
            results = cursor.fetchall()

            MarketDistricts_list = []

            for row in results:
                MarketDistricts_instance = MarketDistricts()
                MarketDistricts_instance.market_district = row['market_district']
                MarketDistricts_list.append(MarketDistricts_instance)

            return MarketDistricts_list
        finally:
            cursor.close()
            connection.close()
    @classmethod
    def get_markets(cls,market_district):
        connection = DBConnection.database_connection()

        if connection is None:
            raise Exception("Failed to establish database connection.")

        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT Distinct market_id, market_name FROM commoditydataanaylsis.dim_marketdetails where market_district = %s order by market_name;", (market_district,))
            results = cursor.fetchall()

            Market_list = []

            for row in results:
                Market_instance = MarketDetails()
                Market_instance.market_id = row['market_id']
                Market_instance.market_name = row['market_name']
                Market_list.append(Market_instance)

            return Market_list
        finally:
            cursor.close()
            connection.close()

class Price_Ops:
    @classmethod
    def get_price_details(cls,commodity_id,market_id):
        connection = DBConnection.database_connection()

        if connection is None:
            raise Exception("Failed to establish database connection.")

        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""WITH LatestPrices AS (
                SELECT DISTINCT
                    f.Min_Price,
                    f.Max_Price,
                    f.Modal_Price,
                    f.Arrival_Date_String,
                    d.commodity_name,
                    d.commodity_variety,
                    d.commodity_grade,
                    f.Arrival_Date,
                    ROW_NUMBER() OVER (PARTITION BY f.market_id, f.commodity_id ORDER BY f.Arrival_Date DESC) AS row_num
                FROM 
                    commoditydataanaylsis.dim_commoditydetails d
                INNER JOIN 
                    commoditydataanaylsis.fact_indiancommoditymarketdata_2024 f 
                    ON d.commodity_id = f.commodity_id
                WHERE 
                    f.market_id = %s
                    AND f.commodity_id = %s
            )
            SELECT 
                L1.Min_Price ,
                L1.Max_Price ,
                L1.Modal_Price,
                L1.Arrival_Date_String,
                L1.commodity_name,
                L1.commodity_variety,
                L1.commodity_grade,
                L2.Arrival_Date_String AS second_latest_arrival_date,
                L2.Max_Price AS second_latest_max_price,
                (L1.Max_Price - L2.Max_Price) AS price_change,
                ((L1.Max_Price - L2.Max_Price) / L2.Max_Price * 100) AS percentage_change
            FROM 
                LatestPrices L1
            JOIN 
                LatestPrices L2
            ON 
                L1.row_num = 1
                AND L2.row_num = 2;

            );""", (market_id,commodity_id,))
            results = cursor.fetchall()

            Price_list = []

            for row in results:
                Price_instance = PriceDetails()
                Price_instance.arrival_date_string = row['Arrival_Date_String']
                Price_instance.min_price = row['Min_Price']
                Price_instance.max_price = row['Max_Price']
                Price_instance.modal_price = row['Modal_Price']
                Price_instance.commodity_name = row['commodity_name']
                Price_instance.commodity_variety = row['commodity_variety']
                Price_instance.commodity_grade = row['commodity_grade']
                Price_instance.second_latest_arrival_date = row['second_latest_arrival_date']
                Price_instance.second_latest_max_price = row['second_latest_max_price']
                Price_instance.price_change = row['price_change']
                Price_instance.percentage_change = row['percentage_change']
                Price_list.append(Price_instance)

            return Price_list
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def get_top6_market_prices(cls,commodity_id):
        connection = DBConnection.database_connection()

        if connection is None:
            raise Exception("Failed to establish database connection.")

        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                WITH LatestCommodityDate AS (
                SELECT MAX(Arrival_Date) AS Latest_Arrival_Date
                FROM commoditydataanaylsis.fact_indiancommoditymarketdata_2024
                WHERE commodity_id = %s  
                ),
                RankedMarkets AS (
                    SELECT 
                        f.market_id,
                        f.commodity_id,
                        f.Arrival_Date_String, 
                        f.Min_Price, 
                        f.Max_Price, 
                        f.Modal_Price,
                        m.market_name, 
                        m.market_district, 
                        m.market_state,
                        ROW_NUMBER() OVER (PARTITION BY f.market_id ORDER BY f.Max_Price DESC) AS price_rank
                    FROM 
                        commoditydataanaylsis.fact_indiancommoditymarketdata_2024 f
                    INNER JOIN 
                        commoditydataanaylsis.dim_marketdetails m 
                        ON f.market_id = m.market_id
                    WHERE 
                        f.commodity_id = %s 
                        AND f.Arrival_Date BETWEEN (
                            SELECT DATE_SUB(Latest_Arrival_Date, INTERVAL 7 DAY)  
                            FROM LatestCommodityDate
                        ) AND (
                            SELECT Latest_Arrival_Date
                            FROM LatestCommodityDate
                        )
                )
                SELECT 
                    market_id,
                    commodity_id,
                    Arrival_Date_String, 
                    Min_Price, 
                    Max_Price, 
                    Modal_Price,
                    market_name, 
                    market_district, 
                    market_state
                FROM RankedMarkets
                WHERE price_rank = 1  
                ORDER BY Max_Price DESC  
                LIMIT 4;  
            """, (commodity_id,commodity_id,))
            results = cursor.fetchall()

            Top6MarketPrices_list = []

            for row in results:
                Top6MarketPrices_instance = Top6MarketPrices()
                Top6MarketPrices_instance.market_id = row['market_id']
                Top6MarketPrices_instance.commodity_id = row['commodity_id']
                Top6MarketPrices_instance.arrival_date_string = row['Arrival_Date_String']
                Top6MarketPrices_instance.min_price = row['Min_Price']
                Top6MarketPrices_instance.max_price = row['Max_Price']
                Top6MarketPrices_instance.modal_price = row['Modal_Price']
                Top6MarketPrices_instance.market_name = row['market_name']
                Top6MarketPrices_instance.market_district = row['market_district']
                Top6MarketPrices_instance.market_state = row['market_state']

                Top6MarketPrices_list.append(Top6MarketPrices_instance)

            return Top6MarketPrices_list
        finally:
            cursor.close()
            connection.close()
            
    @classmethod
    def get_all_commodities_in_market(cls,market_id):
        connection = DBConnection.database_connection()

        if connection is None:
            raise Exception("Failed to establish database connection.")

        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT DISTINCT 
                fimd.commodity_id, 
                fimd.arrival_date, 
                fimd.Modal_Price, 
                c.commodity_name
            FROM 
                commoditydataanaylsis.fact_indiancommoditymarketdata_2024 fimd
            JOIN 
                commoditydataanaylsis.dim_commoditydetails c ON fimd.commodity_id = c.commodity_id
            WHERE 
                fimd.market_id = %s
                AND fimd.arrival_date = (
                    SELECT MAX(arrival_date)
                    FROM commoditydataanaylsis.fact_indiancommoditymarketdata_2024
                    WHERE market_id = %s
                );

            """, (market_id,market_id,))
            results = cursor.fetchall()

            CommodityDetails_list = []

            for row in results:
                commodity_instance = Commodity()
                commodity_instance.commodity_id = row['commodity_id']
                commodity_instance.commodity_name = row['commodity_name']
                commodity_instance.arrival_date = row['arrival_date']
                commodity_instance.modal_price = row['Modal_Price']
                CommodityDetails_list.append(commodity_instance)
        
            return CommodityDetails_list
        finally:
            cursor.close()
            connection.close()

    @classmethod
    def get_commodity_prices(cls, date_range, market_id, commodity_id):
        connection = DBConnection.database_connection()

        if connection is None:
            raise Exception("Failed to establish database connection.")

        try:
            cursor = connection.cursor(dictionary=True)
            query = """
            SELECT 
                YEAR(Combined.Arrival_Date) AS YearValue,
                MONTH(Combined.Arrival_Date) AS MonthValue,
                DATE_FORMAT(MIN(Combined.Arrival_Date), '%%b') AS MonthName,
                AVG(Combined.Min_Price) AS AvgMinPrice,
                AVG(Combined.Max_Price) AS AvgMaxPrice,
                AVG(Combined.Modal_Price) AS AvgModalPrice
            FROM 
            (
                SELECT Arrival_Date, Min_Price, Max_Price, Modal_Price, Market_ID, Commodity_ID
                FROM fact_indiancommoditymarketdata_2025
                
                UNION ALL
                
                SELECT Arrival_Date, Min_Price, Max_Price, Modal_Price, Market_ID, Commodity_ID
                FROM fact_indiancommoditymarketdata_2024

                UNION ALL
                
                SELECT Arrival_Date, Min_Price, Max_Price, Modal_Price, Market_ID, Commodity_ID
                FROM fact_indiancommoditymarketdata_2023

                UNION ALL
                
                SELECT Arrival_Date, Min_Price, Max_Price, Modal_Price, Market_ID, Commodity_ID
                FROM fact_indiancommoditymarketdata_2022

                UNION ALL
                
                SELECT Arrival_Date, Min_Price, Max_Price, Modal_Price, Market_ID, Commodity_ID
                FROM fact_indiancommoditymarketdata_2021
            ) AS Combined
            WHERE
            (
                (%s = '1M' AND Combined.Arrival_Date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH))
                OR (%s = '3M' AND Combined.Arrival_Date >= DATE_SUB(CURDATE(), INTERVAL 3 MONTH))
                OR (%s = '6M' AND Combined.Arrival_Date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH))
                OR (%s = '1Y' AND Combined.Arrival_Date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH))
                OR (%s = 'All')
            )
            AND Combined.Market_ID = %s
            AND Combined.Commodity_ID = %s
            GROUP BY 
                YEAR(Combined.Arrival_Date),
                MONTH(Combined.Arrival_Date)
            ORDER BY 
                YEAR(Combined.Arrival_Date),
                MONTH(Combined.Arrival_Date)
            LIMIT 0, 500;
            """
            
            cursor.execute(query, (date_range, date_range, date_range, date_range, date_range, market_id, commodity_id))
            results = cursor.fetchall()
            print(f"Results from query: {results}")
            formatted_results = []
            for row in results:
                commodity_instance = CommodityMarketData()
                commodity_instance.year_value = row['YearValue']
                commodity_instance.month_value = row['MonthValue']
                commodity_instance.month_name = row['MonthName']
                commodity_instance.avg_min_price = row['AvgMinPrice']
                commodity_instance.avg_max_price = row['AvgMaxPrice']
                commodity_instance.avg_modal_price = row['AvgModalPrice']
                formatted_results.append(commodity_instance)

            return formatted_results
        finally:
            cursor.close()
            connection.close()

class Forecast_Ops:
    @classmethod
    def get_forecasted_price(cls,commodity_id,market_id):
        connection = DBConnection.database_connection()

        if connection is None:
            raise Exception("Failed to establish database connection.")

        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                WITH FilteredData AS (
                SELECT Distinct
                    fimd.Arrival_Date_Key AS Date_Key,
                    fimd.Modal_Price,
                    fcf.Predicted_Price
                FROM
                    fact_indiancommoditymarketdata_2024 fimd
                INNER JOIN
                    fact_commodityforecast fcf
                    ON fimd.Arrival_Date_Key = fcf.Predicted_Date_Key
                    and fimd.commodity_id = fcf.commodity_id
                    and fimd.market_id = fcf.market_id
                WHERE
                    fimd.commodity_id = %s
                    AND fimd.market_id = %s
            )
            SELECT 
                c.week,
                AVG(f.Modal_Price) AS avg_modal_price,
                AVG(f.Predicted_Price) AS avg_predicted_price,
                (1-(AVG(f.Predicted_Price) / AVG(f.Modal_Price)) )*100 as diff

            FROM 
                FilteredData f
            INNER JOIN
                dim_calendar c
                ON f.Date_Key = c.Date_Key
            GROUP BY 
                c.week
            ORDER BY
                c.week;
    

            """, (commodity_id,market_id,))
            results = cursor.fetchall()

            CommodityForecast_list = []

            for row in results:
                CommodityForecast_instance = CommodityForecast()
                CommodityForecast_instance.week = row['week']
                CommodityForecast_instance.avg_modal_price = row['avg_modal_price']
                CommodityForecast_instance.avg_predicted_price = row['avg_predicted_price']
                CommodityForecast_instance.diff = row['diff']

                CommodityForecast_list.append(CommodityForecast_instance)

            return CommodityForecast_list
        finally:
            cursor.close()
            connection.close()
    
    @classmethod
    def get_top6_forecasted_price(cls,commodity_id,market_id):
        connection = DBConnection.database_connection()

        if connection is None:
            raise Exception("Failed to establish database connection.")

        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                WITH FilteredData AS (
                SELECT Distinct
                    fimd.Arrival_Date_Key AS Date_Key,
                    fimd.Modal_Price,
                    fcf.Predicted_Price
                FROM
                    fact_indiancommoditymarketdata_2024 fimd
                INNER JOIN
                    fact_commodityforecast fcf
                    ON fimd.Arrival_Date_Key = fcf.Predicted_Date_Key
                    and fimd.commodity_id = fcf.commodity_id
                    and fimd.market_id = fcf.market_id
                WHERE
                    fimd.commodity_id = %s
                    AND fimd.market_id = %s
            )
            SELECT 
                c.week,
                AVG(f.Modal_Price) AS avg_modal_price,
                AVG(f.Predicted_Price) AS avg_predicted_price,
                (1-(AVG(f.Predicted_Price) / AVG(f.Modal_Price)) )*100 as diff

            FROM 
                FilteredData f
            INNER JOIN
                dim_calendar c
                ON f.Date_Key = c.Date_Key
            GROUP BY 
                c.week
            ORDER BY
                c.week desc limit 6;
    

            """, (commodity_id,market_id,))
            results = cursor.fetchall()

            CommodityForecast_list = []

            for row in results:
                CommodityForecast_instance = CommodityForecast()
                CommodityForecast_instance.week = row['week']
                CommodityForecast_instance.avg_modal_price = row['avg_modal_price']
                CommodityForecast_instance.avg_predicted_price = row['avg_predicted_price']
                CommodityForecast_instance.diff = row['diff']

                CommodityForecast_list.append(CommodityForecast_instance)

            return CommodityForecast_list
        finally:
            cursor.close()
            connection.close()

class SeasonalDataOps:
    @classmethod
    def get_seasonal_data(cls, market_id, commodity_id):
        connection = DBConnection.database_connection()

        if connection is None:
            raise Exception("Failed to establish database connection.")

        try:
            cursor = connection.cursor(dictionary=True)
            query = """
            SELECT 
                CASE 
                    WHEN MONTH(Arrival_Date) IN (3, 4, 5) THEN 'Spring'
                    WHEN MONTH(Arrival_Date) IN (6, 7, 8) THEN 'Summer'
                    WHEN MONTH(Arrival_Date) IN (9, 10, 11) THEN 'Autumn'
                    WHEN MONTH(Arrival_Date) IN (12, 1, 2) THEN 'Winter'
                END AS Season,
                YEAR(Arrival_Date) AS YearValue,
                AVG(Min_Price) AS AvgMinPrice,
                AVG(Max_Price) AS AvgMaxPrice,
                AVG(Modal_Price) AS AvgModalPrice
            FROM 
                (
                    SELECT Arrival_Date, Min_Price, Max_Price, Modal_Price, Market_ID, Commodity_ID
                    FROM fact_indiancommoditymarketdata_2025

                    UNION ALL

                    SELECT Arrival_Date, Min_Price, Max_Price, Modal_Price, Market_ID, Commodity_ID
                    FROM fact_indiancommoditymarketdata_2024

                    UNION ALL

                    SELECT Arrival_Date, Min_Price, Max_Price, Modal_Price, Market_ID, Commodity_ID
                    FROM fact_indiancommoditymarketdata_2023

                    UNION ALL

                    SELECT Arrival_Date, Min_Price, Max_Price, Modal_Price, Market_ID, Commodity_ID
                    FROM fact_indiancommoditymarketdata_2022

                    UNION ALL

                    SELECT Arrival_Date, Min_Price, Max_Price, Modal_Price, Market_ID, Commodity_ID
                    FROM fact_indiancommoditymarketdata_2021
                ) AS Combined
            WHERE
                Combined.Market_ID = %s
                AND Combined.Commodity_ID = %s
            GROUP BY 
                Season, YearValue
            ORDER BY 
                FIELD(Season, 'Spring', 'Summer', 'Autumn', 'Winter'),
                YearValue
            LIMIT 0, 500;
            """
            
            cursor.execute(query, (market_id, commodity_id))
            results = cursor.fetchall()

            formatted_results = []
            for row in results:
                seasonal_instance = SeasonalData(
                    season=row['Season'],
                    year_value=row['YearValue'],
                    avg_min_price=row['AvgMinPrice'],
                    avg_max_price=row['AvgMaxPrice'],
                    avg_modal_price=row['AvgModalPrice']
                )
                formatted_results.append(seasonal_instance)

            return formatted_results
        finally:
            cursor.close()
            connection.close()
