export interface PokJson{
	[id_tabel_pok:number] : {
		program_id_pok: string;
		kegiatan_id_pok: string;
		output_id_pok: string;
		komponen_id_pok: string;
		akun_id_pok: number;
		detail:string;
		terms:string;
		jumlah_volume:number;
		satuan_volume:string;
		jumlah_pagu:string;
	}
}


export interface TransaksiJson{
	[id_transaksi:number] : {
		id_tabel_pok: number;
		id_user: number;
		tanggal_transaksi: string;
		volume: number;
		satuan_volume:string;
		jumlah_transaksi:number;
		keterangan:string;
	}
}

export interface KomponenJson{
	[id_tabel_pok:number] : {
		id_komponen:number;
		id_akun:number;
		id_detail:number;
		jumlah_volume:number;
		satuan_volume:number;
		jumlah_pagu:number;
		sisa_volume:number;
		sisa_pagu:number;
	}
}




export interface Komponen{
	["Komponen"] : {
		id_komponen:number;
		id_pok:string;
		deskripsi:string;
	}
}




export interface Payload {
	["id_tabel_pok"]:number;
	["tanggal_transaksi"]:string;
	["volume"]:number;
	["id_satuan_volume"]:number;
	["jumlah_transaksi"]:number;
	["keterangan"]:string;

}
// PokJson ---> {"id_tabel_pok": {"item_tabel_pok":[data1, data2, data3]}}