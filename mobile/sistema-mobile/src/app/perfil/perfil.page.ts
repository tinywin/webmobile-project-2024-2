import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { IonicModule } from '@ionic/angular';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';
import { ProfileService } from '../services/profile.service';

@Component({
  selector: 'app-perfil',
  templateUrl: './perfil.page.html',
  styleUrls: ['./perfil.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, RouterModule, HttpClientModule]
})
export class PerfilPage implements OnInit {
  profile: any = null;

  constructor(private router: Router, private profileService: ProfileService) {}

  ngOnInit() {
    this.loadProfile();
  }

  loadProfile() {
    this.profileService.getProfile().subscribe(
      (data) => {
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

  getProfileImageUrl(imagePath: string): string {
    return imagePath.startsWith('http') ? imagePath : `http://127.0.0.1:8000${imagePath}`;
  }
}