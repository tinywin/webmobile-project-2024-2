import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CarrosService {
  private apiUrl = 'http://localhost:8000/api/carros'; // Endpoint do backend

  constructor(private http: HttpClient) {}

  // Método para obter todos os carros
  getCarros(): Observable<any> {
    return this.http.get<any>(this.apiUrl);
  }

  // Método para cadastrar um novo carro
  cadastrarCarro(carroData: any): Observable<any> {
    const formData = new FormData();

    // Adiciona cada campo do carroData ao formData, incluindo a foto
    Object.keys(carroData).forEach(key => {
      formData.append(key, carroData[key]);
    });

    // Faz o envio do formData para a API
    return this.http.post<any>(this.apiUrl, formData);
  }
}
