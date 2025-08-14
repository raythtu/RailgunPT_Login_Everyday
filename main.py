import os
from playwright.sync_api import Playwright, sync_playwright, expect

##################
# 猴子补法
###############
import PIL.Image
if not hasattr(PIL.Image, 'ANTIALIAS'):
    from PIL.Image import Resampling
    PIL.Image.ANTIALIAS = Resampling.LANCZOS  # 使用现代替代方法

import ddddocr
from tg_bot_sender import TgBotSender


PTUSERNAME = os.environ.get('PTUSERNAME')
PTPASSWORD = os.environ.get('PTPASSWORD')

BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')



if not BOT_TOKEN:
    print("请设置环境变量 BOT_TOKEN")
    exit(1)

if not CHAT_ID:
    print("请设置环境变量 CHAT_ID")
    exit(1)

if not PTUSERNAME or not PTPASSWORD:
    print("请设置环境变量 PTUSERNAME 和 PTPASSWORD")
    exit(1)



bot = TgBotSender(BOT_TOKEN)


def myocr(img_path):
    with open(img_path, 'rb') as f:
        img_bytes = f.read()
    ocr = ddddocr.DdddOcr()
    res = ocr.classification(img_bytes)
    return res


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(
        headless=True,
        slow_mo=1000
    )
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://audiences.me/login.php", timeout=0)
    page.locator("input[name=\"username\"]").fill(PTUSERNAME)
    print("已输入用户名")
    page.locator("input[name=\"password\"]").fill(PTPASSWORD)
    print("已输入密码:%s")
    page.wait_for_timeout(3000)
    page.get_by_role("img", name="CAPTCHA").screenshot(path="captcha.png")
    ocr_res = myocr("captcha.png")
    print("识别的图片验证码为：", ocr_res)
    page.locator("input[name=\"imagestring\"]").screenshot(path="captcha.png")
    page.locator("input[name=\"imagestring\"]").fill(ocr_res)
    page.locator("input[name=\"logout\"]").check()
    page.get_by_role("button", name="登录").click()
    print("已点击登录")
    page.goto("https://audiences.me/index.php")
    page.wait_for_timeout(3000)
    #page.pause()
    page.goto("https://audiences.me/attendance.php")
    page.wait_for_timeout(3000)
    page.query_selector("签到已得")
    print(page.get_by_text("签到已得"))
    if page.get_by_text("签到已得").is_visible():
        print("已签到")
        bot.send_message(CHAT_ID, "RailgunPT 今天已经签到过了～")
    else:
        print("未签到")
        page.get_by_role("link", name="[签到得魔力]").click()
        bot.send_message(CHAT_ID, "RailgunPT 已签到")
    page.screenshot(path="qmsg.png")

    with open("qmsg.png", "rb") as image_file:
        #files = {"photo": image_file}
        bot.send_photo(CHAT_ID, image_file)


    page.get_by_role("link", name="退出").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
