import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  private baseUrl = 'http://localhost:5000'; // Update with your API URL
  private readonly USERNAME_KEY = 'user';
  private readonly USERPASS_KEY = '#$$%456';

  username: any;
  password: any;

  constructor(private http: HttpClient) {
    const name = sessionStorage.getItem(this.USERNAME_KEY);
    const pass =  sessionStorage.getItem(this.USERNAME_KEY);
    if(name != null && pass != null)
    {
        this.username = name;
        this.password = pass;
    }
  }

  login(username:string,password:string): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
    });
    const body = {
      username: username,
      password: password,
    };
    
    return this.http.post(`${this.baseUrl}/login`, body, { headers });
  }

  uploadFile(file: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('username', this.username);
    formData.append('password', this.password);

    return this.http.post(`${this.baseUrl}/upload_file`, formData);
  }

  getFile(filename: string): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
    });

    const body = {
      username: this.username,
      password: this.password,
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
      username: this.username,
      password: this.password,
    };

    return this.http.post(`${this.baseUrl}/getfiles`,body, { headers });
  }
}
