import { Injectable } from '@angular/core';
import { HttpRequest, HttpHandler, HttpEvent, HttpInterceptor } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
    intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
        const token = localStorage.getItem('token'); // Obtém o token do localStorage

        if (token) {
            request = request.clone({
                setHeaders: {
                    Authorization: `Token ${token}` // Adiciona o token ao cabeçalho
                }
            });
        }

        return next.handle(request); // Continua com a requisição
    }
}