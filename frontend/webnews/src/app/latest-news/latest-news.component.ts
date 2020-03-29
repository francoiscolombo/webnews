import { Component, OnInit, OnDestroy } from '@angular/core';
import { LatestNewsService } from './latest-news.service';
import { PageStoreService } from '../stores/page.store.service';
import { LatestNews } from './latest-news';
import { takeUntil } from 'rxjs/operators';
import { Subject } from 'rxjs';

@Component({
  selector: 'app-latest-news',
  templateUrl: './latest-news.component.html',
  styleUrls: ['./latest-news.component.css']
})
export class LatestNewsComponent implements OnInit, OnDestroy {

  private currentPage: any;
  MyLatestNews: LatestNews[];
  destroy$: Subject<boolean> = new Subject<boolean>();

  constructor(public latestNewsService: LatestNewsService, public pageStoreService: PageStoreService) { }

  ngOnInit(): void {
    this.pageStoreService.currentPage$.subscribe(newPage => {
      this.currentPage = newPage;
      console.log('Current Page is', this.currentPage);
      this.latestNewsService.GetLatestNews(this.currentPage.page).pipe(takeUntil(this.destroy$)).subscribe(data => {
        this.MyLatestNews = data;
        console.log('LatestNews is', this.MyLatestNews);
      });
    });
  }

  ngOnDestroy() {
    this.destroy$.next(true);
    this.destroy$.unsubscribe();
  }

  reloadNews() {
    this.currentPage.page = this.currentPage.page + 1;
    this.pageStoreService.currentPage = this.currentPage;
  }

}
