import uuid
from pydantic import BaseSettings, Field
from uuid import UUID

class Settings(BaseSettings):
    """
    Configurações globais do servidor
    """
    API_V1_STR: str 
    PROJECT_NAME: str 
    INSTANCE_ID: UUID 


settings = Settings(
    API_V1_STR="/v1",
    INSTANCE_ID=uuid.uuid4(),
    PROJECT_NAME="Temperature Provider"
)