import { ComponentFixture, TestBed } from '@angular/core/testing';
import { DetalhesCarroPage } from './detalhes-carro.page';

describe('DetalhesCarroPage', () => {
  let component: DetalhesCarroPage;
  let fixture: ComponentFixture<DetalhesCarroPage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(DetalhesCarroPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
