from requests import *
from nonebot import on_message, on_command
from nonebot.adapters import Bot, Event
from nonebot.rule import to_me
from nonebot.plugin import PluginMetadata
from nonebot import get_plugin_config
from .config import Config
from nonebot_plugin_userinfo import get_user_info
import re
from datetime import datetime
import numpy

__plugin_meta__ = PluginMetadata(
    name="nonebot-plugin-ollama",
    description="连接你的本地ollama模型",
    usage="@你的bot对话即可",
    type="application",
    config=Config,
    homepage="https://github.com/MaStAr1128/nonebot-plugin-ollama"
)

def getGroupID(s):
    # 使用正则表达式匹配第一个数字
    match = re.search(r'\d+', s)
    if match:
        # 提取第一个数字
        id = match.group()
        return id
    return None

plugin_config = get_plugin_config(Config).ollama

group = plugin_config.Listening

index = 0x0d000721

'''
for i in range(len(group)):
    exec(f"messages_{group[i]} = []")
'''
messages = [[ None for _ in range(0) ] for _ in range(len(group))]

doRec = True

doServe = False

'''
# 清空记录
ollamaClear = on_command(cmd="clear", priority=plugin_config.min_priority, block=True, rule=to_me())
@ollamaClear.handle()
async def ollamaClear_handle(bot=Bot, event=Event):
    messages.clear()
    await ollamaClear.send("System: 对话记录已清空.")
'''

# 聊天

'''[To Be Pictured]
ollama_pic = on_command("ATRI.pic()", aliases={"亚托莉.pic()", "萝卜子.pic()"}, priority=plugin_config.min_priority+1, block=False)
@ollama_pic.got("pic", prompt="没有图片诶...")
async def main(
    bot: Bot,
    event: Event,
    picture: Messages = Arg("pic")):

        # your code here...
'''

rec = on_message(priority=plugin_config.min_priority+3, block=False)
@rec.handle()
async def main(bot=Bot, event=Event):
    doServe = False
    msg= str(event.get_message())
    user_info = await get_user_info(bot, event, event.get_user_id())
    userID = ""

    if(user_info.user_id == "2058165181"):
        userID = "C9QuaRtz"
    elif(user_info.user_id == "2574652640"):
        userID = "TKMaStAr"
    elif(user_info.user_id == "3548801159"):
        userID = "爱丽丝"
    else:
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
        # await ollama.send("len: "+str(len(group))+"\nindex: "+str(index))
        messages[index].append({
                "role": 'user',
                "content": formatted_now+userID + ": “" + msg + "”",
            })


ollama = on_command("ATRI", aliases={"亚托莉", "萝卜子"}, priority=plugin_config.min_priority+2, block=False)
@ollama.handle()
async def ollama_handle(bot=Bot, event=Event):

    doRec = True

    doServe = False

    # 获取消息
    msg= str(event.get_message()).replace("ATRI ", "", 1).replace("亚托莉 ", "", 1).replace("萝卜子 ", "", 1)

    groupID = getGroupID(str(event.get_session_id()))

    for i in range(len(group)):
        if(group[i] == groupID):
            index = i
            doServe = True

    if(not doServe):
        return

    # 判断是否为空
    if msg == '':
        await ollama.send("啊咧？有什么事嘛((>ω< ))o")
    # 判断是否达到记录上限
    
    elif len(messages[index]) >= plugin_config.max_histories:
        del messages[index][0]
        # await ollama.send(f"Warning: 对话记录已达到{plugin_config.max_histories}条的上限，现已清空.")
    

    # 向ollama发送请求
    else:
        user_info = await get_user_info(bot, event, event.get_user_id())
        
        if(user_info.user_id == "2058165181"):
            userID = "C9QuaRtz"
        elif(user_info.user_id == "2574652640"):
            userID = "TKMaStAr"
        elif(user_info.user_id == "3548801159"):
            userID = "爱丽丝"
        else:
            userID = user_info.user_name

        now = datetime.now()
        formatted_now = now.strftime("[%Y-%m-%d %H:%M:%S] ")
        
        if(doRec):
            messages[index].append({
                "role": 'user',
                "content": formatted_now+userID + ": “" + msg + "”",
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
            # await ollama.send(str(user_info.user_id)+" | "+str(type(user_info.user_id)))
            await ollama.send(str(event.get_session_id()))
        else:
            await ollama.send(f"Error: {response.status_code}")