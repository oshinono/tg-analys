from celery import Celery
from database import REDIS_URL
from celery.schedules import crontab
from redbeat import RedBeatSchedulerEntry

# Инициализация Celery
app = Celery('tasks', broker=REDIS_URL)

# Настройка расписания задач
app.conf.beat_schedule = {
    'default-scan': {  # более конкретное название
        'task': 'bg_tasks.channels_scan.default_task',  # исправленный путь к задаче
        'schedule': crontab(hour='0'),  # выполнять раз в день в 00:00
        'options': {
            'expires': 3600  # задача истекает через час
        }
    },
}

# Функция для изменения расписания
def update_schedule(task_name: str, new_schedule: crontab) -> bool:
    """
    Обновляет расписание выполнения задачи.
    
    Args:
        task_name: Название задачи
        new_schedule: Новое расписание в формате crontab
    
    Returns:
        bool: Успешно ли обновлено расписание
    """
    try:
        entry = RedBeatSchedulerEntry(
            name=task_name,
            task='bg_tasks.channels_scan.',  # исправленный путь к задаче
            schedule=new_schedule,
            app=app
        )
        entry.save()
        return True
    except Exception as e:
        print(f"Ошибка при обновлении расписания: {str(e)}")
        return False

# Пример использования:
# update_schedule('название-задачи', crontab(minute='*/15'))  # каждые 15 минут


