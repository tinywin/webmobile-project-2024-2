import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { CarrosService } from '../services/carros.service';
import { IonicModule } from '@ionic/angular';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-editar-carro',
  templateUrl: './editar-carro.page.html',
  styleUrls: ['./editar-carro.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, ReactiveFormsModule]
})
export class EditarCarroPage implements OnInit {
  carroForm: FormGroup;
  carroId!: number;

  marcasChoices = [
    { value: 'FORD', label: 'Ford' },
    { value: 'CHEVROLET', label: 'Chevrolet' },
    { value: 'FIAT', label: 'Fiat' },
    { value: 'VOLKSWAGEN', label: 'Volkswagen' },
    { value: 'HYUNDAI', label: 'Hyundai' },
    { value: 'HONDA', label: 'Honda' },
    { value: 'TOYOTA', label: 'Toyota' },
    { value: 'RENAULT', label: 'Renault' },
    { value: 'NISSAN', label: 'Nissan' },
    { value: 'JEEP', label: 'Jeep' },
    { value: 'PEUGEOT', label: 'Peugeot' },
    { value: 'CITROEN', label: 'Citroën' },
    { value: 'MITSUBISHI', label: 'Mitsubishi' },
    { value: 'BMW', label: 'BMW' },
    { value: 'MERCEDES', label: 'Mercedes-Benz' },
    { value: 'AUDI', label: 'Audi' },
    { value: 'KIA', label: 'Kia' },
    { value: 'LANDROVER', label: 'Land Rover' },
    { value: 'VOLVO', label: 'Volvo' },
    { value: 'CHERY', label: 'Chery' },
  ];

  coresChoices = [
    { value: 'PRETO', label: 'Preto' },
    { value: 'BRANCO', label: 'Branco' },
    { value: 'PRATA', label: 'Prata' },
    { value: 'CINZA', label: 'Cinza' },
    { value: 'VERMELHO', label: 'Vermelho' },
    { value: 'AZUL', label: 'Azul' },
    { value: 'VERDE', label: 'Verde' },
  ];

  combustivelChoices = [
    { value: 'GASOLINA', label: 'Gasolina' },
    { value: 'ALCOOL', label: 'Álcool' },
    { value: 'DIESEL', label: 'Diesel' },
    { value: 'FLEX', label: 'Flex' },
    { value: 'ELETRICO', label: 'Elétrico' },
  ];

  constructor(
    private fb: FormBuilder,
    private carrosService: CarrosService,
    private router: Router,
    private route: ActivatedRoute
  ) {
    this.carroForm = this.fb.group({
      marca: ['', Validators.required],
      modelo: ['', Validators.required],
      ano: ['', [Validators.required, Validators.min(1886), Validators.max(new Date().getFullYear())]],
      cor: ['', Validators.required],
      combustivel: ['', Validators.required],
      quilometragem: ['', Validators.required],
      preco: ['', [Validators.required, Validators.min(0.01)]],
      descricao: [''],
      foto: [null]
    });
  }

  ngOnInit() {
    const idParam = this.route.snapshot.paramMap.get('id');
    if (idParam) {
      this.carroId = +idParam;
      this.carrosService.getCarroById(this.carroId.toString()).subscribe({
        next: (carro) => {
          this.carroForm.patchValue({
            marca: carro.marca,
            modelo: carro.modelo,
            ano: carro.ano,
            cor: carro.cor,
            combustivel: carro.combustivel,
            quilometragem: carro.quilometragem,
            preco: carro.preco,
            descricao: carro.descricao
          });
        },
        error: (error) => {
          console.error('Erro ao carregar os dados do carro:', error);
          alert('Erro ao carregar os dados do carro. Tente novamente mais tarde.');
          this.voltarParaHome();
        }
      });
    } else {
      alert('ID do carro não encontrado. Redirecionando para a página inicial.');
      this.voltarParaHome();
    }
  }

  // Gerenciar upload de arquivo
  onFileChange(event: any) {
    const file = event.target.files[0];
    this.carroForm.patchValue({ foto: file });
  }

// Método para editar carro
editarCarro() {
  if (this.carroForm.valid) {
    // Cria o FormData para enviar os dados
    const formData = new FormData();
    const carroAtualizado = this.carroForm.value;

    // Adiciona todos os campos ao FormData
    formData.append('marca', carroAtualizado.marca);
    formData.append('modelo', carroAtualizado.modelo);
    formData.append('ano', carroAtualizado.ano.toString());
    formData.append('cor', carroAtualizado.cor);
    formData.append('combustivel', carroAtualizado.combustivel);
    formData.append('quilometragem', carroAtualizado.quilometragem.toString());
    formData.append('preco', carroAtualizado.preco.toString());
    formData.append('descricao', carroAtualizado.descricao);

    // Adiciona a foto ao FormData se houver uma selecionada
    if (this.carroForm.get('foto')?.value) {
      formData.append('foto', this.carroForm.get('foto')?.value);
    }

    // Faz a requisição para atualizar o carro
    this.carrosService.atualizarCarro(this.carroId, formData).subscribe({
      next: () => {
        alert('Carro atualizado com sucesso!');
        this.voltarParaHome();
      },
      error: (error: any) => {
        console.error('Erro ao atualizar o carro:', error);
        alert('Erro ao atualizar o carro. Tente novamente mais tarde.');
      }
    });
  } else {
    alert('Preencha todos os campos corretamente.');
  }
}
  voltarParaHome() {
    this.router.navigate(['/home']);
  }
}