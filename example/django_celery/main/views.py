from django.shortcuts import render
from django.http import HttpResponse
from .tasks import add
from celery.app.control import Inspect

# Create your views here.

def run_add_task(request):
    if request.method == "POST":
        try:
            x = int(request.POST.get("x", 2))
            y = int(request.POST.get("y", 3))
            seconds = int(request.POST.get("seconds", 0))
        except Exception:
            return HttpResponse("Невалидные параметры", status=400)
        task = add.delay(x, y, seconds)
        return HttpResponse(f"""
            <h2>Задача отправлена!</h2><br>Task ID: {task.id}<br><a href='/run-add/'>Назад</a>
        """)
    form_html = """
    <h2>Запуск Celery задачи add(x, y, seconds)</h2>
    <form method='post'>
        x: <input type='number' name='x' value='2'><br>
        y: <input type='number' name='y' value='3'><br>
        seconds (имитация выполнения): <input type='number' name='seconds' value='0' min='0' max='60'><br>
        <input type='submit' value='Старт'>
    </form>
    <a href='/'>На главную (мониторинг задач)</a>
    """
    return HttpResponse(form_html)


def tasks_overview(request):
    i = Inspect()
    active = i.active() or {}
    reserved = i.reserved() or {}
    scheduled = i.scheduled() or {}

    def flat_tasks(tasks_dict, state):
        result = []
        for worker, tasks in (tasks_dict or {}).items():
            for task in tasks:
                result.append({
                    'state': state,
                    'id': task.get('id'),
                    'name': task.get('name'),
                    'args': task.get('args'),
                    'kwargs': task.get('kwargs'),
                    'worker': worker,
                })
        return result

    all_tasks = flat_tasks(active, 'active') + flat_tasks(reserved, 'reserved') + flat_tasks(scheduled, 'scheduled')

    html = """
    <h1>Celery Tasks Overview</h1>
    <table border='1'><tr><th>Task ID</th><th>Name</th><th>Args</th><th>Kwargs</th><th>Status</th><th>Worker</th></tr>
    """
    for task in all_tasks:
        html += f"<tr>\n<td>{task['id']}</td><td>{task['name']}</td><td>{task['args']}</td><td>{task['kwargs']}</td><td>{task['state']}</td><td>{task['worker']}</td>\n</tr>"
    html += """
    </table>
    <br><a href='/run-add/'>Запустить демо задачу add(2, 3)</a>
    """
    return HttpResponse(html)
