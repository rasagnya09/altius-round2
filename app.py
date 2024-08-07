import base64
import io
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flaskext.mysql import MySQL

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change to a strong, secret key
#mysql database configurations
mysql = MySQL(app)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Nikki@3526'
app.config['MYSQL_DATABASE_DB'] = 'stu'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'

mysql.init_app(app)
#route to home page
@app.route('/')
def index():
    return redirect(url_for('students'))
#retrieving data
@app.route('/students')
def students():
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()
    return render_template('students.html', students=data)
#inserting data
@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        cursor = mysql.get_db().cursor()
        cursor.execute("INSERT INTO students (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
        mysql.get_db().commit()
        flash('Student added successfully!', 'success')
        return redirect(url_for('students'))
    return render_template('add_student.html')
#updating data
@app.route('/edit_student/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    cursor = mysql.get_db().cursor()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        cursor.execute("UPDATE students SET name = %s, email = %s, phone = %s WHERE id = %s", (name, email, phone, id))
        mysql.get_db().commit()
        flash('Student updated successfully!', 'success')
        return redirect(url_for('students'))
    
    cursor.execute("SELECT * FROM students WHERE id = %s", (id,))
    student = cursor.fetchone()
    return render_template('edit_student.html', student=student)
#deleting data
@app.route('/delete_student/<int:id>', methods=['POST'])
def delete_student(id):
    cursor = mysql.get_db().cursor()
    cursor.execute("DELETE FROM students WHERE id = %s", (id,))
    mysql.get_db().commit()
    return redirect(url_for('students'))

if __name__ == '__main__':
    app.run(debug=True)
