from pydantic import BaseModel, Field
from typing import List

class InputSchema(BaseModel):
    objective: str