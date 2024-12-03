import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { Observable, throwError } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrlLogin = 'http://127.0.0.1:8000/api/login/'; // URL da API de login
  private apiUrlRegister = 'http://127.0.0.1:8000/api/register/'; // URL da API de registro

  constructor(private http: HttpClient, private router: Router) {
    this.checkAuthentication();
  }

  public checkAuthentication(): boolean {
    const token = localStorage.getItem('token');
    return !!token; // Retorna verdadeiro se o token existir
  }

  // Método de login
  login(username: string, password: string): Observable<any> {
    const body = { username, password };
    return this.http.post(this.apiUrlLogin, body).pipe(
      tap(response => this.handleLogin(response)),
      catchError(error => {
        console.error('Erro no login:', error);
        return throwError(() => new Error('Credenciais inválidas')); // Manipulação de erro
      })
    );
  }

  // Método de registro
  register(data: any): Observable<any> {
    return this.http.post(this.apiUrlRegister, data).pipe(
      tap(response => {
        console.log('Usuário registrado com sucesso:', response);
        this.router.navigate(['/entrar']); // Redireciona para a página de login após registro
      }),
      catchError(error => {
        console.error('Erro no registro:', error);
        return throwError(() => new Error('Erro ao registrar. Verifique os dados e tente novamente.')); // Manipulação de erro
      })
    );
  }

  handleLogin(response: any): void {
    const token = response.token; // Certifique-se de que o token é retornado assim
    localStorage.setItem('token', token);
    this.router.navigate(['/home']);
  }

  logout(): void {
    this.http.post('http://127.0.0.1:8000/api/logout/', {}).subscribe({
      next: () => {
        localStorage.removeItem('token'); // Remove o token local
        this.router.navigate(['/entrar']); // Redireciona para a tela de login
      },
      error: (error) => {
        console.error('Erro ao fazer logout:', error);
        alert('Erro ao realizar logout. Tente novamente.');
      },
    });
  }  
  isAuthenticated(): boolean {
    return this.checkAuthentication();
  }
}