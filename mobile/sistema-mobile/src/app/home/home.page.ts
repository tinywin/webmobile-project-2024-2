import { IonicModule } from '@ionic/angular';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';
import { CarrosService } from '../services/carros.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.page.html',
  styleUrls: ['./home.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, RouterModule, HttpClientModule]
})
export class HomePage implements OnInit {
  carros: any[] = [];

  constructor(private carroService: CarrosService, private router: Router) {}

  ngOnInit() {
    this.loadCarros();
  }

  loadCarros() {
    this.carroService.getCarros().subscribe(
      (data) => {
        console.log('Dados recebidos:', data); // Verifique se os dados estão chegando aqui
        this.carros = data;
      },
      (error) => {
        console.error('Erro ao carregar os anúncios', error);
      }
    );
  }
  

  goToDetails(carroId: number) {
    this.router.navigate(['/detalhes-carro', carroId]);
  }

  goToPerfil() {
    this.router.navigate(['/perfil']);
  }
}