import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormGroup, FormControl, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../core/auth';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-perfil-form',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule],
  templateUrl: './perfil-form.html',
  styleUrls: ['./perfil-form.scss']
})
export class PerfilFormComponent implements OnInit {
  perfilForm: FormGroup;
  errorMessage: string | null = null;
  successMessage: string | null = null;
  loading = true;
  updating = false;

  private apiUrl = 'http://localhost:5000/api';

  constructor(private authService: AuthService, private http: HttpClient, private router: Router) {
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

    // Traer perfil existente
    this.http.get<any>(`${this.apiUrl}/perfil`, {
      headers: { Authorization: `Bearer ${token}` }
    }).subscribe({
      next: (data) => {
        if (data.perfil) {
          this.perfilForm.patchValue(data.perfil);
          this.updating = true; 
        }
        this.loading = false;
      },
      error: (err) => {
        console.error('Error cargando perfil:', err);
        this.loading = false;
      }
    });
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
      ? this.http.put(`${this.apiUrl}/perfil`, this.perfilForm.value, { headers: { Authorization: `Bearer ${token}` } })
      : this.http.post(`${this.apiUrl}/perfil`, this.perfilForm.value, { headers: { Authorization: `Bearer ${token}` } });

    request$.subscribe({
      next: (res: any) => {
        this.successMessage = res.mensaje;
        this.errorMessage = null;
        if (!this.updating) {
          this.updating = true; 
        }
      },
      error: (err) => {
        console.error('Error guardando perfil:', err);
        this.errorMessage = err.error?.error || 'Error al guardar el perfil.';
        this.successMessage = null;
      }
    });
  }
}
