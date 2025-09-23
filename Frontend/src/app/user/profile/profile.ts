import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormGroup, FormControl, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../core/auth';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule],
  templateUrl: './profile.html',
  styleUrls: ['./profile.scss'],
})
export class ProfileComponent implements OnInit {
  user: any = null;
  loading = true;

  showForm = false;
  perfilForm: FormGroup;
  errorMessage: string | null = null;
  successMessage: string | null = null;
  updating = false;

  private apiUrl = 'http://localhost:5000/api';

  constructor(private authService: AuthService, private router: Router) {
    this.perfilForm = new FormGroup({
      sexo: new FormControl('', Validators.required),
      edad: new FormControl('', [Validators.required, Validators.min(1)]),
      peso: new FormControl('', [Validators.required, Validators.min(1)]),
      altura: new FormControl('', [Validators.required, Validators.min(1)]),
      nivel_actividad: new FormControl('', Validators.required),
      objetivo: new FormControl('', Validators.required)
    });
  }

  ngOnInit(): void {
    const token = this.authService.getToken();
    if (!token) {
      this.router.navigate(['/auth/login']);
      return;
    }

    this.authService.getProfile().subscribe({
      next: (data: any) => {
        this.user = data.user || data;
        if (data.perfil) {
          this.perfilForm.patchValue(data.perfil);
          this.updating = true;
        }
        this.loading = false;
      },
      error: (err) => {
        console.error('Error cargando perfil:', err);
        this.authService.logout();
        this.router.navigate(['/auth/login']);
      }
    });
  }

  onLogout(): void {
    this.authService.logout();
    this.router.navigate(['/auth/login']);
  }

  toggleForm(): void {
    this.showForm = !this.showForm;
  }

  onSubmit(): void {
    if (this.perfilForm.invalid) {
      this.errorMessage = 'Por favor completa todos los campos correctamente.';
      return;
    }

    const token = this.authService.getToken();
    if (!token) {
      this.router.navigate(['/auth/login']);
      return;
    }

    const request$ = this.updating
      ? this.authService.updateProfile(this.perfilForm.value)
      : this.authService.createProfile(this.perfilForm.value);

    request$.subscribe({
      next: (res: any) => {
        this.successMessage = res.mensaje || 'Perfil guardado correctamente.';
        this.errorMessage = null;
        this.updating = true;
        // Actualizar datos visibles después de guardar
        this.user = { ...this.user, ...this.perfilForm.value };
        this.showForm = false;
      },
      error: (err) => {
        console.error('Error guardando perfil:', err);
        this.errorMessage = err.error?.error || 'Error al guardar el perfil.';
        this.successMessage = null;
      }
    });
  }
}
