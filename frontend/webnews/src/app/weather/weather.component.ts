import { Component, OnInit, OnDestroy } from '@angular/core';
import { WeatherService } from './weather.service';
import { IpStoreService } from '../stores/ip.store.service';
import { Weather } from './weather';
import { takeUntil } from 'rxjs/operators';
import { Subject } from 'rxjs';

@Component({
  selector: 'app-weather',
  templateUrl: './weather.component.html',
  styleUrls: ['./weather.component.css']
})
export class WeatherComponent implements OnInit, OnDestroy {

  private currentIP: any;
  MyWeather: Weather;
  destroy$: Subject<boolean> = new Subject<boolean>();

  constructor(public weatherService: WeatherService, public ipStoreService: IpStoreService) { }

  ngOnInit(): void {
    this.ipStoreService.currentIP$.subscribe(newIP => {
      this.currentIP = newIP;
      console.log('Current IP is', this.currentIP);
      if (this.currentIP.ip !== null) {
        this.weatherService.GetWeather(this.currentIP).pipe(takeUntil(this.destroy$)).subscribe(data => {
          this.MyWeather = data;
          console.log('Weather is', this.MyWeather);
        });
      }
    });
  }

  ngOnDestroy() {
    this.destroy$.next(true);
    this.destroy$.unsubscribe();
  }

}
