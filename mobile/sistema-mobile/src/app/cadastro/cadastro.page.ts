import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { AuthService } from '../services/auth.service';
import { Router } from '@angular/router';
import { IonicModule } from '@ionic/angular';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-cadastro',
  templateUrl: './cadastro.page.html',
  styleUrls: ['./cadastro.page.scss'],
  standalone: true,
  imports: [IonicModule, ReactiveFormsModule, CommonModule],
})
export class CadastroPage {
  cadastroForm: FormGroup;

  constructor(
    private fb: FormBuilder,
    private authService: AuthService, // Importando AuthService
    private router: Router
  ) {
    this.cadastroForm = this.fb.group({
      first_name: ['', Validators.required],
      last_name: ['', Validators.required],
      username: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      confirm_password: ['', Validators.required],
      data_nascimento: ['', Validators.required],
      cpf: ['', [Validators.required, Validators.pattern('^[0-9]{11}$')]],
      telefone: ['', Validators.required],
      foto: [null],
    });
  }

  onFileChange(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input && input.files && input.files.length > 0) {
      const file = input.files[0];
      this.cadastroForm.patchValue({ foto: file });
    }
  }

  onRegister() {
    if (this.cadastroForm.valid) {
      const formData = this.cadastroForm.value;
  
      // Converter data_nascimento para o formato 'YYYY-MM-DD'
      const dataNascimento = new Date(formData.data_nascimento).toISOString().split('T')[0];
      formData.data_nascimento = dataNascimento;
  
      console.log('Dados enviados:', formData);
  
      this.authService.register(formData).subscribe({
        next: (response) => console.log('Usuário registrado com sucesso!', response),
        error: (error) => console.error('Erro ao registrar usuário:', error),
      });
    } else {
      console.error('Formulário inválido');
    }
  }
}  