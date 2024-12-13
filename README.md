# 功能介绍
通过ollama提供的接口，
将你的nonebot连接到本地部署的基于ollama框架的LLM模型。

暂时只支持与单个模型进行纯文本聊天。

当前版本：v0.1

# 安装说明
### nb-cli（暂未发布）
```shell
nb plugin install nonebot-plugin-ollama
```

# 配置项
```python
#config.py
class ScopedConfig:
    model: str = "qwen2.5:0.5b"    # 填写所要使用的模型名称
    url: str = "http://127.0.0.1:11434/"    # 填写ollma所在的地址，形如http://***/
    priority: int = 5    # 填写优先级，数字越小优先级越高，推荐设置为低优先
```

# 链接
nonebot: https://nonebot.dev/   
ollama: https://ollama.org.cn/

# 协议
MIT