from pydantic import BaseModel, field_validator

class ScopedConfig(BaseModel):
    model: str = 'ATRI'
    url: str = 'http://127.0.0.1:11434/'
    min_priority: int = 5
    max_histories: int = 100
    Listening: str = ["419921469", "2058165181", "2574652640"]

    @field_validator('min_priority')
    @classmethod
    def check_priority(cls, v: int):
        if v >= 1:
            return v
        raise ValueError('ollama command priority must be greater than 1')
    
    @field_validator('url')
    @classmethod
    def check_url(cls, v: str):
        if v.startswith('http://') and v.endswith('/'):
            return v
        raise ValueError('ollama url must start with http:// and end with /')
    
class Config(BaseModel):
    ollama: ScopedConfig = ScopedConfig()