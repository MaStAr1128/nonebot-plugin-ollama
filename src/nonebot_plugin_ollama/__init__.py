from requests import *
from nonebot import on_message, on_command
from nonebot.adapters import Bot, Event
from nonebot.rule import to_me
from nonebot.plugin import PluginMetadata
from nonebot import get_plugin_config
from .config import Config
from nonebot_plugin_userinfo import get_user_info
from datetime import datetime
import re

__plugin_meta__ = PluginMetadata(
    name="nonebot-plugin-ollama",
    description="连接你的本地ollama模型",
    usage="@你的bot对话即可",
    type="application",
    config=Config,
    homepage="https://github.com/MaStAr1128/nonebot-plugin-ollama"
)

def getGroupID(s):
    match = re.search(r'\d+', s)
    if match:
        id = match.group()
        return id
    return None

plugin_config = get_plugin_config(Config).ollama

group = plugin_config.listening

cmd = plugin_config.cmd

index = 0x0d000721

messages = [[ None for _ in range(0) ] for _ in range(len(group))]

doRec = True

doServe = False

# 聊天

rec = on_message(priority=plugin_config.min_priority+3, block=False)
@rec.handle()
async def main(bot=Bot, event=Event):
    doServe = False
    msg= str(event.get_message())
    user_info = await get_user_info(bot, event, event.get_user_id())
    userID = user_info.user_name

    now = datetime.now()
    formatted_now = now.strftime("[%Y-%m-%d %H:%M:%S] ")

    groupID = getGroupID(str(event.get_session_id()))

    for i in range(len(group)):
        if(group[i] == groupID):
            index = i
            doServe = True
    
    if(not doServe):
        return

    if(doRec):
        messages[index].append({
                "role": 'user',
                "content": formatted_now+userID + ": " + msg,
            })


ollama = on_command(cmd[0], aliases=set(cmd), priority=plugin_config.min_priority+2, block=False)
@ollama.handle()
async def ollama_handle(bot=Bot, event=Event):

    doRec = True

    doServe = False

    # 获取消息
    msg= str(event.get_message())

    for i in range(len(cmd)):
        msg = msg.replace(cmd[i], "", 1)

    groupID = getGroupID(str(event.get_session_id()))

    for i in range(len(group)):
        if(group[i] == groupID):
            index = i
            doServe = True

    if(not doServe):
        return

    # 判断是否达到记录上限
    if len(messages[index]) >= plugin_config.max_histories:
        del messages[index][0]
    
    # 向ollama发送请求
    else:
        user_info = await get_user_info(bot, event, event.get_user_id())
        userID = user_info.user_name

        now = datetime.now()
        formatted_now = now.strftime("[%Y-%m-%d %H:%M:%S] ")
        
        if(doRec):
            messages[index].append({
                "role": 'user',
                "content": formatted_now+userID + ": " + msg,
            })
            doRec = False

        parameters = {
            "model": plugin_config.model,
            "messages": messages[index],
            "stream": False,
        }

        response = post(plugin_config.url+'api/chat', json=parameters)
        if response.status_code == 200:
            await ollama.send(response.json()["message"]["content"])
            messages[index].append(response.json()["message"])
            doRec = False
        else:
            await ollama.send(f"Error: {response.status_code}")
