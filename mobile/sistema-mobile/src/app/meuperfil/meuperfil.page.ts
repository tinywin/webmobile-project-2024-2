import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { IonicModule } from '@ionic/angular';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';
import { ProfileService } from '../services/profile.service';
import { AuthService } from '../services/auth.service'; // Importar AuthService

@Component({
  selector: 'app-meuperfil',
  templateUrl: './meuperfil.page.html',
  styleUrls: ['./meuperfil.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, RouterModule, HttpClientModule]
})
export class MeuPerfilPage implements OnInit {
  profile: any = null;

  constructor(
    private router: Router,
    private profileService: ProfileService,
    private authService: AuthService // Injetar o AuthService
  ) {}

  ngOnInit() {
    this.loadProfile();
  }

  loadProfile() {
    this.profileService.getProfile().subscribe(
      (data) => {
        if (data.date_joined) {
          const date = new Date(data.date_joined);
          const day = String(date.getDate()).padStart(2, '0');
          const month = String(date.getMonth() + 1).padStart(2, '0'); // Janeiro é 0
          const year = date.getFullYear();
          data.date_joined = `${day}/${month}/${year}`;
        }
        this.profile = data;
      },
      (error) => {
        console.error('Erro ao carregar o perfil', error);
      }
    );
  }

  editarPerfil() {
    this.router.navigate(['/editar-perfil']);
  }

  voltarParaHome() {
    this.router.navigate(['/home']);
  }

  getProfileImageUrl(imagePath: string): string {
    return imagePath.startsWith('http') ? imagePath : `http://127.0.0.1:8000${imagePath}`;
  }

  logout() {
    this.authService.logout();
  }
}