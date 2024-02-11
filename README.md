# Travel Bonds App BackEnd API

- Qiita ハッカソン 2024 (2024/2/10〜2/11) に参加した際に開発した作品

## App 概要

1. AI コンシェルジュが、あなたの現在位置(GPS)情報と、好みの場所のタイプから、距離的に近いおすすめスポットを提案してくれます。

2. この Repository は、現在位置の周辺のおすすめ遊び場・スポット提案 Web App の BackEnd-API の Repository

## 環境構築方法(初期 setup)

<br>

### 0. 前提条件

- .env の OPENAI_KEY に OpenAI の API Key が必要

### 1. DockerNetwork を作成する

- [F-E] と [B-E]の Docker Compose 間で、通信するための共通の Network を作成しておきます。

- `docker network create` コマンドで、独自の Network を作成することができます。

```bash
docker network create travel-bonds-network
```

- `docker network ls` コマンドで、Docker Network の一覧を確認することができます。

```bash
docker network ls
```

### 2. Docker Image の Build & Docker Container の起動

- Docker Image のビルド と コンテナの実行を実施します。

```bash
docker-compose up --build
```
