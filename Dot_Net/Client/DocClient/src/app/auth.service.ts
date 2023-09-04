// auth.service.ts
import { Injectable } from '@angular/core';
import { ApiService } from './api.service';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private readonly USERNAME_KEY = 'user';
  private readonly USERPASS_KEY = '#$$%456';

  constructor(private apiservice:ApiService){
  }

  login(username: string, password: string): boolean {
    // Simulate authentication logic (replace with actual authentication)
    this.apiservice.login(username,password).subscribe(
      (data) => 
      {
        sessionStorage.setItem(this.USERNAME_KEY, username);
        sessionStorage.setItem(this.USERPASS_KEY, password);
        return true;
      },
      (error) => {
        console.error('Error fetching documents:', error);
      });

    // if (username === 'admin' && password === 'admin') {
    //   // Store the user in session storage
    //   sessionStorage.setItem(this.USERNAME_KEY, username);
    //   sessionStorage.setItem(this.USERPASS_KEY, password);
    //   return true;
    // }
    return false;
  }

  isAuthenticated(): boolean {
    // Check if a user is stored in session storage
    return !!sessionStorage.getItem(this.USERNAME_KEY);
  }
}
