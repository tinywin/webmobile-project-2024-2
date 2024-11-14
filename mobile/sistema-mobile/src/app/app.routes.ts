import { Routes } from '@angular/router';
import { AuthGuard } from './services/auth.guard';

export const routes: Routes = [
  {
    path: 'entrar',
    loadComponent: () => import('./entrar/entrar.page').then((m) => m.EntrarPage),
  },
  {
    path: 'home',
    loadComponent: () => import('./home/home.page').then((m) => m.HomePage),
    canActivate: [AuthGuard],
  },
  {
    path: 'cadastro',
    loadComponent: () => import('./cadastro/cadastro.page').then((m) => m.CadastroPage),
  },
  {
    path: 'perfil',
    loadComponent: () => import('./perfil/perfil.page').then((m) => m.PerfilPage),
    canActivate: [AuthGuard], // Protegendo o perfil com AuthGuard (opcional)
  },
  {
    path: 'cadastrar-carro',
    loadComponent: () => import('./cadastrar-carro/cadastrar-carro.page').then((m) => m.CadastrarCarroPage),
    canActivate: [AuthGuard], // Protegendo a rota de cadastro de carro, se necessário
  },
  {
    path: '',
    redirectTo: 'entrar',
    pathMatch: 'full',
  },
];