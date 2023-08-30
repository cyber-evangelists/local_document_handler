import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpResponse } from '@angular/common/http';
import { Observable, catchError, throwError } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DocumentServiceService {

  private baseUrl = 'https://localhost:7151/api/Documents'; // Replace with your API endpoint

  constructor(private http: HttpClient) {}

  getDocuments(): Observable<any> {
    return this.http.get(this.baseUrl);
  }

  saveDocument(documentPath: string): Observable<void> {
    return this.http.post<void>(`${this.baseUrl}/saveDocument`, { documentPath });
  }

  downloadDocument(docId: number) {
    const apiUrl = `${this.baseUrl}/DownloadDocument`;
    return this.http.get(apiUrl+`?DocId=${docId}`, { responseType: 'arraybuffer' });
  }
}
