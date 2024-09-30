import json
from typing import Dict
from naptha_sdk.task import Task as Agent
from babyagi.utils import get_logger
from babyagi.schemas import InputSchema

logger = get_logger(__name__)


async def run(inputs: InputSchema, worker_node_urls, *args, **kwargs):

    # get initial task lists
    task_list_agent = Agent(
        name="task_initiator_agent",
        fn="babyagi_task_initiator",
        worker_node_url=worker_node_urls[0],
        *args, 
        **kwargs,
    )

    # task_execution_agent
    task_execution_agent = Agent(
        name="task_execution_agent",
        fn="babyagi_task_executor",
        worker_node_url=worker_node_urls[1],
        *args, 
        **kwargs,
    )

    # task_finalizer_agent
    task_finalizer_agent = Agent(
        name="task_finalizer_agent",
        fn="babyagi_task_finalizer",
        worker_node_url=worker_node_urls[0],
        *args, 
        **kwargs,
    )

    task_list = await task_list_agent(objective=inputs.objective)
    logger.info(f"Initial task list: {task_list}")

    task_list = json.loads(task_list)
    for task in task_list['list']:
        task['done'] = False

    tasks_to_perform = [task for task in task_list['list'] if not task['done']]
    count_num_outstanding_tasks = len(tasks_to_perform)

    logger.info(f"Number of outstanding tasks: {count_num_outstanding_tasks}")

    while count_num_outstanding_tasks > 0:
        logger.info(f"Performing {count_num_outstanding_tasks} tasks")

        for task in tasks_to_perform:
            task_str = f"Task Name: {task['name']}\nTask Description: {task['description']}\n"
            task_execution_response = await task_execution_agent(task=task_str, objective=inputs.objective)
            logger.info(f"Task response: {task_execution_response}")

            task['result'] = task_execution_response
            task['done'] = True

        tasks_str = ""
        for task in task_list['list']:
            tasks_str += f"Task Name: {task['name']}\nTask Description: {task['description']}\nTask Result: {task['result']}\nDone: {task['done']}\n"
        logger.info(f"Final task list: {tasks_str}")

        task_finalizer_response = await task_finalizer_agent(task=tasks_str, objective=inputs.objective)
        logger.info(f"Task finalizer response: {task_finalizer_response}")

        task_finalizer_response = json.loads(task_finalizer_response)

        count_num_outstanding_tasks = len([task for task in task_list['list'] if not task['done']])
        logger.info(f"Number of outstanding tasks: {count_num_outstanding_tasks}")


    logger.info(f"Completed task list: {task_finalizer_response}")

    task_list['list'].append(
        {
            'name': "Finalizer Task",
            'description': "Finalizer Task",
            'done': True,
            'result':task_finalizer_response['final_report']
        }
    )

    return json.dumps(task_list)

