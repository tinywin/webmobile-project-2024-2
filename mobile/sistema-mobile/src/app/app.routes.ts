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
    canActivate: [AuthGuard],  // Protegendo a home com AuthGuard
  },
  {
    path: 'cadastro',
    loadComponent: () => import('./cadastro/cadastro.page').then((m) => m.CadastroPage),
  },
  {
    path: 'meuperfil',  // O caminho da URL
    loadComponent: () => import('./meuperfil/meuperfil.page').then((m) => m.MeuPerfilPage),
    canActivate: [AuthGuard], // Protegendo o perfil com AuthGuard
  },  
  {
    path: 'cadastrar-carro',
    loadComponent: () => import('./cadastrar-carro/cadastrar-carro.page').then((m) => m.CadastrarCarroPage),
    canActivate: [AuthGuard], // Protegendo a rota de cadastro de carro
  },
  {
    path: 'alterar-senha',
    loadComponent: () => import('./alterar-senha/alterar-senha.page').then((m) => m.AlterarSenhaPage),
    canActivate: [AuthGuard], // Protegendo a rota de alterar senha
  },
  {
    path: 'editar-perfil',
    loadComponent: () => import('./editar-perfil/editar-perfil.page').then((m) => m.EditarPerfilPage),
    canActivate: [AuthGuard], // Protegendo a rota de edição de perfil
  },
  {
    path: '',
    redirectTo: 'entrar',
    pathMatch: 'full',
  },
  {
    path: 'detalhes-carro/:id',  // O `:id` é um parâmetro dinâmico para o ID do carro
    loadComponent: () => import('./detalhes-carro/detalhes-carro.page').then((m) => m.DetalhesCarroPage),
  },
];
