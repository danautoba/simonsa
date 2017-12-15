from flask import Flask, url_for, jsonify, request 
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
from uuid import uuid4


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:heliumvoldo@localhost/simonsa'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)

from models import * 



@app.route('/api/transaksi', methods = ['GET'])
def api_lihat_transaksi():
	dict_transaksi = {}
	data_transaksi = Transaksi.query.all()
	for data in data_transaksi:
		dict_transaksi[data.id_transaksi] = {"data_transaksi": [data.id_tabel_pok, 
											data.id_user, 
											data.tanggal_transaksi, 
											data.volume, 
											data.t_satuan_volume.deskripsi, 
											data.jumlah_transaksi, 
											data.keterangan]}
	return jsonify(dict_transaksi)


@app.route('/api/transaksi/<int:id_transaksi>', methods = ['GET'])
def api_lihat_item_transaksi(id_transaksi):
	dict_transaksi = {}
	data_transaksi = Transaksi.query.filter_by(id_transaksi = id_transaksi).first()
	dict_transaksi[data_transaksi.id_transaksi] = {"data_transaksi": [data_transaksi.id_tabel_pok, 
													data_transaksi.id_user, 
													data_transaksi.tanggal_transaksi, 
													data_transaksi.volume, 
													data_transaksi.id_satuan_volume, 
													data_transaksi.jumlah_transaksi, 
													data_transaksi.keterangan]}
	return jsonify(dict_transaksi)


@app.route('/api/transaksi/perkomponen/<int:kode_komponen>')
def transaksikomponen(kode_komponen):
	id_transaksi = []
	komponen = []
	akun = []
	desk_akun = []
	tgl_transaksi = []
	keterangan = []
	jlh_transaksi = []
	jlh_volume =[]
	query_pok = Pok.query.filter_by(id_komponen = kode_komponen).all()
	for item_pok in query_pok:
		query_transaksi = Transaksi.query.filter_by(id_tabel_pok = item_pok.id_tabel_pok).all()
		for data in query_transaksi:
			id_transaksi.append(data.id_transaksi)
			komponen.append(item_pok.komponen.id_pok)
			akun.append(item_pok.id_akun)
			desk_akun.append(item_pok.akun.deskripsi)	
			tgl_transaksi.append(data.tanggal_transaksi)
			keterangan.append(data.keterangan)
			jlh_transaksi.append(data.jumlah_transaksi)
			jlh_volume.append(data.volume)
	gabung = zip(id_transaksi, tgl_transaksi, komponen, akun, desk_akun, jlh_transaksi, jlh_volume, keterangan)
	dict_transaksi = {}
	for data in gabung:
		dict_transaksi[data[0]] = {"data_transaksi":[	data[1], 
														data[2], 
														data[3], 
														data[4],
														data[5],
														data[6],
														data[7]		]}
	return jsonify({"Transaksi":dict_transaksi})



@app.route('/api/transaksi', methods = ['POST'])
def api_entri_transaksi():	
	data_transaksi = Transaksi.from_json_transaksi(request.json)
	db.session.add(data_transaksi)
	db.session.commit()
	return jsonify(data_transaksi.to_json_transaksi())


@app.route('/api/sisa')
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
				sisa_volume.append(str(item_pok.jumlah_volume - item_transaksi[1]))
				sisa_pagu.append(str(item_pok.jumlah_pagu - item_transaksi[2]))
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

	return jsonify(dict(zip(id_tabel_pok, zip(	program, 
												kegiatan, 
												output, 
												komponen, 
												akun, 
												detail, 
												jumlah_volume, 
												satuan_volume, 
												jumlah_pagu, 
												sisa_volume, 
												sisa_pagu))))



@app.route('/api/pok')
def api_pok():
	list_pok = Pok.query.all()
	dict_pok = {}
	for item in list_pok:
		dict_pok[item.id_tabel_pok] = {"item_tabel_pok":[item.program.id_pok, 
										item.kegiatan.id_pok, 
										item.output.id_pok, 
										item.komponen.id_pok, 
										item.id_akun, 
										item.detail.deskripsi, 
										item.terms.deskripsi, 
										item.jumlah_volume, 
										item.satuan_volume.deskripsi,  
										item.jumlah_pagu	]}
	return jsonify(dict_pok)



@app.route('/api/program', methods=['GET', 'POST'])
def api_program():
	if request.method == 'GET':
		list_program = Program.query.all()
		dict_program = {}
		for item in list_program:
			dict_program[item.id_program] = item.deskripsi
		return jsonify({"Program":dict_program})
	if request.method == 'POST':
		program = Program.from_json_program(request.json)
		db.session.add(program)
		db.session.commit()
		return jsonify({"Program":program.to_json_program()})



@app.route('/api/kegiatan', methods=['GET'])
def api_kegiatan():
	list_kegiatan = Kegiatan.query.all()
	dict_kegiatan = {}
	for item in list_kegiatan:
		dict_kegiatan[item.id_pok] = item.deskripsi
	return jsonify({"Kegiatan":dict_kegiatan})



@app.route('/api/output', methods=['GET'])
def api_output():
	list_output = Output.query.all()
	dict_output = {}
	for item in list_output:
		dict_output[item.id_pok] = item.deskripsi
	return jsonify({"Output":dict_output})



@app.route('/api/komponen', methods=['GET'])
def api_komponen():
	list_komponen = Komponen.query.all()
	dict_komponen = {}
	for item in list_komponen:
		dict_komponen[item.id_komponen] = [item.id_pok, item.deskripsi]
	return jsonify(dict_komponen)


@app.route('/api/pok/khusus/<id_komponen>', methods=['GET'])
@app.route('/api/pok/khusus/<id_komponen>/<id_akun>', methods=['GET'])
@app.route('/api/pok/khusus/<id_komponen>/<id_akun>/<id_detail>', methods=['GET'])
def tampilperkomponen(id_komponen, id_akun=None, id_detail=None):
	if id_akun and id_detail is not None:
		query_pok = Pok.query.filter_by(id_komponen = id_komponen).filter_by(id_akun=id_akun).filter_by(id_detail=id_detail).all()
	elif id_akun is not None:
		query_pok = Pok.query.filter_by(id_komponen = id_komponen).filter_by(id_akun=id_akun).all()
	else:
		query_pok = Pok.query.filter_by(id_komponen = id_komponen).all()
	
	dict_pok = {}
	if query_pok:
		for item in query_pok:
			dict_pok[item.id_tabel_pok] = [	item.program.id_pok, 
												item.kegiatan.id_pok, 
												item.output.id_pok, 
												item.komponen.id_pok,
												item.komponen.deskripsi, 
												item.akun.id_akun,
												item.akun.deskripsi,
												item.detail.id_detail, 
												item.detail.deskripsi, 
												item.terms.deskripsi, 
												item.jumlah_volume, 
												item.satuan_volume.deskripsi,  
												item.jumlah_pagu	]												
		return jsonify(dict_pok)
	else:
		return jsonify({"item_tabel_pok" : "Tidak ada"})
	


@app.route('/api/akun', methods=['GET'])
def api_akun():
	list_akun = Akun.query.all()
	dict_akun = {}
	for item in list_akun:
		dict_akun[item.id_akun] = item.deskripsi
	return jsonify({"Akun":dict_akun})



@app.route('/api/detail', methods=['GET'])
def api_detail():
	list_detail = Detail.query.all()
	dict_detail = {}
	for item in list_detail:
		dict_detail[item.id_detail] = item.deskripsi
	return jsonify({"Detail":dict_detail})



if __name__ == '__main__':
	app.run(debug=True)