from database.DB_connect import DBConnect
from model.categoria import Categoria


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getDateRange():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT distinct (order_date) from orders o order by order_date"""

        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    @staticmethod
    def getCategories():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ select *
                    from categories c """

        cursor.execute(query)

        for row in cursor:
            results.append(Categoria(**row))

        cursor.close()
        conn.close()
        return results