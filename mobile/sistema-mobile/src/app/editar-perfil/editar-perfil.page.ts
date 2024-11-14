import { Component } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { IonicModule } from '@ionic/angular';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-editar-perfil',
  templateUrl: './editar-perfil.page.html',
  styleUrls: ['./editar-perfil.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, ReactiveFormsModule]
})
export class EditarPerfilPage {
  perfilForm: FormGroup;

  constructor(private fb: FormBuilder, private router: Router) {
    // Inicializando o formulário de edição de perfil
    this.perfilForm = this.fb.group({
      first_name: ['', Validators.required],
      last_name: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      foto: [null],
      cpf: ['', Validators.required],
      data_nascimento: ['', Validators.required]
    });
  }

  onSubmit() {
    if (this.perfilForm.valid) {
      console.log('Dados do perfil salvos:', this.perfilForm.value);
      // Aqui você pode implementar a lógica para salvar os dados do perfil no backend
      this.router.navigate(['/meuperfil']); // Redireciona para a página do perfil
    } else {
      console.error('Formulário inválido');
    }
  }

  alterarFoto(event: any) {
    const file = event.target.files[0];
    if (file) {
      // Simulando a atualização da foto
      const reader = new FileReader();
      reader.onload = () => {
        this.perfilForm.patchValue({ foto: reader.result });
      };
      reader.readAsDataURL(file);
    }
  }
}
