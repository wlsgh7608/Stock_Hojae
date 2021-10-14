from databases import Databases

class CRUD(Databases):
    def insertDB(self,schema,table,column,data):
        sql = " INSERT INTO {schema}.{table}({column}) VALUES {data} ;".format(schema=schema,table=table,column=column,data=data)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e :
            print(" insert DB err ",e) 
            # self.cursor.rollback()
    
    def readDB(self,schema,table,column):
        sql = " SELECT {column} from {schema}.{table}".format(column=column,schema=schema,table=table)
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except Exception as e :
            result = (" read DB err",e)
        
        return result

    def updateDB(self,schema,table,column,value,condition):
        sql = " UPDATE {schema}.{table} SET {column}='{value}' WHERE {column}='{condition}' ".format(schema=schema
        , table=table , column=column ,value=value,condition=condition )
        try :
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e :
            
            print(" update DB err",e)

    def deleteDB(self,schema,table,condition):
        sql = " DELETE FROM {schema}.{table} WHERE {condition} ; ".format(schema=schema,table=table, condition=condition)
        try :
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            print( "delete DB err", e)

    