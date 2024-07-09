from database.DB_connect import DBConnect
from model.retailer import Retailer


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_country():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = []
        query = """SELECT DISTINCT country
                    FROM go_retailers"""

        cursor.execute(query)
        for row in cursor:
            result.append(row['country'])


        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_year():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = []
        query = """select distinct year(date) 
                    from go_daily_sales 
                    where year(date) > 2014 
                    and year(date)<2019"""

        cursor.execute(query)
        for row in cursor:
            result.append(row['year(date)'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_retailers():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = []
        query = """select * from go_retailers"""

        cursor.execute(query)
        for row in cursor:
            result.append(Retailer(row['Retailer_code'], row['Retailer_name'], row['Type'], row['Country']))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getSameProduct( anno, paese, idMap):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = []
        query = """Select d1.Retailer_code as Ret1, d2.Retailer_code as Ret2, count(DISTINCT d1.Product_number) as N
                    From go_retailers r1, go_daily_sales d1, go_retailers r2, go_daily_sales d2
                    Where d1.Retailer_code>d2.Retailer_code 
                    And r1.Retailer_code = d1.Retailer_code
                    And r2.Retailer_code = d2.Retailer_code 
                    And year(d1.date) = %s
                    And year(d2.date) = year(d1.date)
                    And r1.country = %s
                    And r2.country = %s 
                    And d1.Product_number = d2.Product_number 
                    Group by d1.Retailer_code, d2.Retailer_code;"""

        cursor.execute(query, (anno, paese, paese))
        for row in cursor:
            result.append((idMap[row['Ret1']], idMap[row['Ret2']], row['N']))

        cursor.close()
        conn.close()
        return result
