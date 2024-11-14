import { ComponentFixture, TestBed } from '@angular/core/testing';
import { CadastrarCarroPage } from './cadastrar-carro.page';

describe('CadastrarCarroPage', () => {
  let component: CadastrarCarroPage;
  let fixture: ComponentFixture<CadastrarCarroPage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(CadastrarCarroPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
