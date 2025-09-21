import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms'; 
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-login',
  imports: [CommonModule, FormsModule],
  templateUrl: './login.html',
  styleUrls: ['./login.scss']
})
export class LoginComponent {
  credentials = {
    email: '',
    contrasena: ''
  };

  constructor(private router: Router) {}

  onLogin() {
    if (this.credentials.email && this.credentials.contrasena) {
      console.log('Login exitoso:', this.credentials);
      this.router.navigate(['/profile']);
    }
  }
}
