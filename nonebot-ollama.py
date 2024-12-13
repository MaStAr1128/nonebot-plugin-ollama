from requests import *
from nonebot import on_message
from nonebot.adapters import Bot, Event
from nonebot.rule import to_me

ollama = on_message(priority=5, block=False, rule=to_me())
@ollama.handle()
async def ollama_handle(bot=Bot, event=Event):

    msg= str(event.get_message())
    model = 'qwen2.5:0.5b'
    url = 'http://127.0.0.1:11434/'
    parameters = {
        "model": model,
        "messages": [
            {
                "role": 'user',
                "content": msg,
            }
        ],
        "stream": False,
    }

    response = post(url+'api/chat', json=parameters)
    if response.status_code == 200:
        await ollama.send(response.json()["message"]["content"])
    else:
        await ollama.send(f"Error: {response.status_code}")