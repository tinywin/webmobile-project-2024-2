import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { Observable, throwError } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://127.0.0.1:8000/api/login/'; // URL da API Django

  constructor(private http: HttpClient, private router: Router) {
    this.checkAuthentication();
  }

  public checkAuthentication(): boolean {
    const token = localStorage.getItem('token');
    return !!token; // Retorna verdadeiro se o token existir
  }

  login(username: string, password: string): Observable<any> {
    const body = { username, password };
    return this.http.post(this.apiUrl, body).pipe(
      tap(response => this.handleLogin(response)),
      catchError(error => {
        console.error('Erro no login:', error);
        return throwError(() => new Error('Credenciais inválidas')); // Manipulação de erro
      })
    );
  }
  

  handleLogin(response: any): void {
    const token = response.token; // Certifique-se de que o token é retornado assim
    localStorage.setItem('token', token);
    this.router.navigate(['/home']);
  }

  logout(): void {
    localStorage.removeItem('token');
    this.router.navigate(['/entrar']); // Redireciona corretamente para o login
  }

  isAuthenticated(): boolean {
    return this.checkAuthentication();
  }
}