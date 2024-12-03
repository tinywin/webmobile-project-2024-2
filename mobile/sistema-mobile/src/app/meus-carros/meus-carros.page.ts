import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CarrosService } from '../services/carros.service';
import { IonicModule } from '@ionic/angular';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';
import { AuthService } from '../services/auth.service'; // Importar o AuthService

@Component({
  selector: 'app-meus-carros',
  templateUrl: './meus-carros.page.html',
  styleUrls: ['./meus-carros.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, RouterModule, HttpClientModule]
})
export class MeusCarrosPage implements OnInit {
  carros: any[] = [];
  erroCarregamento: string | null = null;

  constructor(
    private carroService: CarrosService,
    private router: Router,
    private authService: AuthService // Injetar o AuthService
  ) {}

  ngOnInit() {
    this.loadMeusCarros();
  }

  // Carregar os carros do usuário atual
  loadMeusCarros() {
    this.carroService.getMeusCarros().subscribe(
      (data) => {
        this.carros = data;
        this.erroCarregamento = null;
      },
      (error) => {
        console.error('Erro ao carregar os carros do usuário', error);
        this.erroCarregamento = 'Erro ao carregar seus carros. Tente novamente mais tarde.';
      }
    );
  }

  // Método para editar carro
  editarCarro(carroId: number) {
    this.router.navigate(['/editar-carro', carroId]);
  }

  // Método para remover carro
  removerCarro(carroId: number) {
    if (confirm('Tem certeza que deseja remover este carro?')) {
      this.carroService.removerCarro(carroId).subscribe(
        () => {
          // Atualiza a lista de carros removendo o carro deletado
          this.carros = this.carros.filter(carro => carro.id !== carroId);
        },
        (error) => {
          console.error('Erro ao remover o carro', error);
          alert('Erro ao remover o carro. Tente novamente mais tarde.');
        }
      );
    }
  }

  // Método para logout
  logout() {
    this.authService.logout();
  }
}