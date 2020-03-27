import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { WeatherComponent } from './weather/weather.component';
import { IpWanComponent } from './ipwan/ipwan.component';
import { CategoryComponent } from './category/category.component';
import { TopStoriesComponent } from './top-stories/top-stories.component';
import { LatestNewsComponent } from './latest-news/latest-news.component';

import { WeatherService } from './weather/weather.service';
import { IpWanService } from './ipwan/ipwan.service';
import { TopStoryService } from './top-stories/top-stories.service';
import { LatestNewsService } from './latest-news/latest-news.service';
import { CategoryService } from './category/category.service';
import { IpStoreService } from './stores/ip.store.service';
import { PageStoreService } from './stores/page.store.service';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { MatToolbarModule } from '@angular/material/toolbar';
import { MatTabsModule } from '@angular/material/tabs';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatRippleModule } from '@angular/material/core';

import { MatCarouselModule } from '@ngmodule/material-carousel';

@NgModule({
  declarations: [
    AppComponent,
    WeatherComponent,
    IpWanComponent,
    CategoryComponent,
    TopStoriesComponent,
    LatestNewsComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatToolbarModule,
    MatTabsModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatRippleModule,
    MatCarouselModule
  ],
  providers: [
    WeatherService,
    IpWanService,
    TopStoryService,
    LatestNewsService,
    CategoryService,
    IpStoreService,
    PageStoreService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
