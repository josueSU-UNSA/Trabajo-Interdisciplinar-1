from re import M
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL,MySQLdb

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'holamundo'
app.config['MYSQL_DB'] = 'flaskcontacts'
mysql = MySQL(app)

app.secret_key='mysecretkey'

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/ingreso',methods=["GET","POST"])
def ingreso():
    if request.method == 'POST':
        cui = request.form['cui']
        password = request.form['password'].encode('utf-8')
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM user WHERE cui=%s",[cui])
        user = curl.fetchone()
        curl.close()
        if not user:
            return "Error CUI not found"
        else:
            if password == user["password"].encode('utf-8'):
                session['cui'] = user['cui']
                return  redirect(url_for('semestre'))
            else:
                return "Error password and CUI not match"

@app.route('/semestre',methods = ['POST','GET'])#nos enviara algo cada vez que entremos a nuestra pagina principal para evitar el not Found
def semestre():
    return render_template('semes.html')

#@app.route('/logout', methods=["GET", "POST"])
#def logout():
#    session.clear()
#    return render_template("login.html")

#auxiliar
@app.route('/Form1/<string:d>',methods = ['POST','GET'])#nos enviara algo cada vez que entremos a nuestra pagina principal para evitar el not Found
def Form1(d):
    #print(d)
    cur=mysql.connection.cursor()
    cur.execute('TRUNCATE TABLE horarios')
    mysql.connection.commit()
    cur.execute('INSERT INTO horarios SELECT * FROM horarios{}'.format(d))#hacemos la consutla sql para traer todos los datos
    mysql.connection.commit()#recordar que esto se ejecuta cada vez que aparece la parte incial
    return redirect(url_for('Form'))

@app.route('/Form',methods = ['GET'])#nos enviara algo cada vez que entremos a nuestra pagina principal para evitar el not Found
def Form():
    #haremos esta consulta para enviar los datos en el tbody del html ya que esta funcion es la que redirecciona al index
    cur=mysql.connection.cursor()#hacemos la consutla sql para traer todos los datos
    cur.execute("SELECT * FROM horarios")
    data=cur.fetchall()#con esto se ejecuta la consulta almacenado en una variable data
    cur.close()
    #recordar que esto se ejecuta cada vez que aparece la parte incial
    return render_template('horario.html',horarios=data)#enviara esta imagen, renderizara el formulario
    #el horarios=data es para poder mandar al html las tuplas creadas
    
@app.route('/add_course',methods=['POST'])
def add_course():# empezaremos a guardar datos
    if request.method=='POST':
        curso=request.form['curso']#guardamos en una variable lo recibido desde el form
        dia=request.form['dia']#recibimos cada dato guardandolos en una variable
        hora_inicio=request.form['hora_inicio']
        hora_final=request.form['hora_final']
        profesor=request.form['profesor']
        grupo=request.form['grupo']
        cur=mysql.connection.cursor()#esta parte para saber donde esta el cursor de la conexion mysql almacenado en una variable
        #el cur nos permitira hacer ejecutar las consultas de mysql
        cur.execute('INSERT INTO horarios(curso,dia,hora_inicio,hora_final,profesor,grupo) VALUES(%s,%s,%s,%s,%s,%s)',(curso,dia,hora_inicio,hora_final,profesor,grupo))
        mysql.connection.commit()#aqui ejecutamos la consulta
        flash("Curso Agregado")
        return redirect(url_for('Form'))#nos redirecciona otra vez al html incial esto despues de hacer la consulta
    
@app.route('/delete/<string:id>', methods = ['POST','GET'])#el string id porque esa es la condicion que pusimos para poder hacer el delete en una fila
def delete_contact(id):
    #pasaremos el id por una consulta sql para eliminar este id
    cur=mysql.connection.cursor()
    cur.execute('DELETE FROM horarios WHERE id={}'.format(id))#el format nos sirve para poder remplazar en la instruccion sql el id
    mysql.connection.commit()#se ejecuto la consulta
    flash('Curso eliminado del horario')  
    return redirect(url_for('Form'))

@app.route('/comprobacion', methods = ['POST','GET'])
def comprobacion():
    cur=mysql.connection.cursor()
    #cur.execute('TRUNCATE TABLE grafico')
    #mysql.connection.commit()
    cur.execute('SELECT * FROM horarios WHERE hora_inicio=%s',['7:00'])
    data=cur.fetchall()
    d1=data
    print(d1)
    cur.execute('SELECT * FROM horarios WHERE hora_inicio=%s',['7:50'])
    data=cur.fetchall()
    d2=data
    cur.execute('SELECT * FROM horarios WHERE hora_inicio=%s',['8:50'])
    data=cur.fetchall()
    d3=data
    cur.execute('SELECT * FROM horarios WHERE hora_inicio=%s',['9:40'])
    data=cur.fetchall()
    d4=data
    cur.execute('SELECT * FROM horarios WHERE hora_inicio=%s',['10:40'])
    data=cur.fetchall()
    d5=data
    cur.execute('SELECT * FROM horarios WHERE hora_inicio=%s',['11:30'])
    data=cur.fetchall()
    d6=data
    cur.execute('SELECT * FROM horarios WHERE hora_inicio=%s',['12:20'])
    data=cur.fetchall()
    d7=data
    cur.execute('SELECT * FROM horarios WHERE hora_inicio=%s',['13:10'])
    data=cur.fetchall()
    d8=data
    cur.execute('SELECT * FROM horarios WHERE hora_inicio=%s',['14:50'])
    data=cur.fetchall()
    d9=data
    cur.execute('SELECT * FROM horarios WHERE hora_inicio=%s',['15:50'])
    data=cur.fetchall()
    d10=data
    cur.execute('SELECT * FROM horarios WHERE hora_inicio=%s',['16:40'])
    data=cur.fetchall()
    d11=data
    cur.execute('SELECT * FROM horarios WHERE hora_inicio=%s',['17:40'])
    data=cur.fetchall()
    d12=data
    cur.execute('SELECT * FROM horarios WHERE hora_inicio=%s',['18:30'])
    data=cur.fetchall()
    d13=data
    cur.execute('SELECT * FROM horarios WHERE hora_inicio=%s',['19:30'])
    data=cur.fetchall()
    d14=data
    cur.close()
    tup = d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11,d12,d13,d14
    dia = 'Lunes','Martes','Miercoles','Jueves','Viernes'
    hor = '07:00-07:50','07:50-08:40','08:50-09:40','09:40-10:30','10:40-11:30','11:30-12:20','12:20-13:10','13:10-14:00','14:50-15:40','15:50-16:40','16:40-17:30','17:40-18:30','18:30-19:20','19:30-20:20'
    return render_template('comprobacion.html',t=tup, h=hor, diad=dia)

if __name__=='__main__':#si el archivo que se esta ejecutando es el main es decir el app.py entonces arranca el servidor
    app.run(port=3000,debug=True)#corre el servidor