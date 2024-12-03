import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { IonicModule } from '@ionic/angular';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-alterar-senha',
  templateUrl: './alterar-senha.page.html',
  styleUrls: ['./alterar-senha.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, ReactiveFormsModule]
})
export class AlterarSenhaPage {
  senhaForm: FormGroup;

  constructor(
    private fb: FormBuilder,
    private router: Router
  ) {
    this.senhaForm = this.fb.group(
      {
        senhaAntiga: ['', Validators.required],
        novaSenha1: ['', [Validators.required, Validators.minLength(6)]],
        novaSenha2: ['', Validators.required],
      },
      { validator: this.passwordsMatch }
    );
  }

  passwordsMatch(form: FormGroup) {
    const novaSenha1 = form.get('novaSenha1')?.value;
    const novaSenha2 = form.get('novaSenha2')?.value;

    return novaSenha1 === novaSenha2 ? null : { passwordMismatch: true };
  }

  alterarSenha() {
    if (this.senhaForm.valid) {
      alert('Senha alterada com sucesso!');
      this.voltarParaPerfil();
    } else {
      this.senhaForm.markAllAsTouched();
    }
  }

  voltarParaPerfil() {
    this.router.navigate(['/meuperfil']);
  }
}