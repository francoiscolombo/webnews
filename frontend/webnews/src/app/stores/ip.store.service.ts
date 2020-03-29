import { Injectable } from '@angular/core';
import { Observable, BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class IpStoreService {

  private _currentIP: BehaviorSubject<any>;

  constructor() {
    this._currentIP = new BehaviorSubject({
      ip: null
    });
  }

  get currentIP$(): Observable<any> {
    return this._currentIP.asObservable();
  }

  get currentIP(): any {
    return this._currentIP.value;
  }

  set currentIP(newIP: any) {
    this._currentIP.next(newIP);
  }

}
