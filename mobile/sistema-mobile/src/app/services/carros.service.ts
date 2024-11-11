import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CarrosService {
  private apiUrl = 'http://localhost:8100/api/carros';

  constructor(private http: HttpClient) {}

  getCarros(): Observable<any> {
    return this.http.get(this.apiUrl);
  }
}
