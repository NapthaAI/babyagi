from pydantic import BaseModel, Field
from typing import List

class InputSchema(BaseModel):
    objective: str

class Task(BaseModel):
    """Class for defining a task to be performed."""
    name: str = Field(..., description="The name of the task to be performed.", alias="id")
    description: str = Field(..., description="The description of the task to be performed.")
    done: bool = Field(False, description="The status of the task. True if the task is done, False otherwise.")
    result: str = Field("", description="The result of the task.")

class TaskList(BaseModel):
    """Class for defining a list of tasks."""
    list: List[Task] = Field([], description="A list of tasks to be performed.")


class TaskFinalizer(BaseModel):
    """Class for finalizing the tasks."""
    final_report: str = Field("", description="The final report of the tasks.")
    new_tasks: List[Task] = Field([], description="A list of new tasks to be performed.")
    objective_met: bool = Field(False, description="The status of the objective. True if the objective have been met, False otherwise.")