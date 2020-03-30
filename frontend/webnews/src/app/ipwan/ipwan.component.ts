import { Component, OnInit, OnDestroy } from '@angular/core';
import { IpWanService } from './ipwan.service';
import { IpStoreService } from '../stores/ip.store.service';
import { IpWan } from './ipwan';
import { takeUntil } from 'rxjs/operators';
import { Subject } from 'rxjs';

@Component({
  selector: 'app-ipwan',
  templateUrl: './ipwan.component.html',
  styleUrls: ['./ipwan.component.css']
})

export class IpWanComponent implements OnInit, OnDestroy {

  MyIp: IpWan;
  destroy$: Subject<boolean> = new Subject<boolean>();

  constructor(public ipService: IpWanService, public ipStoreService: IpStoreService) { }

  ngOnInit(): void {
    this.ipService.GetIpWan().pipe(takeUntil(this.destroy$)).subscribe(data => {
      this.MyIp = data;
      this.ipStoreService.currentIP = data;
      console.log('IP is', this.MyIp);
      if (this.MyIp.ip !== null) {
        this.ipService.UpdateWeather(data).subscribe(res => {
          console.log('Response from update weather is', res);
        });
      }
    });
  }

  ngOnDestroy() {
    this.destroy$.next(true);
    this.destroy$.unsubscribe();
  }

}
