import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ProfileService {
  private apiUrl = 'http://127.0.0.1:8000/api/perfil/me/';

  constructor(private http: HttpClient) {}

  getProfile(): Observable<any> {
    const token = localStorage.getItem('token');
    if (!token) {
      console.error("Token de autenticação não encontrado.");
      throw new Error("Token de autenticação não encontrado.");
    }

    const headers = new HttpHeaders({
      'Authorization': `Token ${token}`
    });

    return this.http.get(this.apiUrl, { headers });
  }
}