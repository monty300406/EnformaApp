import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthResponse } from './models/auth-response.model';  
import { User } from './models/user.model';    

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private apiUrl = 'http://localhost:5000/api'; // Flask API

  constructor(private http: HttpClient) {}

  // 🔹 Registro
  register(userData: Partial<User>): Observable<AuthResponse> {
    return this.http.post<AuthResponse>(`${this.apiUrl}/registro`, userData);
  }

  // 🔹 Login
  // auth.ts
login(credentials: { email: string; contrasena: string }): Observable<AuthResponse> {
  return this.http.post<AuthResponse>(`${this.apiUrl}/login`, credentials);
}


  // 🔹 Perfil
  getProfile(): Observable<User> {
    return this.http.get<User>(`${this.apiUrl}/perfil`);
  }

  // 🔹 Logout (solo borra token local)
  logout(): void {
    localStorage.removeItem('token');
  }

  // 🔹 Guardar token
  saveToken(token: string): void {
    localStorage.setItem('token', token);
  }

  // 🔹 Obtener token
  getToken(): string | null {
    return localStorage.getItem('token');
  }

  // 🔹 Validar si hay sesión
  isLoggedIn(): boolean {
    return !!this.getToken();
  }
}
