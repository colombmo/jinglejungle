import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class FileService {

  constructor(private http: HttpClient) { }

  loadPhotos(): Observable<any> {
    return this.http.get("./assets/lnd4.json");
  }
  loadPhotosBern():Observable<any> {
  return this.http.get("./assets/bern.json");
  }
  loadPhotosZurich():Observable<any> {
    return this.http.get("./assets/zurich.json");
    }
  

}
