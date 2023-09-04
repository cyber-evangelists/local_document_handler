import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {

  isDisplay: boolean = false;
  constructor(private router: Router) {} 

  logout() {
    sessionStorage.removeItem('user'); 
  
    // Redirect to the login page
    this.router.navigate(['/login']);
  }
 
}
