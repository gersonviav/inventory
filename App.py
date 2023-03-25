from itertools import product
import MySQLdb
from flask import Flask,render_template, request, request_started,url_for,redirect,flash
from flask_mysqldb import MySQL

app =Flask(__name__)
#mysql conncetion
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB'] ='clientes_store'
mysql = MySQL(app)
# setting
app.secret_key = 'mysecretkey'
# starting the app
@app.route('/')
def Index () :
    cur =mysql.connection.cursor()
    cur.execute('select * from clientes'),
    data=cur.fetchall()
    
    print(data)
    return render_template('index.html',clientes=data)
@app.route('/add_contact',methods=['POST'])
def add_contact():
    if request.method == 'POST':
            fullname = request.form['fullname']
            monto = request.form['monto']
            estado = request.form['estado']
            cur =mysql.connection.cursor()
            cur.execute('insert into clientes (fullname,monto,estado) VALUES (%s,%s,%s)',
            (fullname,monto,estado))
            mysql.connection.commit()
            flash('Contac added succesfully')
            print(fullname)
            print(monto)
            print(estado)
    return redirect(url_for('Index'))
@app.route('/edit/<id>')
def get_contact(id):
    cur=mysql.connection.cursor()
    cur.execute('select * from clientes where id =%s',(id))
    data = cur.fetchall()
    print(data[0])
    return render_template('edit-client.html',client = data[0])
@app.route('/products')
def get_products():
    cur =mysql.connection.cursor()
    cur.execute('select * from productos'),
    data=cur.fetchall()
    
    print(data)
    #return render_template('index.html',clientes=data)

    return render_template('products.html',products=data)
@app.route('/update/<id>',methods =['POST'])
def  update_contact(id):

    if request.method == 'POST':
            fullname = request.form['fullname']
            monto = request.form['monto']
            estado = request.form['estado']

            cur =mysql.connection.cursor()
            cur.execute("""
            UPDATE clientes
            set fullname=%s,
                monto = %s ,
                estado =%s
            where id=%s
            """,(fullname,monto,estado,id)
            )
            mysql.connection.commit()
            flash('concact updated succesfully')
            return redirect(url_for('Index'))

@app.route('/add_rest/<id>/<monto>',methods =['POST'])
def add_rest(id,monto):
    if request.method == 'POST':
            monto2= request.form['monto']
            monto2=float(monto)+float(monto2)
            monto2=float(monto2)
            monto2 = str(monto2)
            print(monto2)
            cur = mysql.connection.cursor()
            cur.execute("""
            UPDATE  clientes
            set monto = %s
            where id =%s
            """ ,(monto2,id)
            )
            data=cur.fetchall()
            print(data)
            print(id,monto2)
            mysql.connection.commit()
            flash('pay succesfully')
    return redirect(url_for('Index'))

@app.route('/add_deb/<id>/<monto>',methods =['POST'])
def add_deb(id,monto):
    if request.method == 'POST':
            monto2= request.form['monto']
            monto2=float(monto)-float(monto2)
            monto2=float(monto2)
            monto2 = str(monto2)
            print(monto2)
            cur = mysql.connection.cursor()
            cur.execute("""
            UPDATE  clientes
            set monto = %s
            where id =%s
            """ ,(monto2,id)
            )
            data=cur.fetchall()
            print(data)
            print(id,monto2)
            mysql.connection.commit()
            flash('pay succesfully')
    return redirect(url_for('Index'))

@app.route('/delete/<string:id>')
def delete_contact(id):
    cur =mysql.connection.cursor()
    cur.execute('DELETE FROM clientes where id ={0}'.format(id))
    mysql.connection.commit()
    flash('Contac removes succesfully')
    return redirect(url_for('Index'))

if __name__ == "__main__":
    
    app.run(port=3000, debug=True)

