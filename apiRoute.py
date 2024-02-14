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
    

    @application.route('/restaurant/', methods=['GET'])
    @cross_origin('*')
    def getEntity():
        fn_dmn_id = request.args.get('fn_dmn_id')
        sql_query = """SELECT name from restaurant"""
        output = apiService.getData(sql_query)
        outArray=[]
        try:
           print(output)    
        except Exception as exc:
            print(exc)
        return jsonify(output)
    

apiService = Apiservice ()


if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 8443), application)
    http_server.start()
    try:
       logger.info("LDAP Service is up and running")
       http_server.serve_forever()

    except Exception as exc:
       logger.exception(exc)



 
