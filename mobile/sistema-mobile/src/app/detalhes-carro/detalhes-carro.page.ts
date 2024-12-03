import { CommonModule } from '@angular/common';
import { IonicModule } from '@ionic/angular';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { Component, OnInit } from '@angular/core';
import { CarrosService } from '../services/carros.service';

@Component({
  selector: 'app-detalhes-carro',
  templateUrl: './detalhes-carro.page.html',
  styleUrls: ['./detalhes-carro.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, RouterModule]
})
export class DetalhesCarroPage implements OnInit {
  carro: any;

  constructor(private route: ActivatedRoute, private carroService: CarrosService) {}

  ngOnInit() {
    const carroId = this.route.snapshot.paramMap.get('id');
    if (carroId) {
      console.log("ID do carro obtido:", carroId); // Debug para verificar se o ID foi obtido corretamente
      this.loadCarroDetails(carroId);
    } else {
      console.error("ID do carro não encontrado");
    }
  }

  loadCarroDetails(id: string) {
    this.carroService.getCarroById(id).subscribe(
      (data) => {
        console.log('Dados do carro recebidos:', data); // Debug para verificar os dados recebidos
        this.carro = data;
      },
      (error) => {
        console.error('Erro ao carregar os detalhes do carro', error);
      }
    );
  }
}