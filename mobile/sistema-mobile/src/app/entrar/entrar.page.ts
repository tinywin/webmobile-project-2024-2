import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { IonicModule } from '@ionic/angular';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http'; // Importe o HttpClientModule
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-entrar',
  templateUrl: './entrar.page.html',
  styleUrls: ['./entrar.page.scss'],
  standalone: true,
  imports: [IonicModule, ReactiveFormsModule, CommonModule, HttpClientModule] // Inclua HttpClientModule
})
export class EntrarPage {
  loginForm: FormGroup;
  loginError: string | null = null;

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {
    this.loginForm = this.fb.group({
      username: ['', Validators.required],
      password: ['', Validators.required]
    });
  }

  onLogin() {
    if (this.loginForm.valid) {
      const { username, password } = this.loginForm.value;
      this.authService.login(username, password).subscribe({
        next: (response) => {
          this.authService.handleLogin(response);
          this.router.navigate(['/home']);
          this.loginError = null;
        },
        error: (err) => {
          console.error('Erro no login:', err);
          this.loginError = 'Credenciais inválidas';
        }
      });
    } else {
      this.loginError = 'Preencha todos os campos corretamente.';
    }
  }

  goToCadastro() {
    this.router.navigate(['/cadastro']);
  }

  esqueceuSenha() {
    console.log('Recuperação de senha');
  }
}