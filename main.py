from database import engine, metadata_obj
from crud import create_task, get_tasks, delete_task, update_task, change_task_status

metadata_obj.create_all(engine)

# test qiling har bir crud functionni
