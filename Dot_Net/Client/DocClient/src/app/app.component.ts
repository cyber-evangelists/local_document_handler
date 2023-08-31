import { Component } from '@angular/core';
import { DocumentServiceService } from './document-service.service';
import { Router } from '@angular/router';
import { ApiService } from './api.service';
import { saveAs } from 'file-saver';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'DocClient';

  documents: any[] = [];

  constructor(private documentService: DocumentServiceService,
    private apiService :ApiService,
    private router: Router) { }

  ngOnInit(): void {
    this.apiService.getFiles().subscribe(
      (data) => {
        this.documents = data;
        console.log(this.documents);
      },
      (error) => {
        console.error('Error fetching documents:', error);
      }
    );
  }

  navigateToUpload() {
    this.router.navigate(['/upload']);
  }

  Download(docName:string)
  {
    this.apiService.getFile(docName).subscribe((response: any) => {
      console.log(response);
      this.saveFile(response, docName); // Adjust file name and extension as needed
    },
   (error)=> {
    console.error('Error Downloading:', error);
}    
    );}

private saveFile(data: any, fileName: string) {
  const blob = new Blob([data], { type: 'application/octet-stream' });
  const url = window.URL.createObjectURL(blob);

  const a = document.createElement('a');
  a.href = url;
  a.download = fileName;
  a.click();

  window.URL.revokeObjectURL(url); 
}

}
