import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { AuthService } from '../../core/auth';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './login.html',
  styleUrls: ['./login.scss'],
})
export class LoginComponent {
  credentials = {
    email: '',
    contrasena: '',
  };

  errorMessage: string | null = null;

  constructor(private authService: AuthService, private router: Router) {}

  onLogin(): void {
    if (!this.credentials.email || !this.credentials.contrasena) {
      this.errorMessage = 'Por favor completa todos los campos';
      return;
    }

    this.authService.login(this.credentials).subscribe({
      next: (res) => {
        console.log('Respuesta del backend en login:', res); // 👀 imprime toda la respuesta
        this.authService.saveToken(res.token);

        console.log(
          'Token guardado en localStorage:',
          this.authService.getToken()
        ); // 👀 verifica token
        this.router.navigate(['/user/profile']);
      },
      error: (err) => {
        console.error('Error en login:', err);
        this.errorMessage = 'Credenciales incorrectas';
      },
    });
  }
}
