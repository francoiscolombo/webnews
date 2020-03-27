import { Component, OnInit, OnDestroy } from '@angular/core';
import { TopStoryService } from './top-stories.service';
import { TopStory } from './top-stories';
import { takeUntil } from 'rxjs/operators';
import { Subject } from 'rxjs';

@Component({
  selector: 'app-top-stories',
  templateUrl: './top-stories.component.html',
  styleUrls: ['./top-stories.component.css']
})
export class TopStoriesComponent implements OnInit, OnDestroy {

  MyTopStories: TopStory[];
  destroy$: Subject<boolean> = new Subject<boolean>();

  constructor(public topStoryService: TopStoryService) { }

  ngOnInit(): void {
    this.topStoryService.GetTopStories().pipe(takeUntil(this.destroy$)).subscribe(data => {
      this.MyTopStories = data;
      console.log('TopStories is', this.MyTopStories);
    });
  }

  ngOnDestroy() {
    this.destroy$.next(true);
    this.destroy$.unsubscribe();
  }

}
