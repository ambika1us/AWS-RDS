import flask
from flask import request, jsonify
from flask_cors import CORS, cross_origin
from flask import Response
from sqlalchemy.orm.util import identity_key
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import json
from gevent.pywsgi import WSGIServer
import logging

logger = logging.getLogger(__name__)

application = flask.Flask(__name__)
application.config["DEBUG"] = True
CORS(application,resources={r"/*": {"origins": "*"}})
application.config['CORS_HEADERS'] = 'Content-Type'



class Apiservice():
    
    def __init__(self):
    
      print('Inside __init__')
      self.conn = psycopg2.connect(user="postgres",password="admin987",host="database-1.ciuhxly1igor.ap-south-1.rds.amazonaws.com",port=5432,dbname="postgres")
      
      
    def getConnection (self):
       print('Inside getConnection')
       try:
          cur = self.conn.cursor()
          cur.execute('SELECT 1')
          cur.close()

       except Exception as exc:
          logger.error(exc)
          self.conn = psycopg2.connect(user="postgres",password="admin987",host="database-1.ciuhxly1igor.ap-south-1.rds.amazonaws.com",port=5432,dbname="postgres")
       return self.conn
    
    
    def getData(self,query):
        sql_query = query
        conn = apiService.getConnection()
        cur = conn.cursor()
        cur.execute(sql_query)
        context_records = cur.fetchall()
        return context_records
    
    def postData(self,query,value):
        sql_query = query
        conn = apiService.getConnection ()
        cur = conn.cursor()
        cur.execute(sql_query,value)
        conn.commit()
        return "Data Added"
    
   
    @application.route('/health', methods=['GET'])
    @cross_origin('*')
    def hello():
        return "hello from API"
    

    @application.route('/entity/', methods=['GET'])
    @cross_origin('*')
    def getEntity():
        fn_dmn_id = request.args.get('fn_dmn_id')
        sql_query = """SELECT name from testdb"""
        output = apiService.getData(sql_query)
        outArray=[]
        try:
            length = len(output)
            for i in range(length):
                entity={}
                entity["ent_id"]= output[i][0]
                entity["ent_nm"]= output[i][1]
                entity["ent_val_tx"]= output[i][2]
                entity["creat_user_id"]= output[i][3]
                entity["func_dmn_nm"]= output[i][4]
                entity["func_dmn_id"]= output[i][5]
                entity["creat_ts"]= output[i][6]
                outArray.append(entity)     
        except Exception as exc:
            print(exc)
        return jsonify(outArray)
    

   
    @application.route('/postintent/', methods=['POST'])
    @cross_origin('*')
    def postIntent():

        body = request.json
        if(len(body)>0):

            for x in range(len(body)):
                intnt_nm= body[x]['intnt_nm']
                func_dmn_id=body[x]['func_dmn_id']
                act_in= True
                creat_user_id= body[x]['creat_user_id']
                creat_ts= str(datetime.now())
                check_select = "Select intnt_nm from intnt_train where intnt_nm=%s and func_dmn_id=%s"
                checkval=(intnt_nm,func_dmn_id,)
                checkdup = apiService.checkPresence(check_select,checkval)
                length = len(checkdup)
                if(length != 0 ):

                    out = "Intent Already exist"
                else:
                    sql_ins="""INSERT INTO intnt_train(intnt_nm,func_dmn_id,act_in,creat_user_id,creat_ts) VALUES (%s,%s,%s,%s,%s)"""
                    values=(intnt_nm,func_dmn_id,act_in,creat_user_id,creat_ts)
                    out = apiService.postData(sql_ins,values)  
        return out

    
    
    @application.route('/updateintent/', methods=['PUT'])
    @cross_origin('*')
    def updateIntent():
        body = request.json
        if(len(body)>0):
            for x in range(len(body)):
                intnt_nm= body[x]['intnt_nm']
                lst_updt_user_id= body[x]['lst_updt_user_id']
                lst_updt_ts= str(datetime.now())
                intnt_id= body[x]['intnt_id']
                sql_upt="""Update intnt_train set intnt_nm = %s, lst_updt_user_id=%s,lst_updt_ts=%s  where intnt_id = %s"""
                values=(intnt_nm,lst_updt_user_id, lst_updt_ts, intnt_id)
                out = apiService.postData(sql_upt,values)
            return out


apiService = Apiservice ()


if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 8443), application, keyfile='/opt/epaas/certs/dkey', certfile='/opt/epaas/certs/ca-chain')
    http_server.start()
    try:
       logger.info("LDAP Service is up and running")
       http_server.serve_forever()

    except Exception as exc:
       logger.exception(exc)



 
