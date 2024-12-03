import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CarrosService {
  private apiUrl = 'http://localhost:8000/api/carros/';

  constructor(private http: HttpClient) {}

  // Método para obter todos os carros
  getCarros(): Observable<any> {
    return this.http.get<any>(this.apiUrl);
  }

  // Método para obter os detalhes de um carro específico
  getCarroById(id: string): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}${id}/`);
  }

  // Método para obter os carros do usuário atual
  getMeusCarros(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}meus-carros/`);
  }

  // Método para cadastrar um novo carro
  cadastrarCarro(carroData: any): Observable<any> {
    const formData = new FormData();

    // Adiciona os dados ao FormData
    Object.keys(carroData).forEach(key => {
      formData.append(key, carroData[key]);
    });

    return this.http.post<any>(this.apiUrl, formData);
  }

  // Método para editar um carro específico
  editarCarro(id: number, carroData: any): Observable<any> {
    return this.http.put<any>(`${this.apiUrl}${id}/`, carroData);
  }

// Método para atualizar carro com FormData
atualizarCarro(carroId: number, formData: FormData): Observable<any> {
  return this.http.put(`${this.apiUrl}${carroId}/`, formData);
}
  
  // Método para remover um carro específico
  removerCarro(id: number): Observable<any> {
    return this.http.delete<any>(`${this.apiUrl}${id}/`);
  }
}