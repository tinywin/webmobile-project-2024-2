import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { CarrosService } from '../services/carros.service';
import { Router } from '@angular/router';
import { IonicModule } from '@ionic/angular';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-cadastrar-carro',
  templateUrl: './cadastrar-carro.page.html',
  styleUrls: ['./cadastrar-carro.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, ReactiveFormsModule]
})
export class CadastrarCarroPage {
  carroForm: FormGroup;

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
    private router: Router
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

  // Gerenciar upload de arquivo
  onFileChange(event: any) {
    const file = event.target.files[0];
    this.carroForm.patchValue({ foto: file });
  }

  // Método para cadastrar carro
  cadastrarCarro() {
    if (this.carroForm.valid) {
      const formData = this.carroForm.value;
      this.carrosService.cadastrarCarro(formData).subscribe({
        next: () => {
          alert('Carro cadastrado com sucesso!');
          this.voltarParaHome();
        },
        error: (error: any) => alert('Erro ao cadastrar carro: ' + error.message)
      });
    } else {
      alert('Preencha todos os campos corretamente.');
    }
  }

  voltarParaHome() {
    this.router.navigate(['/home']);
  }
}