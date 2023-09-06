// login.component.ts
import { Component } from '@angular/core';
import { AuthService } from '../auth.service';
import { Route, Router } from '@angular/router';
import { AppComponent } from '../app.component';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
})
export class LoginComponent {
  username = '';
  password = '';
  error='';
  private readonly USERNAME_KEY = 'user';

  constructor(private authService: AuthService,
    private router : Router) {}

  onSubmit(): void {
    // this.authService.login(this.username, this.password).subscribe((resp)=>{
    //   if(resp){
    //     console.log(resp);
    //     this.router.navigate(['/home']);
    //   }
    //   else{
    //     this.error ='Login failed';

    //   }
    // });
    if(this.username != '' && this.password != '')
    {
      if (this.isAuthenticated()) {
        console.log('Login successful');
        this.router.navigate(['/home']);
        
      } else {
        this.error ='Login failed';
      }
    }
  }

  isAuthenticated(): boolean {
    // Check if a user is stored in session storage
    this.authService.login(this.username, this.password);
    console.log(sessionStorage.getItem(this.USERNAME_KEY));
    return !!sessionStorage.getItem(this.USERNAME_KEY);
  }
}
