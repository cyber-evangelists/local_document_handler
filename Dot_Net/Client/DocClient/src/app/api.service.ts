import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  private baseUrl = 'https://b334-223-123-4-243.ngrok-free.app'; // Update with your API URL

  constructor(private http: HttpClient) {}

  login(): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
    });

    const body = {
      username: 'admin',
      password: 'admin',
    };

    return this.http.post(`${this.baseUrl}/login`, body, { headers });
  }

  uploadFile(file: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('username', 'admin');
    formData.append('password', 'admin');

    return this.http.post(`${this.baseUrl}/upload_file`, formData);
  }

  getFile(filename: string): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
    });

    const body = {
      username: 'admin',
      password: 'admin',
      filename: filename,
    };
    const options = {
      headers,
      responseType: 'blob' as 'json',
    };

    return this.http.post(`${this.baseUrl}/get_file`, body, options);
  }

  getFiles(): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json', // Set the appropriate content type
    });

    const body = {
      username: 'admin',
      password: 'admin',
    };

    return this.http.post(`${this.baseUrl}/getfiles`,body, { headers });
  }
}
