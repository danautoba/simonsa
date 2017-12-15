from simonsa import db
from datetime import datetime
from werkzeug.security import generate_password_hash
from uuid import uuid4


class Program(db.Model):
	__tablename__ = 'program'
	id_program = db.Column(db.Integer, primary_key=True)
	id_pok = db.Column(db.VARCHAR(100))
	deskripsi = db.Column(db.Text)
	tabel_pok = db.relationship('Pok', backref = 'program', lazy = 'dynamic')

	def __init__(self, id_program, id_pok, deskripsi):
		self.id_program = id_program
		self.id_pok = id_pok
		self.deskripsi = deskripsi


	def to_json_program(self):
		data_pok = {
						'id_program' : self.id_program,
						'id_pok' : self.id_pok,
						'deskripsi' : self.deskripsi
		}
		return data_pok

	@staticmethod
	def from_json_program(data_pok):
		id_program = data_pok.get('id_program')
		id_pok = data_pok.get('id_pok')
		deskripsi = data_pok.get('deskripsi')
		return Program(id_program = id_program, id_pok = id_pok, deskripsi = deskripsi)	





class Kegiatan(db.Model):
	__tablename__ = 'kegiatan'
	id_kegiatan = db.Column(db.Integer, primary_key=True)
	id_pok = db.Column(db.VARCHAR(100))
	deskripsi = db.Column(db.Text)	
	tabel_pok = db.relationship('Pok', backref = 'kegiatan', lazy = 'dynamic')

class Output(db.Model):
	__tablename__ = 'output'
	id_output = db.Column(db.Integer, primary_key=True)
	id_pok = db.Column(db.VARCHAR(100))
	deskripsi = db.Column(db.Text)	
	tabel_pok = db.relationship('Pok', backref = 'output', lazy = 'dynamic')


class Komponen(db.Model):
	__tablename__ = 'komponen'
	id_komponen = db.Column(db.Integer, primary_key=True)
	id_pok = db.Column(db.VARCHAR(100))
	deskripsi = db.Column(db.Text)	
	tabel_pok = db.relationship('Pok', backref = 'komponen', lazy = 'dynamic')


class Akun(db.Model):
	__tablename__ = 'akun'
	id_akun = db.Column(db.Integer, primary_key=True)
	deskripsi = db.Column(db.Text)	
	tabel_pok = db.relationship('Pok', backref = 'akun', lazy = 'dynamic')


class Detail(db.Model):
	__tablename__ = 'detail'
	id_detail = db.Column(db.Integer, primary_key=True)
	deskripsi = db.Column(db.Text)	
	tabel_pok = db.relationship('Pok', backref = 'detail', lazy = 'dynamic')



class User(db.Model):
	__tablename__ = 'user'
	id_user = db.Column(db.BigInteger, primary_key=True)
	nama = db.Column(db.Text)
	password_hashed = db.Column(db.VARCHAR(100))

	def __init__(self, id_user, nama, password):
		self.id_user = id_user
		self.nama = nama
		self.password_hashed = generate_password_hash(password)



class Log(db.Model):
	__tablename__ = 'log_login'
	id_log = db.Column(db.BigInteger, primary_key=True)
	id_user = db.Column(db.Integer)
	tanggal_login = db.Column(db.DateTime, default=datetime.utcnow)

class Satuan_volume(db.Model):
	__tablename__ = 'satuan_volume'
	id_satuan_volume = db.Column(db.Integer, primary_key=True)
	deskripsi = db.Column(db.Text)	
	tabel_pok = db.relationship('Pok', backref = 'satuan_volume', lazy = 'dynamic')
	tabel_transaksi = db.relationship('Transaksi', backref = 't_satuan_volume', lazy = 'dynamic')

class Terms(db.Model):
	__tablename__ = 'terms'
	id_terms = db.Column(db.Integer, primary_key=True)
	deskripsi = db.Column(db.Text)
	tabel_pok = db.relationship('Pok', backref = 'terms', lazy = 'dynamic')



class Pok(db.Model):
	__tablename__ = 'pok'
	id_tabel_pok = db.Column(db.BigInteger, primary_key=True)
	id_program = db.Column(db.Integer, db.ForeignKey('program.id_program'))
	id_kegiatan = db.Column(db.Integer, db.ForeignKey('kegiatan.id_kegiatan'))
	id_output = db.Column(db.Integer, db.ForeignKey('output.id_output'))
	id_komponen = db.Column(db.Integer, db.ForeignKey('komponen.id_komponen'))
	id_akun = db.Column(db.Integer, db.ForeignKey('akun.id_akun'))
	id_detail = db.Column(db.Integer, db.ForeignKey('detail.id_detail'))
	id_terms = db.Column(db.Integer, db.ForeignKey('terms.id_terms'))
	id_satuan_volume = db.Column(db.Integer, db.ForeignKey('satuan_volume.id_satuan_volume'))
	jumlah_volume = db.Column(db.Integer)
	jumlah_pagu = db.Column(db.Integer)
	no_revisi = db.Column(db.Integer)
	rel_tabel_transaksi = db.relationship('Transaksi', backref = 'pok_transaksi', lazy = 'dynamic')
	rel_tabel_sisa = db.relationship('Sisa_pagu', backref = 'pok_sisa_pagu', lazy = 'dynamic')

	def __init__(self, id_tabel_pok, id_program, id_kegiatan, id_output, id_komponen, id_akun, id_detail, id_terms, id_satuan_volume, jumlah_volume, jumlah_pagu, no_revisi):
		self.id_tabel_pok = id_tabel_pok
		self.id_program = id_program
		self.id_kegiatan = id_kegiatan
		self.id_output = id_output
		self.id_komponen = id_komponen
		self.id_akun = id_akun
		self.id_detail = id_detail
		self.id_terms = id_terms
		self.id_satuan_volume = id_satuan_volume
		self.jumlah_volume = jumlah_volume
		self.jumlah_pagu = jumlah_pagu
		self.no_revisi = no_revisi 






class Transaksi(db.Model):
	__tablename__ = 'transaksi'
	id_transaksi = db.Column(db.BigInteger, primary_key=True)
	id_tabel_pok = db.Column(db.Integer, db.ForeignKey('pok.id_tabel_pok'))
	id_user = db.Column(db.Integer)
	tanggal_transaksi = db.Column(db.DateTime)
	volume = db.Column(db.Integer)
	id_satuan_volume = db.Column(db.Integer, db.ForeignKey('satuan_volume.id_satuan_volume'))
	jumlah_transaksi = db.Column(db.Integer)
	keterangan = db.Column(db.Text)

	def __init__(self, id_transaksi, id_tabel_pok, id_user, tanggal_transaksi, volume, id_satuan_volume, jumlah_transaksi, keterangan):
		self.id_transaksi = id_transaksi
		self.id_tabel_pok = id_tabel_pok
		self.id_user = id_user
		self.tanggal_transaksi = tanggal_transaksi
		self.volume = volume
		self.id_satuan_volume = id_satuan_volume
		self.jumlah_transaksi = jumlah_transaksi
		self.keterangan = keterangan


	def to_json_transaksi(self):
		data_transaksi = {
						'id_transaksi' : self.id_transaksi,
						'id_tabel_pok' : self.id_tabel_pok,
						'id_user' : self.id_user,
						'tanggal_transaksi' : self.tanggal_transaksi,
						'volume' : self.volume,
						'id_satuan_volume' : self.id_satuan_volume,
						'jumlah_transaksi' : self.jumlah_transaksi,
						'keterangan' : self.keterangan
		}
		return data_transaksi

	@staticmethod
	def from_json_transaksi(data_transaksi):
		id_tabel_pok = data_transaksi.get('id_tabel_pok')
		tanggal_transaksi = data_transaksi.get('tanggal_transaksi')
		volume = data_transaksi.get('volume')
		id_satuan_volume = data_transaksi.get('id_satuan_volume')
		jumlah_transaksi = data_transaksi.get('jumlah_transaksi')
		keterangan = data_transaksi.get('keterangan')
		return Transaksi(	id_transaksi = int(str(uuid4().int)[:10]), 
							id_tabel_pok = id_tabel_pok, 
							id_user = 20, 
							tanggal_transaksi = tanggal_transaksi, 
							volume = volume, 
							id_satuan_volume = id_satuan_volume, 
							jumlah_transaksi = jumlah_transaksi, 
							keterangan = keterangan)




class Sisa_pagu(db.Model):
	__tablename__ = 'sisa_pagu'
	id_tabel_pok = db.Column(db.Integer, db.ForeignKey('pok.id_tabel_pok'), primary_key=True)
	sisa_volume = db.Column(db.Integer)
	sisa_pagu = db.Column(db.Integer)
	keterangan = db.Column(db.Text)

	def __init__(self, id_tabel_pok, sisa_volume, sisa_pagu, keterangan):
		self.id_tabel_pok = id_tabel_pok
		self.sisa_volume = sisa_volume
		self.sisa_pagu = sisa_pagu
		self.keterangan = keterangan