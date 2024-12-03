import { ComponentFixture, TestBed } from '@angular/core/testing';
import { EditarCarroPage } from './editar-carro.page';

describe('EditarCarroPage', () => {
  let component: EditarCarroPage;
  let fixture: ComponentFixture<EditarCarroPage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(EditarCarroPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
