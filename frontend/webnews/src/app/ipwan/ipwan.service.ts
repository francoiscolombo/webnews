import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { IpWan } from './ipwan';
import { Observable, throwError } from 'rxjs';
import { retry, catchError } from 'rxjs/operators';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})

export class IpWanService {

  private baseUrl = environment.baseURL;

  constructor(private http: HttpClient) { }

  // Http Headers
  private httpOptions = {
    headers: new HttpHeaders({
      'Access-Control-Allow-Origin': '*',
      'Content-Type': 'application/json',
      'application': environment.appName,
      'token': environment.token
    })
  };

  // GET my IP
  GetIpWan(): Observable<IpWan> {
    return this.http.get<IpWan>('https://api6.ipify.org?format=json')
    .pipe(
      retry(1),
      catchError(this.errorHandler)
    );
  }

  // Initialize the weather API with my IP
  UpdateWeather(data): Observable<IpWan> {
    console.log('inside update weather, data is ', data);
    return this.http.put<IpWan>(this.baseUrl + 'weather', JSON.stringify(data), this.httpOptions)
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
