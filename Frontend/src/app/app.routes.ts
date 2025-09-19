import { Routes } from '@angular/router';
import { AuthGuard } from './core/guards/auth-guard';
import { LoginComponent } from './auth/login/login';
import { RegisterComponent } from './auth/register/register';
import { ProfileComponent } from './user/profile/profile';

export const routes: Routes = [
    {
        path: '',
        redirectTo: 'auth/login',
        pathMatch: 'full',
    },
    {
        path: 'auth',
        children: [
            { path: 'login', component: LoginComponent },
            { path: 'register', component: RegisterComponent },
        ],
    },
    {
        path: 'user',
        children: [
            {
                path: 'profile',
                component: ProfileComponent,
                canActivate: [AuthGuard], 
            },
        ],
    },
    {
        path: '**',
        redirectTo: 'auth/login', 
    },
];
