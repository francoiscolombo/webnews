import { Injectable } from '@angular/core';
import { Observable, BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PageStoreService {

  private _currentPage: BehaviorSubject<any>;

  constructor() {
    this._currentPage = new BehaviorSubject({
      page: 1
    });
  }

  get currentPage$(): Observable<any> {
    return this._currentPage.asObservable();
  }

  get currentPage(): any {
    return this._currentPage.value;
  }

  set currentPage(newPage: any) {
    this._currentPage.next(newPage);
  }

}
