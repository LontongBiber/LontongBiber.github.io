import os
import string
import textwrap
from flask import Flask , render_template, redirect, flash, request,session ,url_for
from werkzeug import secure_filename
import sqlite3 as sql
from peewee import *
from flask_ckeditor import CKEditor, CKEditorField




UPLOAD_FOLDER = 'static/uploads/'

app = Flask(__name__)
app.secret_key = '1234567'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['CKEDITOR_PKG_TYPE'] = 'basic'
ckeditor = CKEditor(app)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


DATABASE = "dbtamk.db"
database = SqliteDatabase(DATABASE)



#membuat table disabilitas
class BaseModel(Model):
	class Meta:
		database = database

class Disabilitas(BaseModel):
	id = IntegerField(unique=True)
	nama = TextField()
	ttl = TextField()
	penyandang = TextField()
	jenis_kelamin = TextField()
	usia = TextField()
	alamat = TextField()
	status = TextField()


class create_tables():
	with database:
		database.create_tables([Disabilitas])


#membuat tabel alat 1
class Alat1(BaseModel):
	id = IntegerField(unique=True)
	nama_alat = TextField()
	jumlah = TextField()

class create_tables():
	with database:
		database.create_tables([Alat1])


#membuat tabel donatur
class Donatur(BaseModel):
	id = IntegerField(unique=True)
	nama = TextField()
	alamat = TextField()
	jenis_bantuan = TextField()

class create_tables():
	with database:
		database.create_tables([Donatur])

#membuat tabel Berita
class Berita(BaseModel):
	id = IntegerField(unique=True)
	tanggal = TextField()
	judul = TextField()
	isi = TextField()
	author = TextField()
	

class create_tables():
	with database:
		database.create_tables([Berita])

	



# @app.route('/saves')
# def saves():
# 	entry = Disabilitas.create(
# 		id = '0001',
# 		nama = 'lurah',
# 		ttl = 'sidaorjo 12 agustus 1990',
# 		penyandang = 'tunawicara',
# 		jenis_kelamin = 'L',
# 		usia = '31',
# 		alamat = 'sidaorjo',
# 		status = 'menikah',
# 	)
# 	return  "saved"

##################halaman user########3

@app.route('/')
def index():
	return  render_template('user.html')

@app.route('/halamanberita')
def halamanberita():
	row = Berita.select(Berita.id,Berita.tanggal,Berita.judul,
	Berita.isi,Berita.author)
	return  render_template('halamanberita.html', menu='master',submenu='berita', row = row)

@app.route('/tampilberita/<id>')
def tampilberita(id):
	row = Berita.select(Berita.id,Berita.tanggal,Berita.judul,
	Berita.isi,Berita.author).where(Berita.id==id).first()
	return  render_template('tampilberita.html', menu='master',submenu='berita', data = row)

@app.route('/halamanperalatan')
def halamanperalatan():
	tongkat = Alat1.select(Alat1.jumlah).where(Alat1.nama_alat=="TONGKAT").first()
	kursi_roda = Alat1.select(Alat1.jumlah).where(Alat1.nama_alat=="KURSI RODA").first()
	kaki_pasangan = Alat1.select(Alat1.jumlah).where(Alat1.nama_alat=="KAKI PASANGAN").first()
	kacamata = Alat1.select(Alat1.jumlah).where(Alat1.nama_alat=="KACA MATA").first()
	alat_pendengaran = Alat1.select(Alat1.jumlah).where(Alat1.nama_alat=="ALAT PENDENGARAN").first()
	alquran = Alat1.select(Alat1.jumlah).where(Alat1.nama_alat=="ALQURAN").first()
	return render_template('halamanperalatan.html',
		tongkat=tongkat, 
		kursi_roda=kursi_roda, 
		kaki_pasangan=kaki_pasangan,
		kacamata=kacamata, 
		alat_pendengaran=alat_pendengaran, 
		alquran=alquran,
	) 
	
@app.route ('/kontak')
def kontak():
	return render_template('kontak.html')

################batas hal user#############

@app.route('/masterdisabilitas')
def masterdisabilitas():
	row = Disabilitas.select(Disabilitas.id,Disabilitas.nama,Disabilitas.ttl,
	Disabilitas.penyandang,Disabilitas.jenis_kelamin,Disabilitas.usia,Disabilitas.alamat,Disabilitas.status)
	return  render_template('masterdisabilitas.html', menu='master',submenu='disabilitas', row = row )

# memanggil form tambah
@app.route('/add_disabilitas')
def add_disabilitas():
	return render_template('tambahdisabilitas.html')
# menyimpan hasil input form tambah
@app.route('/save-disabilitas',methods=['POST'])
def save_disabilitas():
	entry = Disabilitas.create(
		nama = request.form['nama_lengkap'],
		ttl = request.form['ttl'],
		penyandang = request.form['penyandang'],
		jenis_kelamin = request.form['jk'],
		usia = request.form['usia'],
		alamat = request.form['alamat'],
		status = request.form['status'],
	)
	return redirect("/masterdisabilitas")

# memanggil form edit
@app.route('/edit_disabilitas/<id>')
def edit_disabilitas(id):
	row = Disabilitas.select(Disabilitas.id,Disabilitas.nama,Disabilitas.ttl,
	Disabilitas.penyandang,Disabilitas.jenis_kelamin,Disabilitas.usia,
	Disabilitas.alamat,Disabilitas.status).where(Disabilitas.id==id).first()
	return render_template('editdisabilitas.html', row=row, id=id)
# menyimpan hasil input form edit
@app.route('/saveupdate-disabilitas/<id>',methods=['POST'])
def saveupdate_disabilitas(id):
	entry = Disabilitas.update(
		nama = request.form['nama_lengkap'],
		ttl = request.form['ttl'],
		penyandang = request.form['penyandang'],
		jenis_kelamin = request.form['jk'],
		usia = request.form['usia'],
		alamat = request.form['alamat'],
		status = request.form['status'],
	).where(Disabilitas.id==id)
	entry.execute()
	return redirect("/masterdisabilitas")

# hapus data disabilitas
@app.route('/delete_disabilitas/<id>')
def delete_disabilitas(id):
	query = Disabilitas.delete().where(Disabilitas.id==id)
	query.execute()
	return redirect("/masterdisabilitas")
################################selesai disabilitas###############################################################

@app.route('/masterdonatur')
def masterdonatur():
	row = Donatur.select(Donatur.id,Donatur.nama,Donatur.alamat,
	Donatur.jenis_bantuan)
	return  render_template('masterdonatur.html', menu='master',submenu='donatur', row = row )


# memanggil form tambah
@app.route('/add_donatur')
def add_donatur():
	return render_template('tambahdonatur.html')

# menyimpan hasil input form tambah
@app.route('/save-donatur',methods=['POST'])
def save_donatur():
	entry = Donatur.create(
		nama = request.form['nama'],
		alamat = request.form['alamat'],
		jenis_bantuan = request.form['jenis'],
		
	)
	return redirect("/masterdonatur")

# memanggil form edit
@app.route('/edit_donatur/<id>')
def edit_donatur(id):
	row = Donatur.select(Donatur.id,Donatur.nama,Donatur.alamat,
	Donatur.jenis_bantuan).where(Donatur.id==id).first()
	return render_template('editdonatur.html', row=row, id=id)

# menyimpan hasil input form edit
@app.route('/saveupdate-donatur/<id>',methods=['POST'])
def saveupdate_donatur(id):
	entry = Donatur.update(
		nama = request.form['nama'],
		alamat = request.form['alamat'],
		jenis_bantuan = request.form['jenis'],
		
	).where(Donatur.id==id)
	entry.execute()
	return redirect("/masterdonatur")

# hapus data donatur
@app.route('/delete_donatur/<id>')
def delete_donatur(id):
	query = Donatur.delete().where(Donatur.id==id)
	query.execute()
	return redirect("/masterdonatur")

	###################################selesai donatur#########################################

@app.route('/masteralat')
def masteralat():
	row = Alat1.select(Alat1.id,Alat1.nama_alat,Alat1.jumlah)
	return  render_template('masteralat.html', menu='master',submenu='alat', row = row )


# memanggil form tambah
@app.route('/add_alat')
def add_alat():
	return render_template('tambahalat.html')

# menyimpan hasil input form tambah
@app.route('/save-alat',methods=['POST'])
def save_alat():
	entry = Alat1.create(
		nama_alat = request.form['nama'],
		jumlah = request.form['jumlah'],
		
	)
	return redirect("/masteralat")

# memanggil form edit
@app.route('/edit_alat/<id>')
def edit_alat(id):
	row = Alat1.select(Alat1.id,Alat1.nama_alat,Alat1.jumlah).where(Alat1.id==id).first()
	return render_template('edit_alat.html', row=row, id=id)

# menyimpan hasil input form edit
@app.route('/saveupdate-alat/<id>',methods=['POST'])
def saveupdate_alat(id):
	entry = Alat1.update(
		nama_alat = request.form['nama'],
		jumlah = request.form['jumlah'],
		
	).where(Alat1.id==id)
	entry.execute()
	return redirect("/masteralat")

# hapus data donatur
@app.route('/delete_alat/<id>')
def delete_alat(id):
	query =Alat1.delete().where(Alat1.id==id)
	query.execute()
	return redirect("/masteralat")

###########################selesai berita###############################

@app.route('/masterberita')
def masterberita():
	row = Berita.select(Berita.id,Berita.tanggal,Berita.judul,
	Berita.isi,Berita.author)
	return  render_template('masterberita.html', menu='master',submenu='berita', row = row )


# memanggil form tambah
@app.route('/add_berita')
def add_berita():
	return render_template('tambahberita.html')

# menyimpan hasil input form tambah
@app.route('/save-berita',methods=['POST'])
def save_berita():
	entry = Berita.create(
		tanggal = request.form['tanggal'],
		judul = request.form['judul'],
		isi= request.form.get('isi'),
		author= request.form['author'],
	)
	return redirect("/masterberita")

# memanggil form edit
@app.route('/edit_berita/<id>')
def edit_berita(id):
	row = Berita.select(Berita.id,Berita.tanggal,Berita.judul,
	Berita.isi,Berita.author).where(Berita.id==id).first()
	return render_template('editberita.html', row=row, id=id)

# menyimpan hasil input form edit
@app.route('/saveupdate-berita/<id>',methods=['POST'])
def saveupdate_berita(id):
	entry = Berita.update(
		tanggal = request.form['tanggal'],
		judul = request.form['judul'],
		isi= request.form.get('isi'),
		author = request.form['author'],	
		
	).where(Berita.id==id)
	entry.execute()
	return redirect("/masterberita")

# hapus data Berita
@app.route('/delete_berita/<id>')
def delete_berita(id):
	query = Berita.delete().where(Berita.id==id)
	query.execute()
	return redirect("/masterberita")

@app.route('/tampil-berita/<id>')
def tampil_berita(id):
	row = Berita.select(Berita.id,Berita.tanggal,Berita.judul,
	Berita.isi,Berita.author).where(Berita.id==id).first()
	return render_template('halamanberita.html', row=row, id=id)

###########gambar###########
#upload gambar
@app.route('/upload_gambar')
def upload_gambar():
	return render_template('tambahberita.html')

@app.route('/upload_gambar', methods=['POST'])
def upload_image():
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		#print('upload_image filename: ' + filename)
		flash('Image successfully uploaded and displayed below')
		return render_template('upload.html', filename=filename)
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

	
######### LOGIN ####################

@app.route('/admin')
def admin_login():
	if 'admin_id' in session:
		session_id = session.get('admin_id')
		return  render_template('index.html')
	else:
		session_id = ''
		return render_template('login.html')

@app.route('/admin_login_proses',methods=['POST'])
def admin_login_proses():
	nama = request.form['username']
	row = Disabilitas.select(Disabilitas.id).where(Disabilitas.nama==nama).first()
	session['admin_id'] = row.id
	return redirect('/admin')

###### LOGOUT ######
@app.route('/logout')
def logout():
	if 'admin_id' in session:
		session.pop('admin_id',None)
	return redirect('/admin')


if __name__ == "__main__":
	create_tables()
	app.run(
		host="0.0.0.0",
		debug=True
	)
	