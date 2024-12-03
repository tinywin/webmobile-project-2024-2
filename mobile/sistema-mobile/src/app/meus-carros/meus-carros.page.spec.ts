import { ComponentFixture, TestBed } from '@angular/core/testing';
import { MeusCarrosPage } from './meus-carros.page';

describe('MeusCarrosPage', () => {
  let component: MeusCarrosPage;
  let fixture: ComponentFixture<MeusCarrosPage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(MeusCarrosPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
