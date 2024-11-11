import { IonicModule } from '@ionic/angular';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CarrosService } from '../services/carros.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.page.html',
  styleUrls: ['./home.page.scss'],
  standalone: true,
  imports: [IonicModule] // Adiciona o IonicModule para componentes standalone
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
        this.carros = data;
      },
      (error) => {
        console.error('Erro ao carregar os anúncios públicos', error);
      }
    );
  }

  goToDetails(carroId: number) {
    this.router.navigate(['/detalhes-carro', carroId]);
  }
}