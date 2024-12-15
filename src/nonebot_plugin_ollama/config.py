from pydantic import BaseModel, field_validator

class ScopedConfig(BaseModel):
    model: str = 'qwen2.5:0.5b'
    url: str = 'http://127.0.0.1:11434/'  # http://***/
    min_priority: int = 5
    max_histories: int = 50
    
class Config(BaseModel):
    ollama: ScopedConfig = ScopedConfig()