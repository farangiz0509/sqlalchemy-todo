from crud import create_task, get_tasks, update_task, delete_task, change_task_status

# 1. Create a new task
task_id = create_task("Test Task", "This is a test description")
print("Created Task ID:", task_id)

# 2. Get all tasks
tasks = get_tasks()
print("All Tasks:", tasks)

# 3. Update the task
update_task(task_id, title="Updated Task", description="Updated description")
updated_tasks = get_tasks()
print("Tasks after update:", updated_tasks)

# 4. Change task status
updated_task = change_task_status(task_id)
print("Task after status change:", updated_task)

# 5. Delete the task
result = delete_task(task_id)
print(result)

# 6. Get all tasks after deletion
final_tasks = get_tasks()
print("Tasks after deletion:", final_tasks)
