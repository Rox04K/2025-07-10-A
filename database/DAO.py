from database.DB_connect import DBConnect
from model.categoria import Categoria
from model.prodotto import Prodotto


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

    @staticmethod
    def getNodi(categoria):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ select *
                    from products p 
                    where category_id = %s """

        cursor.execute(query, (categoria,))

        for row in cursor:
            results.append(Prodotto(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getArchi(categoria, start, end, mappa):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ with nodi as (
                    select product_id
                    from products p 
                    where category_id = %s),
                    possibili as(
                    select product_id, count(*) as totVendite
                    from order_items oi, orders o
                    where o.order_id = oi.order_id
                    and product_id in (select * from nodi)
                    and order_date between %s and %s
                    group by product_id)
                    select p1.product_id as n1, p2.product_id as n2, (p1.totVendite + p2.totVendite) as peso 
                    from possibili p1, possibili p2
                    where p1.totVendite >= p2.totVendite 
                    and p1.product_id <> p2.product_id"""

        cursor.execute(query, (categoria, start, end))

        for row in cursor:
            results.append((mappa[row['n1']], mappa[row['n2']], row['peso']))

        cursor.close()
        conn.close()
        return results