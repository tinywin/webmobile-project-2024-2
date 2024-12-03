import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ProfileService {
  private baseUrl = 'http://localhost:8000/api/perfil/me/';
  private updateUrl = 'http://localhost:8000/api/perfil/update_me/';

  constructor(private http: HttpClient) {}

  getProfile(): Observable<any> {
    const token = localStorage.getItem('token');
    const headers = new HttpHeaders({
      'Authorization': 'Token ' + token,
    });

    return this.http.get(this.baseUrl, { headers });
  }

  updateProfile(data: any): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': 'Token ' + localStorage.getItem('token'),
    });
  
    // Se houver uma foto válida (do tipo File), utilize FormData
    if (data.foto && data.foto instanceof File) {
      const formData = new FormData();
      Object.keys(data).forEach((key) => {
        if (data[key] !== null) {
          formData.append(key, data[key]);
        }
      });
      return this.http.patch(this.updateUrl, formData, { headers });
    }
  
    // Caso contrário, envie apenas os dados como JSON
    const payload = { ...data };
    delete payload.foto; // Remove a foto do payload se não for um arquivo válido
    return this.http.patch(this.updateUrl, payload, { headers });
  }  
}
