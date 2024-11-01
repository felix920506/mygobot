# 自行架設 mygobot

## 系統需求

如果想要運行 mygobot, 你需要以下的環境

- 網路連線
- Discord 帳號
- 一台電腦

電腦上需要安裝以下套件：

- [Python 3.12](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installation)

## 建立 Discord 應用

在架設之前，需要先建立 Discord 機器人帳號：

1. 前往 [Discord API 管理介面](https://discord.com/developers/docs/intro)
2. 登入後選擇左上角的 `Applications`
3. 選擇右上角的 `New Application`，輸入你想要的名稱，勾選同意，然後點 `Create`
4. 你會進入應用程式的管理介面，請選擇左邊的 `Bot` 頁面設定機器人的名稱和頭像
5. 往下把 `Public Bot` 關閉，然後打開 `Message Content Intent`
