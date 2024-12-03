import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ProfileService {
  private baseUrl = 'http://127.0.0.1:8000'; // Base URL corrigida
  private apiBase = `${this.baseUrl}/api/`;
  private perfilEndpoint = this.apiBase + 'perfil/';
  private usuariosEndpoint = this.apiBase + 'usuarios/';
  private perfilUsuarioEndpoint = this.apiBase + 'perfil-usuario/';

  constructor(private http: HttpClient) {}

  private getHeaders(): HttpHeaders {
    const token = localStorage.getItem('token');
    return new HttpHeaders({
      'Authorization': `Token ${token}`,
    });
  }

  /**
   * Obtém a URL completa da imagem, adicionando o baseUrl se necessário.
   * @param imagePath Caminho da imagem
   * @returns URL completa da imagem
   */
  getFullImageUrl(imagePath: string | null): string {
    if (!imagePath) {
      return `${this.baseUrl}/media/default-profile.png`; // Imagem padrão
    }
    return imagePath.startsWith('http') ? imagePath : `${this.baseUrl}${imagePath}`;
  }

  /**
   * Obtém o perfil do usuário logado.
   */
  getProfile(): Observable<any> {
    return this.http.get(this.perfilEndpoint + 'me/', { headers: this.getHeaders() });
  }

  /**
   * Obtém o perfil de um usuário específico pelo ID.
   * @param userId ID do usuário
   */
  getUserProfile(userId: string): Observable<any> {
    return this.http.get(`${this.perfilUsuarioEndpoint}${userId}/`, { headers: this.getHeaders() });
  }

  /**
   * Obtém os anúncios de um usuário específico pelo ID.
   * @param userId ID do usuário
   */
  getAnuncios(userId: string): Observable<any> {
    return this.http.get(`${this.usuariosEndpoint}${userId}/anuncios/`, { headers: this.getHeaders() });
  }

  /**
   * Atualiza o perfil do usuário logado.
   * @param data Dados do perfil
   */
  updateProfile(data: any): Observable<any> {
    const headers = this.getHeaders();

    if (data.foto && data.foto instanceof File) {
      const formData = new FormData();
      Object.keys(data).forEach((key) => {
        if (data[key] !== null) {
          formData.append(key, data[key]);
        }
      });
      return this.http.patch(this.perfilEndpoint + 'update_me/', formData, { headers });
    }

    const payload = { ...data };
    delete payload.foto;
    return this.http.patch(this.perfilEndpoint + 'update_me/', payload, { headers });
  }
}