from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'

def create_connection():
    conn = sqlite3.connect('karyawan.db')
    return conn

@app.route('/')
def index():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM karyawan")
    karyawan = cursor.fetchall()
    conn.close()
    return render_template('index.html', karyawan=karyawan)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nik = request.form['nik']
        nama = request.form['nama']
        departemen = request.form['departemen']
        jabatan = request.form['jabatan']
        conn = create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO karyawan (nik, nama, departemen, jabatan) VALUES (?, ?, ?, ?)",
                           (nik, nama, departemen, jabatan))
            conn.commit()
            flash('Data karyawan berhasil ditambahkan!', 'success')
        except sqlite3.IntegrityError:
            flash('Error: NIK sudah ada!', 'danger')
        finally:
            conn.close()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/update/<nik>', methods=['GET', 'POST'])
def update(nik):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM karyawan WHERE nik = ?", (nik,))
    karyawan = cursor.fetchone()

    if request.method == 'POST':
        nama = request.form['nama']
        departemen = request.form['departemen']
        jabatan = request.form['jabatan']
        cursor.execute("""
            UPDATE karyawan 
            SET nama = ?, departemen = ?, jabatan = ? 
            WHERE nik = ?
        """, (nama, departemen, jabatan, nik))
        conn.commit()
        flash('Data karyawan berhasil diperbarui!', 'success')
        return redirect(url_for('index'))
    
    conn.close()
    return render_template('update.html', karyawan=karyawan)

@app.route('/delete/<nik>', methods=['POST'])
def delete(nik):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM karyawan WHERE nik = ?", (nik,))
    conn.commit()
    conn.close()
    flash('Data karyawan berhasil dihapus!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
