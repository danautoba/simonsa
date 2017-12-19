import { Component, Input, Output} from '@angular/core';
import { Pipe, PipeTransform } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Response } from '@angular/http';
import { Observable } from "rxjs/Observable";
import { NgForm, FormGroup, FormControl } from "@angular/forms";
import "rxjs/Rx";
import 'rxjs/add/operator/map';
import { PokJson, TransaksiJson, KomponenJson, Komponen } from './data';

@Pipe({name: 'keys'})
export class KeysPipe implements PipeTransform {
  transform(value, args:string[]) : any {
    let keys = [];
    for (let key in value) {
      keys.push({key: key, value: value[key]});
    }
    return keys;
  }
}

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})


export class AppComponent {  
  pilihKomponen:number;
  pilihAkun:number;
  pilihDetail:number;
  id:KomponenJson;
  id_pok:number;

  title = 'Simonsa';
  pok_url = 'http://localhost:5000/api/pok';
  pok_url_khusus = 'http://localhost:5000/api/pok/khusus/';
  transaksi_url = 'http://localhost:5000/api/transaksi';
  komponen_url = 'http://localhost:5000/api/komponen';
  tampilPok = false;
  tampilTransaksi = false;
  tampilFormTransaksi = false;
  tampilFormAkun = false;
  public id_komponen;

  list_pok:PokJson;
  list_transaksi:TransaksiJson;
  items_komponen_pok:KomponenJson;
  item_komponen_lain:KomponenJson;
  item_atomic:KomponenJson;
  idPok:KomponenJson;
  item_komponen:Komponen;


  constructor (private http:HttpClient) {
    
  }

  getPok() {
  	this.http
  		.get(this.pok_url)
  		.subscribe(
  			(datapok:PokJson) => {
  				this.list_pok = datapok;
  			}
  		);
  		this.tampilPok = true;
  		this.tampilTransaksi = false;
  		this.tampilFormTransaksi = false;
  	};

  getTransaksi() {
  	this.http
  		.get(this.transaksi_url)
  		.subscribe(
  			(datatransaksi:TransaksiJson) => {
  				this.list_transaksi = datatransaksi;
  				console.log(this.list_transaksi);
  			}
  		);
  		this.tampilTransaksi = true;
  		this.tampilPok = false;
  		this.tampilFormTransaksi = false;
  	};


  getKomponen() {
  	this.http
  		.get(this.komponen_url)
  		.subscribe(
  			(datakomponen:Komponen) => {
  				this.item_komponen = datakomponen;
  				//console.log(this.item_komponen);
  			}
  		);
  		this.tampilFormTransaksi = true;
  		this.tampilTransaksi = false;
  		this.tampilPok = false;
  	}

  getKomponenItems(id_komponen:number) {
  	this.http
  		.get(this.pok_url_khusus+id_komponen)
  		.subscribe(
  			(itemkomponen:KomponenJson) => {
  				this.item_komponen_lain = itemkomponen;
  				console.log(this.item_komponen_lain);
  				console.log(id_komponen);
  			}
  		);
  		this.tampilFormAkun = true;
  	}	



    getAtomicItems(id_komponen, id_akun) {
  	this.http
  		.get(this.pok_url_khusus+id_komponen+"/"+id_akun)
 		  .subscribe(
 			(itematomic:KomponenJson) => {
  				this.item_atomic = itematomic;
  				console.log(this.item_atomic);
  				console.log(id_komponen);
  				console.log(id_akun);

  			}
 		);
  	}


  	getIdTabelPOK(id_komponen, id_akun, id_detail) {
  		this.http
  			.get(this.pok_url_khusus+id_komponen+"/"+id_akun+"/"+id_detail)
  			.subscribe(
  					(id_tabel_pok:KomponenJson) => {
  						this.idPok = id_tabel_pok;
  						console.log(this.idPok['item_tabel_pok']);
  						console.log(id_komponen);
  						console.log(id_akun);
  						console.log(id_detail);
  					}
  				);
  	}


  	simpanTransaksi(f) {
  		console.log(f);
  	}

  ngOnInit():void {
  	
  	};
}


