import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthResponse } from './models/auth-response.model';
import { User } from './models/user.model';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private apiUrl = 'http://localhost:5000/api';

  constructor(private http: HttpClient) {}

  // Registro
  register(userData: Partial<User>): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${this.apiUrl}/registro`, userData);
  }

  // Login
  login(credentials: { email: string; contrasena: string }): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${this.apiUrl}/login`, credentials);
  }

  // Obtener perfil completo
  getProfile(): Observable<any> {
    const token = this.getToken();
    return this.http.get<any>(`${this.apiUrl}/perfil`, {
      headers: { Authorization: `Bearer ${token}` },
    });
  }

  // Crear perfil
  createProfile(perfil: any): Observable<any> {
    const token = this.getToken();
    return this.http.post<any>(`${this.apiUrl}/perfil`, perfil, {
      headers: { Authorization: `Bearer ${token}` },
    });
  }

  // Actualizar perfil
  updateProfile(perfil: any): Observable<any> {
    const token = this.getToken();
    return this.http.put<any>(`${this.apiUrl}/perfil`, perfil, {
      headers: { Authorization: `Bearer ${token}` },
    });
  }

  // Logout
  logout(): void {
    localStorage.removeItem('token');
  }

  // Guardar token
  saveToken(token: string): void {
    localStorage.setItem('token', token);
  }

  // Obtener token
  getToken(): string | null {
    return localStorage.getItem('token');
  }

  // Comprobar sesión activa
  isLoggedIn(): boolean {
    return !!this.getToken();
  }
}
