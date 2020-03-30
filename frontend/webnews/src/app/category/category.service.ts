import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Category } from './category';
import { Observable, throwError } from 'rxjs';
import { retry, catchError } from 'rxjs/operators';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})

export class CategoryService {

  private baseUrl = environment.baseURL;

  constructor(private http: HttpClient) { }

  // Http Headers
  private httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json',
      'application': environment.appName,
      'token': environment.token
    })
  };

  // GET the categories to display
  GetCategories(): Observable<Category[]> {
    return this.http.get<Category[]>(this.baseUrl + 'categories/' + environment.categories, this.httpOptions)
    .pipe(
      retry(1),
      catchError(this.errorHandler)
    );
  }

  // Error handling
  errorHandler(error) {
     let errorMessage = '';
     if (error.error instanceof ErrorEvent) {
       // Get client-side error
       errorMessage = error.error.message;
     } else {
       // Get server-side error
       errorMessage = `Error Code: ${error.status}\nMessage: ${error.message}`;
     }
     console.log(errorMessage);
     return throwError(errorMessage);
  }

}
