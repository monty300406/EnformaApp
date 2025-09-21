import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-register',
  imports: [CommonModule, FormsModule],
  templateUrl: './register.html',
  styleUrls: ['./register.scss']
})
export class RegisterComponent {
  user = {
    nombre: '',
    email: '',
    contrasena: ''
  };

  constructor(private router: Router) {}

  onRegister() {
    console.log('Usuario registrado:', this.user);
    this.router.navigate(['/auth/login']);
  }
}
