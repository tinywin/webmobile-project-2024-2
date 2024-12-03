import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ProfileService } from '../services/profile.service';
import { IonicModule } from '@ionic/angular';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-perfil-usuario',
  templateUrl: './perfil-usuario.page.html',
  styleUrls: ['./perfil-usuario.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, RouterModule, HttpClientModule]
})
export class PerfilUsuarioPage implements OnInit {
  usuario: any = null;
  anuncios: any[] = [];

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private profileService: ProfileService
  ) {}

  ngOnInit() {
    this.loadUserProfile();
  }

  /**
   * Carrega o perfil do usuário a partir do ID fornecido na rota.
   */
  loadUserProfile() {
    const userId = this.route.snapshot.paramMap.get('id');

    if (!userId) {
      console.error('ID do usuário não fornecido na rota.');
      return;
    }

    // Faz requisição ao novo endpoint para buscar o perfil e os anúncios
    this.profileService.getUserProfile(userId).subscribe(
      (data) => {
        this.usuario = data.user; // Dados do usuário
        this.usuario.telefone = data.profile.telefone || 'Não informado'; // Adiciona o telefone
        this.anuncios = data.anuncios; // Lista de anúncios
      },
      (error) => {
        console.error('Erro ao carregar o perfil do usuário:', error);
      }
    );
  }

  /**
   * Navega para a página de detalhes do carro.
   * @param carroId ID do carro
   */
  goToDetalhesCarro(carroId: string) {
    this.router.navigate(['/detalhes-carro', carroId]);
  }

  /**
   * Retorna a URL completa para a imagem de perfil, se disponível.
   */
  getProfileImageUrl(imagePath: string | null): string {
    const baseUrl = 'http://127.0.0.1:8000'; // Base URL do servidor
    if (!imagePath) {
      return `${baseUrl}/media/default-profile.png`; // Exibe imagem padrão
    }
    return imagePath.startsWith('http') ? imagePath : `${baseUrl}${imagePath}`;
  }  
  /**
   * Redireciona para a página inicial.
   */
  goToHome() {
    this.router.navigate(['/']);
  }
}