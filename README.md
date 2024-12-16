# 功能介绍
通过ollama提供的接口，
将你的nonebot连接到本地部署的基于ollama框架的LLM模型。

暂时只支持与单个模型进行纯文本聊天。

### 主要功能
使用自定义命令前缀进行对话。

当前版本：v0.2.3-c0.1

# 配置项
```python
#config.py
class ScopedConfig:
    model: str = "qwen2.5:0.5b"    # 填写所要使用的模型名称
    url: str = "http://127.0.0.1:11434/"    # 填写ollma所在的地址，形如http://***/
    min_priority: int = 5    # 填写优先级，数字越小优先级越高，推荐设置为低优先，
    # 该优先级为clear指令优先级，对话优先级为 min_priority+1
    max_histories: int = 100    # 填写最大历史对话记录条数
    listening: str = ["00110721", "10001"] # 填写使用对话功能的群聊号或私聊对方QQ号
    cmd: str = ["ollama ", "qwen "] # 填写希望机器人回复此消息的命令前缀
```

推荐先修改你所使用模型Modelfile的System项，调整后能够更加胜任工作。

输入至你的模型的消息格式如下（已自动删去命令前缀）:

[2024-12-14 19:12:52] UserName: 这是一条测试消息。

### 隐私数据管理
机器人所使用的所有聊天记录均储存于本地，且随机器人重启而清空。

在仅使用本地LLM的情况下，你的聊天数据不会被上传至任何第三方服务器进行处理。

### 未来开发方向：

1. 自动切换llava进行图片处理
2. 在config.py内添加对Modelfile的支持
3. 聊天记录（日志）导出

最终目标：提供API，为其他开发者实现跨插件事件响应与处理。

# 相关链接
nonebot: https://nonebot.dev/   
ollama: https://ollama.org.cn/

# 开源协议
MIT
