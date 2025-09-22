import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { AuthService } from '../../core/auth';
import { User } from '../../core/models/user.model';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './profile.html',
  styleUrls: ['./profile.scss'],
})
export class ProfileComponent implements OnInit {
  user: User | null = null;
  loading = true;

  constructor(private authService: AuthService, private router: Router) {}

  ngOnInit(): void {
    console.log('Cargando perfil, token actual:', this.authService.getToken()); // 👀

    this.authService.getProfile().subscribe({
      next: (data: User) => {
        console.log('Perfil recibido del backend:', data); // 👀
        this.user = data;
        this.loading = false;
      },
      error: (err) => {
        console.error('Error al cargar el perfil:', err); // 👀 error detallado
        this.authService.logout();
        this.router.navigate(['/auth/login']);
      },
    });
  }

  onLogout(): void {
    this.authService.logout();
    this.router.navigate(['/auth/login']);
  }
}
