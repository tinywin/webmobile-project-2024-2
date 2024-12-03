import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { ProfileService } from '../services/profile.service';
import { Router } from '@angular/router';
import { IonicModule, ToastController } from '@ionic/angular';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-editar-perfil',
  templateUrl: './editar-perfil.page.html',
  styleUrls: ['./editar-perfil.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, ReactiveFormsModule]  // Certifique-se de adicionar ReactiveFormsModule aqui
})
export class EditarPerfilPage implements OnInit {
  profileForm: FormGroup;

  constructor(
    private fb: FormBuilder,
    private profileService: ProfileService,
    private router: Router,
    private toastController: ToastController
  ) {
    this.profileForm = this.fb.group({
      first_name: ['', Validators.required],
      last_name: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      cpf: [''],
      data_nascimento: [''],
      telefone: [''],
      foto: ['']
    });
  }

  ngOnInit() {
    this.loadProfile();
  }

  loadProfile() {
    this.profileService.getProfile().subscribe(
      (data) => {
        this.profileForm.patchValue(data);
      },
      (error) => {
        console.error('Erro ao carregar o perfil', error);
      }
    );
  }

  onFileChange(event: any) {
    if (event.target.files.length > 0) {
      const file = event.target.files[0];
      this.profileForm.patchValue({ foto: file });
    }
  }

  onSave() {
    if (this.profileForm.valid) {
      this.profileService.updateProfile(this.profileForm.value).subscribe(
        (response) => {
          this.presentToast('Perfil atualizado com sucesso!', 'success');
          this.router.navigate(['/meuperfil']);
        },
        (error) => {
          this.presentToast('Erro ao atualizar perfil.', 'danger');
          console.error('Erro ao atualizar perfil', error);
        }
      );
    }
  }

  voltarParaPerfil() {
    this.router.navigate(['/meuperfil']);
  }

  async presentToast(message: string, color: string) {
    const toast = await this.toastController.create({
      message,
      duration: 2000,
      color
    });
    toast.present();
  }

  getFormErrors(): string[] {
    const errors: string[] = [];
    Object.keys(this.profileForm.controls).forEach(key => {
      const controlErrors = this.profileForm.get(key)?.errors;
      if (controlErrors) {
        Object.keys(controlErrors).forEach(errorKey => {
          errors.push(`${key}: ${errorKey}`);
        });
      }
    });
    return errors;
  }

  getProfileImageUrl(imagePath: string): string {
    return imagePath.startsWith('http') ? imagePath : `http://127.0.0.1:8000${imagePath}`;
  }
}
