// recommendations.ts
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../core/auth';

@Component({
  selector: 'app-recommendations',
  standalone: true, 
  imports: [CommonModule],
  templateUrl: './recommendations.html',
  styleUrls: ['./recommendations.scss'],
})
export class RecommendationsComponent implements OnInit {
  recommendations: any = null;
  loading: boolean = true;
  error: string | null = null;

  constructor(private authService: AuthService) {}

  ngOnInit(): void {
    this.loadRecommendations();
  }

  // 🔹 Método público para refrescar
  loadRecommendations(): void {
    this.loading = true;
    this.error = null;

    this.authService.getRecommendations().subscribe({
      next: (data) => {
        this.recommendations = data;
        this.loading = false;
      },
      error: (err) => {
        console.error('Error al obtener recomendaciones:', err);
        this.error = 'No se pudieron cargar las recomendaciones.';
        this.loading = false;
      },
    });
  }
}
