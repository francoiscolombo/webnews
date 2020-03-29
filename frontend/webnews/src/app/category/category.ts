import { News } from './news';

export class Category {
  id: number;
  title: string;
  primary: News;
  news: News[];
}
