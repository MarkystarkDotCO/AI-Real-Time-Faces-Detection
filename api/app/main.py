from flask import Flask, jsonify
import pyodbc 
from flask import request
app = Flask(__name__)

#send data to DATABASE
@app.route('/add')
def index():
    server = 'aikmitl.database.windows.net'
    database = 'AddressAndPopulation'
    username = 'aikmitl'
    password = 'vajajava+25%'   
    driver= '{ODBC Driver 17 for SQL Server}'

    #Request ID
    population = request.args['population']
    city = request.args['city']
    state = request.args['state']
    postcode = request.args['postcode']
    country = request.args['country']
    time = request.args['time']

    #SQL for write data
    with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            cursor.execute('INSERT INTO AddressAndPopulation ( Population, city, state, PostalCode, Country, TimeStamp)'+'VALUES'+'('+population+','+"'"+city+"'"+','+"'"+state+"'"+','+postcode+','+"'"+country+"'"+','+"'"+time+"'"')')
            conn.commit()
    return "Success"

#View DATA from DATABASE
@app.route('/')
def view():
    #LOGIN to AZURE SQL SERVER
    server = 'aikmitl.database.windows.net'
    database = 'AddressAndPopulation'
    username = 'aikmitl'
    password = 'vajajava+25%'   
    driver= '{ODBC Driver 17 for SQL Server}'
    with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:

            #SQL for read as json
            cursor.execute("SELECT * FROM AddressAndPopulation;")
            rows = cursor.fetchall()
            info={}
            i = 0
            for row in rows:
                info[i] ={
                "Population":str(row[0]),
                "city":str(row[1]),
                "state":str(row[2]),
                "postcode":str(row[3]),
                "country":str(row[4]),
                "date-time":str(row[5]),
                }
                i = i+1
                #print(info)
            return jsonify(info)





if __name__ == '__main__':
    #app.run(debug=True,host="0.0.0.0", port=80)
    app.run(debug=True)

