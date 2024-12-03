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
    canActivate: [AuthGuard], // Protegendo a home com AuthGuard
  },
  {
    path: 'cadastro',
    loadComponent: () => import('./cadastro/cadastro.page').then((m) => m.CadastroPage),
  },
  {
    path: 'meuperfil',
    loadComponent: () => import('./meuperfil/meuperfil.page').then((m) => m.MeuPerfilPage),
    canActivate: [AuthGuard],
  },
  {
    path: 'cadastrar-carro',
    loadComponent: () => import('./cadastrar-carro/cadastrar-carro.page').then((m) => m.CadastrarCarroPage),
    canActivate: [AuthGuard],
  },
  {
    path: 'alterar-senha',
    loadComponent: () => import('./alterar-senha/alterar-senha.page').then((m) => m.AlterarSenhaPage),
    canActivate: [AuthGuard],
  },
  {
    path: 'editar-perfil',
    loadComponent: () => import('./editar-perfil/editar-perfil.page').then((m) => m.EditarPerfilPage),
    canActivate: [AuthGuard],
  },
  {
    path: '',
    redirectTo: 'home', // Redirecionar para 'home' como padrão
    pathMatch: 'full',
  },
  {
    path: 'detalhes-carro/:id',
    loadComponent: () => import('./detalhes-carro/detalhes-carro.page').then((m) => m.DetalhesCarroPage),
  },
  {
    path: 'meus-carros',
    loadComponent: () => import('./meus-carros/meus-carros.page').then((m) => m.MeusCarrosPage),
    canActivate: [AuthGuard],
  },
  {
    path: 'editar-carro/:id',
    loadComponent: () => import('./editar-carro/editar-carro.page').then((m) => m.EditarCarroPage),
    canActivate: [AuthGuard],
  },
  {
    path: 'perfil-usuario/:id',
    loadComponent: () => import('./perfil-usuario/perfil-usuario.page').then((m) => m.PerfilUsuarioPage),
  },
];