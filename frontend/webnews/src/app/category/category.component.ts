import { Component, OnInit, OnDestroy } from '@angular/core';
import { CategoryService } from './category.service';
import { Category } from './category';
import { takeUntil } from 'rxjs/operators';
import { Subject } from 'rxjs';

@Component({
  selector: 'app-category',
  templateUrl: './category.component.html',
  styleUrls: ['./category.component.css']
})
export class CategoryComponent implements OnInit, OnDestroy {

  MyCategories: Category[];
  destroy$: Subject<boolean> = new Subject<boolean>();

  constructor(public categoryService: CategoryService) { }

  ngOnInit(): void {
    this.categoryService.GetCategories().pipe(takeUntil(this.destroy$)).subscribe(data => {
      this.MyCategories = data;
      console.log('Categories is', this.MyCategories);
    });
  }

  ngOnDestroy() {
    this.destroy$.next(true);
    this.destroy$.unsubscribe();
  }

}
