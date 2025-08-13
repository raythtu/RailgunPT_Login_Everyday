# RailgunPT 每日签到脚本

使用 Playwright 自动登录 RailgunPT 并完成每日签到任务。

## 功能特性
- 自动识别验证码登录
- 每日自动签到
- Telegram 消息通知
- 签到结果截图发送

## 环境变量配置
需要设置以下环境变量：
- PTUSERNAME: PT站点用户名
- PTPASSWORD: PT站点密码
- BOT_TOKEN: Telegram Bot Token
- CHAT_ID: Telegram 接收消息的 Chat ID

## 使用方法
1. 安装依赖：`pip install -r requirements.txt`
2. 安装 Playwright 浏览器：`playwright install chromium`
3. 设置环境变量
4. 运行脚本：`python main.py`