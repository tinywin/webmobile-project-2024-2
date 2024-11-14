import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { CarrosService } from '../services/carros.service'; // Ajuste o caminho conforme necessário
import { IonicModule } from '@ionic/angular';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-cadastrar-carro',
  templateUrl: './cadastrar-carro.page.html',
  styleUrls: ['./cadastrar-carro.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule]
})
export class CadastrarCarroPage {
  carroForm: FormGroup;

  constructor(
    private fb: FormBuilder,
    private carrosService: CarrosService
  ) {
    this.carroForm = this.fb.group({
      marca: ['', Validators.required],
      modelo: ['', Validators.required],
      ano: ['', [Validators.required, Validators.min(1900), Validators.max(new Date().getFullYear())]],
      cor: ['', Validators.required],
      combustivel: ['', Validators.required],
      quilometragem: ['', Validators.required],
      preco: ['', Validators.required],
      descricao: ['', Validators.required],
      foto: [null]
    });
  }

  onFileChange(event: any) {
    const file = event.target.files[0];
    this.carroForm.patchValue({ foto: file });
  }

  cadastrarCarro() {
    if (this.carroForm.valid) {
      const formData = new FormData();
      Object.keys(this.carroForm.controls).forEach((key) => {
        formData.append(key, this.carroForm.get(key)?.value);
      });
      this.carrosService.cadastrarCarro(formData).subscribe({
        next: (response: any) => alert('Carro cadastrado com sucesso!'),
        error: (error: any) => alert('Erro ao cadastrar carro: ' + error.message)
      });
    } else {
      alert('Preencha todos os campos corretamente.');
    }
  }
}