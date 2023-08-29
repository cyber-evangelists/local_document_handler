import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-document-uploader',
  templateUrl: './document-uploader.component.html',
  styleUrls: ['./document-uploader.component.css']
})
export class DocumentUploaderComponent {
  docName: any
  docPath: any
  
  constructor(private http: HttpClient) { }
  
  onFileSelected(event: any) {
    const file: File = event.target.files[0];
    this.docName = file.name;
    this.docPath = URL.createObjectURL(file);
  }
  
  uploadDocument() {
    this.http.get(this.docPath, { responseType: 'arraybuffer' })
      .subscribe(response => {
        const byteArray = new Uint8Array(response);
        this.saveToDatabase(byteArray);
      });
  }
  

  saveToDatabase(byteArray: Uint8Array) {
    const apiUrl = 'https://localhost:7151/api/Documents/UploadDocument'; // Replace with your API endpoint
    const requestData = {
      Name: this.docName,
      Path:"C:/TempFiles/" + this.docName,
      Data: this.arrayBufferToBase64(byteArray),
    };

    
    
    this.http.post(apiUrl, requestData).subscribe(
      () => {
        console.log('Document saved to the database');
      },
      error => {
        console.error('Error saving document:', error);
      }
    );
  }

  arrayBufferToBase64(buffer: Iterable<number>) {
    let binary = '';
    const bytes = new Uint8Array(buffer);
    for (let i = 0; i < bytes.length; i++) {
        binary += String.fromCharCode(bytes[i]);
    }
    return window.btoa(binary);
}
}
