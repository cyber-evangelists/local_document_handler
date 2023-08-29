import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DocumentUploaderComponent } from './document-uploader.component';

describe('DocumentUploaderComponent', () => {
  let component: DocumentUploaderComponent;
  let fixture: ComponentFixture<DocumentUploaderComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [DocumentUploaderComponent]
    });
    fixture = TestBed.createComponent(DocumentUploaderComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
