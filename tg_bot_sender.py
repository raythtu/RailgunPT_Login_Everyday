# tg_bot_sender.py
import requests
import json
from typing import Optional, Dict, Any, List, Union

class TgBotSender:
    """
    Telegram Bot 消息发送工具类
    """
    
    def __init__(self, bot_token: str):
        """
        初始化 TgBotSender
        
        Args:
            bot_token (str): Telegram Bot 的 token
        """
        self.bot_token = bot_token
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
    
    def send_message(self, chat_id: Union[int, str], text: str, 
                     parse_mode: Optional[str] = None,
                     disable_web_page_preview: bool = False,
                     disable_notification: bool = False,
                     reply_to_message_id: Optional[int] = None,
                     allow_sending_without_reply: bool = True) -> Dict[str, Any]:
        """
        发送文本消息
        
        Args:
            chat_id: 聊天ID，可以是用户ID、群组ID或频道ID
            text: 消息文本
            parse_mode: 解析模式，可选 'Markdown', 'MarkdownV2', 'HTML'
            disable_web_page_preview: 是否禁用网页预览
            disable_notification: 是否静默发送
            reply_to_message_id: 回复的消息ID
            allow_sending_without_reply: 未找到回复消息时是否正常发送
            
        Returns:
            dict: API 响应结果
        """
        url = f"{self.base_url}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": text,
            "disable_web_page_preview": disable_web_page_preview,
            "disable_notification": disable_notification,
            "allow_sending_without_reply": allow_sending_without_reply
        }
        
        if parse_mode:
            data["parse_mode"] = parse_mode
            
        if reply_to_message_id:
            data["reply_to_message_id"] = reply_to_message_id
            
        response = requests.post(url, json=data)
        return response.json()
    
    def send_photo(self, chat_id: Union[int, str], photo: Union[str, bytes],
               caption: Optional[str] = None,
               parse_mode: Optional[str] = None,
               disable_notification: bool = False,
               reply_to_message_id: Optional[int] = None) -> Dict[str, Any]:
        """
        发送图片消息
        
        Args:
            chat_id: 聊天ID
            photo: 图片URL、文件ID或文件对象
            caption: 图片说明文字
            parse_mode: 解析模式
            disable_notification: 是否静默发送
            reply_to_message_id: 回复的消息ID
            
        Returns:
            dict: API 响应结果
        """
        url = f"{self.base_url}/sendPhoto"
        data = {
            "chat_id": chat_id,
            "disable_notification": disable_notification
        }
        
        if caption:
            data["caption"] = caption
            
        if parse_mode:
            data["parse_mode"] = parse_mode
            
        if reply_to_message_id:
            data["reply_to_message_id"] = reply_to_message_id
        
        # 如果photo是文件对象，使用multipart/form-data上传
        if hasattr(photo, 'read') or (isinstance(photo, str) and photo.startswith('./')):
            if isinstance(photo, str):
                with open(photo, 'rb') as f:
                    files = {'photo': f}
                    response = requests.post(url, data=data, files=files)
            else:
                files = {'photo': photo}
                response = requests.post(url, data=data, files=files)
        else:
            # 如果是URL或file_id
            data['photo'] = photo
            response = requests.post(url, json=data)
            
        return response.json()

    
    def send_document(self, chat_id: Union[int, str], document: str,
                      caption: Optional[str] = None,
                      parse_mode: Optional[str] = None,
                      disable_notification: bool = False,
                      reply_to_message_id: Optional[int] = None) -> Dict[str, Any]:
        """
        发送文档
        
        Args:
            chat_id: 聊天ID
            document: 文件URL或文件ID
            caption: 文件说明文字
            parse_mode: 解析模式
            disable_notification: 是否静默发送
            reply_to_message_id: 回复的消息ID
            
        Returns:
            dict: API 响应结果
        """
        url = f"{self.base_url}/sendDocument"
        data = {
            "chat_id": chat_id,
            "document": document,
            "disable_notification": disable_notification
        }
        
        if caption:
            data["caption"] = caption
            
        if parse_mode:
            data["parse_mode"] = parse_mode
            
        if reply_to_message_id:
            data["reply_to_message_id"] = reply_to_message_id
            
        response = requests.post(url, json=data)
        return response.json()
    
    def get_me(self) -> Dict[str, Any]:
        """
        获取Bot信息
        
        Returns:
            dict: Bot信息
        """
        url = f"{self.base_url}/getMe"
        response = requests.get(url)
        return response.json()
    
    def get_updates(self, offset: Optional[int] = None, 
                    limit: int = 100, 
                    timeout: int = 0) -> Dict[str, Any]:
        """
        获取更新消息
        
        Args:
            offset: 更新ID偏移量
            limit: 返回更新数量限制
            timeout: 超时时间
            
        Returns:
            dict: 更新消息列表
        """
        url = f"{self.base_url}/getUpdates"
        params = {
            "limit": limit,
            "timeout": timeout
        }
        
        if offset:
            params["offset"] = offset
            
        response = requests.get(url, params=params)
        return response.json()


def send_message_simple(bot_token: str, chat_id: Union[int, str], text: str) -> Dict[str, Any]:
    """
    简单发送消息函数（无需创建类实例）
    
    Args:
        bot_token: Bot token
        chat_id: 聊天ID
        text: 消息文本
        
    Returns:
        dict: API响应结果
    """
    sender = TgBotSender(bot_token)
    return sender.send_message(chat_id, text)


# 使用示例
if __name__ == "__main__":
    # 替换为你的 Bot Token 和 Chat ID
    BOT_TOKEN = "xxxxxxxx"
    CHAT_ID = "yyyyyy"
    
    # 创建发送器实例
    bot = TgBotSender(BOT_TOKEN)
    
    # 发送简单文本消息
    #result = bot.send_message(CHAT_ID, "Hello from Python!")
    # 修改您的代码如下：
    with open("captcha.png", "rb") as image_file:
        #files = {"photo": image_file}
        result = bot.send_photo(CHAT_ID, image_file)

    print("消息发送结果:", result)