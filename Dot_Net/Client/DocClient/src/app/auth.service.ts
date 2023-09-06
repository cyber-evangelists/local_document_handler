// auth.service.ts
import { Injectable } from '@angular/core';
import { ApiService } from './api.service';
import { BlockGroup } from '@angular/compiler';
import { Observable, catchError, map, of } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
// class status{
//   status:string | undefined;
// }
export class AuthService {
  private readonly USERNAME_KEY = 'user';
  private readonly USERPASS_KEY = '#$$%456';

  constructor(private apiservice:ApiService){
  }

  login(username: string, password: string) {
    // Simulate authentication logic (replace with actual authentication)
     this.apiservice.login(username, password).subscribe(
      (data) => {
        if (data.status == 'login sucessfull') {
          sessionStorage.setItem(this.USERNAME_KEY, username);
          sessionStorage.setItem(this.USERPASS_KEY, password);
        }
      },
      (error) => {
        console.error('Error fetching documents:', error);
      } 
      );
  }
  
  

  isAuthenticated(): boolean {
    // Check if a user is stored in session storage
    return !!sessionStorage.getItem(this.USERNAME_KEY);
  }
}
