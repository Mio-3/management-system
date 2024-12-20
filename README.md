# アルバイトシフト管理アプリ

**※現在も開発中**

## 進捗
<img width="900" alt="スクリーンショット スクリーンショット 2024-11-18 3.24.08.png" src="https://github.com/user-attachments/assets/29a52df8-061c-4ec4-9e35-f4a5e8122510">
<img width="900" src= "https://github.com/user-attachments/assets/d0e86634-feb8-4bf7-9810-e3c53feb33cb">
<img width="1402" alt="スクリーンショット 2024-12-20 22 03 30" src="https://github.com/user-attachments/assets/11c93ec5-a5ea-4ecd-b525-9962e0bd403f" />

FastAPIがSwagger UIを自動で生成してくれるのが非常に助かる...


# URL

## 開発の背景
私のアルバイト先のシフト提出方法が以下の問題点を抱えていました。
- シフト提出がお店のカレンダーに記載する方法のため、お店にいる時しかシフト提出ができない **利便性** に関する問題
- シフト提出を忘れてしまった際に、お互いに負担がかかってしまう問題

これらの問題をWEBアプリ開発によって、解決できないのではないのか？と考え、開発を決意いたしました。


## 使用技術
- TypeScript   5.5.2
- Next.js   14.2.4
- React   18.3.1
- Tailwind CSS   3.4.4
- Material-UI   5.15.21
- Python   3.11.5
- FastAPI
- Strawberry GraphQL
- MongoDB
- Docker  26.1.1
- Docker-Compose v2.27.0-desktop.2
- FullCalendar
- Nagar Date Public Holiday API

### 開発期間
2024年07月~現在まで

## 役割
**個人開発**

企画、ヒアリング調査、要件定義、社長への企画提案、画面設計、開発


# 機能一覧
## 現時点で実装した機能
- カレンダー表示機能
- シフト申請フォーム機能
- レスポンシブ対応(スマホ、PC)
- 日本の祝日表示機能(Web API使用)
- レイアウト構成(Material-UI)
- 認証処理(GraphQL)

## 実装予定の機能
- 認証機能(従業員ID、パスワード)
- シフト提出のAPI開発
- 従業員一覧画面
- デプロイ