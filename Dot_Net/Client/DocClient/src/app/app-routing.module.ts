import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DocumentUploaderComponent } from './document-uploader/document-uploader.component';

const routes: Routes = [ 
  { path: 'upload', component: DocumentUploaderComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
