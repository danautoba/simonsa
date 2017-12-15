from flask import Flask, render_template, request, url_for, redirect, jsonify 
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
from uuid import uuid4


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:heliumvoldo@localhost/simonsa'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)

from models import * 

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/inputuser')
def inputuser():
	return render_template('page_inputuser.html')


@app.route('/proses_inputuser', methods=['POST'])
def proses_inputuser():
	id_user = int(str(uuid4().int)[:10])
	nama = request.form['nama_user']
	password = request.form['password_user']
	user = User(id_user, nama, password)
	db.session.add(user)
	db.session.commit()
	return redirect(url_for('inputuser'))



@app.route('/pok')
def pok():
	datas = Pok.query.all()
	return render_template('page_pok.html', list_data=datas)


@app.route('/api/pok')
def api_pok():
	datas = Pok.query.all()
	x = {}
	for i in datas:
		x[i.id_tabel_pok] = [i.program.id_pok, i.kegiatan.id_pok, i.output.id_pok, i.komponen.id_pok, i.id_akun, i.detail.deskripsi, i.terms.deskripsi, i.jumlah_volume, i.satuan_volume.deskripsi,  i.jumlah_pagu]
	return jsonify(x)


@app.route('/transaksi')
def transaksi():
	list_komponen = Komponen.query.all()
	return render_template('page_transaksi.html', komponen_list = list_komponen)


@app.route('/prosestransaksi', methods=['POST'])
def prosestransaksi():
	komponen = request.form['pilih_komponen']
	query_komponen = Komponen.query.filter_by(deskripsi = komponen).first()
	query_id_pok = Pok.query.filter_by(id_komponen = query_komponen.id_komponen).order_by("id_akun").all()
	return render_template('page_prosestransaksi.html', query_id_pok = query_id_pok)




@app.route('/test', methods = ['POST'])
def test():
	all_row = request.form.getlist("simpan")
	for row in all_row:
		inp_pemakaian = "input_pemakaian"+str(row)
		inp_volume = "input_volume"+str(row)
		inp_date = "input_date"+str(row)
		inp_keterangan = "input_keterangan"+str(row)
		req_pemakaian = request.form[inp_pemakaian]
		req_volume = request.form[inp_volume]
		req_date = request.form[inp_date]
		req_keterangan = request.form[inp_keterangan]
		satuan_vol = Pok.query.filter_by(id_tabel_pok = row).first()
		to_simpan = Transaksi(	int(str(uuid4().int)[:10]),
								int(row),
								20,
								req_date,
								int(req_volume),
								int(satuan_vol.id_satuan_volume),
								int(req_pemakaian),
								req_keterangan)
		db.session.add(to_simpan)
		db.session.commit()
	return "Sukses"



@app.route('/inputdata')
def inputdata():
	program_list=Program.query.all()
	kegiatan_list = Kegiatan.query.all()
	output_list = Output.query.all()
	komponen_list = Komponen.query.all()
	akun_list = Akun.query.all()
	detail_list = Detail.query.order_by("deskripsi").all()
	posisi_list = Terms.query.all()
	satuan_volume_list = Satuan_volume.query.all()
	return render_template('page_inputdata.html', 
							list_program = program_list,
							list_kegiatan = kegiatan_list,
							list_output = output_list,
							list_komponen = komponen_list,
							list_akun = akun_list,
							list_detail = detail_list,
							list_posisi = posisi_list,
							list_satuan_volume = satuan_volume_list	
							)


@app.route('/prosesdata', methods=['GET', 'POST'])
def prosesdata():
	revisi = 4
	program = request.form['program']
	kegiatan = request.form['kegiatan']
	output = request.form['output']
	komponen = request.form['komponen']
	akun = request.form['akun']
	detail = request.form['detail']
	terms = request.form['posisi']
	satuan_volume = request.form['satuan_volume']
	jumlah_volume = request.form['jumlah_volume']
	jumlah_pagu = request.form['jumlah_pagu']

	query_program = Program.query.filter_by(deskripsi=program).first()
	query_kegiatan = Kegiatan.query.filter_by(deskripsi=kegiatan).first()
	query_output = Output.query.filter_by(deskripsi=output).first()
	query_komponen = Komponen.query.filter_by(deskripsi=komponen).first()
	query_akun = Akun.query.filter_by(deskripsi=akun).first()
	query_detail = Detail.query.filter_by(deskripsi=detail).first()
	query_terms = Terms.query.filter_by(deskripsi=terms).first()
	query_satuan_volume = Satuan_volume.query.filter_by(deskripsi=satuan_volume).first()
	

	add_db_pok = Pok(	int(str(uuid4().int)[:15]),
						query_program.id_program, 
						query_kegiatan.id_kegiatan,
						query_output.id_output,
						query_komponen.id_komponen,
						query_akun.id_akun,
						query_detail.id_detail,
						query_terms.id_terms,
						query_satuan_volume.id_satuan_volume,
						jumlah_volume,
						jumlah_pagu,
						revisi
						)
	db.session.add(add_db_pok)
	db.session.commit()

	return redirect(url_for('inputdata'))



@app.route('/sisa')
def sisa_pagu():
	id_tabel_pok = []
	program = []
	kegiatan = []
	output = []
	komponen = []
	akun = []
	detail =[]
	jumlah_volume = []
	satuan_volume = []
	jumlah_pagu = []
	sisa_volume = []
	sisa_pagu = []
	
	query_pok = Pok.query.all()
	query_transaksi = db.session.query(Transaksi.id_tabel_pok, db.func.sum(Transaksi.volume), db.func.sum(Transaksi.jumlah_transaksi)).group_by(Transaksi.id_tabel_pok).all()

	for item_pok in query_pok:
		for item_transaksi in query_transaksi:
			if item_pok.id_tabel_pok == item_transaksi[0]:
				sisa_volume.append(item_pok.jumlah_volume - item_transaksi[1])
				sisa_pagu.append(item_pok.jumlah_pagu - item_transaksi[2])
				id_tabel_pok.append(item_pok.id_tabel_pok)
		if item_pok.id_tabel_pok not in id_tabel_pok:
			sisa_volume.append(item_pok.jumlah_volume)
			sisa_pagu.append(item_pok.jumlah_pagu)
			id_tabel_pok.append(item_pok.id_tabel_pok)
		
		program.append(item_pok.program.id_pok)
		kegiatan.append(item_pok.kegiatan.id_pok)
		output.append(item_pok.output.id_pok)
		komponen.append(item_pok.komponen.id_pok)
		akun.append(item_pok.id_akun)
		detail.append(item_pok.detail.deskripsi)
		jumlah_volume.append(item_pok.jumlah_volume)
		satuan_volume.append(item_pok.satuan_volume.deskripsi)
		jumlah_pagu.append(item_pok.jumlah_pagu) 

	gabung = zip(id_tabel_pok, program, kegiatan, output, komponen, akun, detail, jumlah_volume, satuan_volume, jumlah_pagu, sisa_volume, sisa_pagu)		
	return render_template('page_sisa_pagu.html', 	gabung = gabung)

@app.route('/tampilperkomponen/<id_komponen>')
def tampilperkomponen(id_komponen):
	query_pok = Pok.query.filter_by(id_komponen = id_komponen).order_by("id_akun").all()
	query_transaksi = db.session.query(Transaksi.id_tabel_pok, db.func.sum(Transaksi.volume), db.func.sum(Transaksi.jumlah_transaksi)).group_by(Transaksi.id_tabel_pok).all()

	id_tabel_pok = []
	komponen = []
	akun = []
	detail =[]
	jumlah_volume = []
	satuan_volume = []
	jumlah_pagu = []
	sisa_volume = []
	sisa_pagu = []

	for item_pok in query_pok:
		for item_transaksi in query_transaksi:
			if item_pok.id_tabel_pok == item_transaksi[0]:
				sisa_volume.append(item_pok.jumlah_volume - item_transaksi[1])
				sisa_pagu.append(item_pok.jumlah_pagu - item_transaksi[2])
				id_tabel_pok.append(item_pok.id_tabel_pok)
		if item_pok.id_tabel_pok not in id_tabel_pok:
			sisa_volume.append(item_pok.jumlah_volume)
			sisa_pagu.append(item_pok.jumlah_pagu)
			id_tabel_pok.append(item_pok.id_tabel_pok)

		komponen.append(item_pok.komponen.id_pok)
		akun.append(item_pok.id_akun)
		detail.append(item_pok.detail.deskripsi)
		jumlah_volume.append(item_pok.jumlah_volume)
		satuan_volume.append(item_pok.satuan_volume.deskripsi)
		jumlah_pagu.append(item_pok.jumlah_pagu)	

	gabung = zip(id_tabel_pok, komponen, akun, detail, jumlah_volume, satuan_volume, jumlah_pagu, sisa_volume, sisa_pagu)

	return render_template('page_tampil_per_komponen.html', gabung = gabung, query_pok = query_pok)

@app.route('/transaksikomponen/<id_komponen>')
def transaksikomponen(id_komponen):
	akun = []
	desk_akun = []
	tgl_transaksi = []
	keterangan = []
	jlh_transaksi = []
	jlh_volume =[]
	query_pok = Pok.query.filter_by(id_komponen = id_komponen).all()
	komponen = query_pok[0].komponen.deskripsi
	for item_pok in query_pok:
		query_transaksi = Transaksi.query.filter_by(id_tabel_pok = item_pok.id_tabel_pok).all()
		for data in query_transaksi:
			akun.append(item_pok.id_akun)
			desk_akun.append(item_pok.akun.deskripsi)	
			tgl_transaksi.append(data.tanggal_transaksi)
			keterangan.append(data.keterangan)
			jlh_transaksi.append(data.jumlah_transaksi)
			jlh_volume.append(data.volume)
	gabung = zip(akun, desk_akun, tgl_transaksi, keterangan, jlh_transaksi, jlh_volume)
	return render_template('page_tampil_transaksi_per_komponen.html', komponen = komponen, gabung = gabung)

if __name__ == '__main__':
	app.run(debug=True)