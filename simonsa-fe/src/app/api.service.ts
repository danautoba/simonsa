import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable()
export class ApiService {
  url_pok = 'http://localhost:5000/api/pok';
  url_sisa = 'http://localhost:5000/api/sisa';

  constructor(private http:HttpClient) { }

  lihat_pok (): void {
    this.http.get(this.url_pok).subscribe(data=> {
      console.log(data);
    });
  }
  
  lihat_sisa (): void {
      this.http.get(this.url_sisa).subscribe(data=> {
        console.log(data);
      });
  }
}
