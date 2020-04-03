import mysql.connector

class DBHelper:
    def __init__(self,dbname,pwd=''):
        self.conexion = mysql.connector.connect(user='root',
                                                password=pwd,
                                                host='localhost',
                                                db=dbname)
        self.cursor = self.conexion.cursor(buffered=True)
    def end(self):
        self.conexion.close()
#         self.cursor.close() # The code works if i remove this line;
    def get_user_ongoing_orders(self,userid):
        sql = 'SELECT * FROM `order` WHERE `userid` = "{}" and `orderStatus` != "delivered"'.format(userid)
        self.cursor.execute(sql)
        columns = self.cursor.column_names
        result = [{columns[i]:v for i, v in enumerate(element)} for element in self.cursor.fetchall()]
        
        return result

    def get_order_items(self,orderId):
        sql = 'SELECT * FROM `orderdetail` WHERE `orderId` = "{}"'.format(orderId)
        self.cursor.execute(sql)
        columns = self.cursor.column_names
        result = [{columns[i]:v for i, v in enumerate(element)} for element in self.cursor.fetchall()]
        
        return result

    



