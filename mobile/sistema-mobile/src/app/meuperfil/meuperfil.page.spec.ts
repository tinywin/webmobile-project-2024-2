import { ComponentFixture, TestBed } from '@angular/core/testing';
import { MeuPerfilPage } from './meuperfil.page'; // Atualize para MeuperfilPage

describe('MeuperfilPage', () => {  // Atualize para MeuperfilPage
  let component: MeuPerfilPage;
  let fixture: ComponentFixture<MeuPerfilPage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(MeuPerfilPage); // Atualize aqui também
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});