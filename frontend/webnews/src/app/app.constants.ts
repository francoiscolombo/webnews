export class AppConstants {
    public static get baseURL(): string { return "http://localhost:5000/api/v1.0/"; }
    public static get appName(): string { return "fcwebnews.jobs"; }
    public static get token(): string { return "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcHBsaWNhdGlvbiI6MSwiZXhwaXJlcyI6MTYxNjQ1MDgxMS40Njg1NTgzfQ.IxLRidQCFLFwDQyObJc3VK5uEi5TKgxTrMh5cb8VAUE"; }
    public static get maxHeadlines(): number { return 3; }
    public static get categories(): string { return "Business,Entertainment,Health,Lifestyle,Politics,Technology,World"; }
}
