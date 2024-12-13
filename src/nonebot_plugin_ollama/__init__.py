from requests import *
from nonebot import on_message
from nonebot.adapters import Bot, Event
from nonebot.rule import to_me
from nonebot.plugin import PluginMetadata
from nonebot import get_plugin_config
from .config import Config

__plugin_meta__ = PluginMetadata(
    name="nonebot-plugin-ollama",
    description="连接你的本地ollama模型",
    usage="@你的bot对话即可",
    type="application",
    config=Config,
    homepage="https://github.com/MaStAr1128/nonebot-plugin-ollama"
)

plugin_config = get_plugin_config(Config).ollama

ollama = on_message(priority=plugin_config.priority, block=False, rule=to_me())
@ollama.handle()
async def ollama_handle(bot=Bot, event=Event):

    msg= str(event.get_message())

    parameters = {
        "model": plugin_config.model,
        "messages": [
            {
                "role": 'user',
                "content": msg,
            }
        ],
        "stream": False,
    }

    response = post(plugin_config.url+'api/chat', json=parameters)
    if response.status_code == 200:
        await ollama.send(response.json()["message"]["content"])
    else:
        await ollama.send(f"Error: {response.status_code}")