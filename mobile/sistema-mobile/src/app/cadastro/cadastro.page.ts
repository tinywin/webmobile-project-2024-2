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
  fotoPreview: string | ArrayBuffer | null = null;

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
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

  /**
   * Método chamado quando há mudança no campo de arquivo.
   * Atualiza a pré-visualização da foto e o campo no formulário.
   */
  onFileChange(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input && input.files && input.files.length > 0) {
      const file = input.files[0];
      this.cadastroForm.patchValue({ foto: file });

      // Pré-visualização da imagem
      const reader = new FileReader();
      reader.onload = (e) => {
        this.fotoPreview = e.target?.result ?? null; // Garantir que não seja undefined, mas sim null
      };
      reader.readAsDataURL(file);
    }
  }

  /**
   * Método chamado ao submeter o formulário de cadastro.
   * Valida e envia os dados para o servidor.
   */
  onRegister() {
    if (this.cadastroForm.valid) {
      const formData = new FormData();
      
      // Adiciona todos os campos ao FormData
      Object.keys(this.cadastroForm.value).forEach(key => {
        const value = this.cadastroForm.get(key)?.value;
        if (value !== null) {
          formData.append(key, value);
        }
      });

      // Formatar data_nascimento para 'YYYY-MM-DD'
      const dataNascimento = new Date(this.cadastroForm.get('data_nascimento')?.value).toISOString().split('T')[0];
      formData.set('data_nascimento', dataNascimento);

      this.authService.register(formData).subscribe({
        next: (response) => {
          console.log('Usuário registrado com sucesso!', response);
          this.router.navigate(['/home']);
        },
        error: (error) => console.error('Erro ao registrar usuário:', error),
      });
    } else {
      console.error('Formulário inválido');
    }
  }
}