import re


def analyze_tasks(user_input):
    """Анализирует ввод пользователя и определяет тип прокрастинации + решение"""

    # Определяем категории задач
    tasks = extract_tasks(user_input)

    # Анализируем эмоциональную нагрузку
    emotional_weight = analyze_emotional_weight(user_input)

    # Определяем тип прокрастинации
    procrastination_type = identify_procrastination_type(tasks, emotional_weight)

    # Подбираем решение
    solution = get_solution(procrastination_type)

    return {
        'tasks': tasks,
        'emotional_weight': emotional_weight,
        'procrastination_type': procrastination_type,
        'solution': solution['solution'],
        'action': solution['action'],
        'type': procrastination_type
    }


def extract_tasks(text):
    """Извлекает задачи из текста"""
    # Простой парсинг по ключевым словам
    task_keywords = ['сделать', 'написать', 'купить', 'позвонить', 'подготовить', 'сходить']
    tasks = []

    words = text.lower().split()
    for i, word in enumerate(words):
        if word in task_keywords and i + 1 < len(words):
            task = f"{word} {words[i + 1]}"
            tasks.append(task)

    return tasks if tasks else ["Общие задачи"]


def analyze_emotional_weight(text):
    """Анализирует эмоциональную нагрузку задач"""
    stress_words = ['срочно', 'надо', 'должен', 'обязан', 'проблема', 'сложно']
    positive_words = ['хочу', 'мечта', 'интересно', 'нравится']

    stress_count = sum(1 for word in stress_words if word in text.lower())
    positive_count = sum(1 for word in positive_words if word in text.lower())

    if stress_count > positive_count:
        return "high"  # Высокая нагрузка
    elif positive_count > stress_count:
        return "low"  # Низкая нагрузка
    else:
        return "medium"  # Средняя нагрузка


def identify_procrastination_type(tasks, emotional_weight):
    """Определяет тип прокрастинации"""
    if emotional_weight == "high" and len(tasks) > 3:
        return "overwhelm"  # Перегрузка
    elif emotional_weight == "high":
        return "fear_failure"  # Страх провала
    elif len(tasks) == 0:
        return "no_motivation"  # Нет мотивации
    else:
        return "cant_start"  # Не могу начать


def get_solution(procrastination_type):
    """Возвращает решение для типа прокрастинации"""
    solutions = {
        "overwhelm": {
            "solution": "Метод 'Швейцарского сыра' - сделай маленькие дырочки в самых страшных задачах",
            "action": "Выбери ОДНУ самую противную задачу и сделай только 5% от неё"
        },
        "fear_failure": {
            "solution": "Метод 'Минимального действия' - цель 'сделать плохо'",
            "action": "Сделай первую версию намеренно криво, разреши себе ошибаться"
        },
        "no_motivation": {
            "solution": "Дедлайн с последствиями + награда",
            "action": "Поставь таймер на 25 минут. После - любимое дело как награда!"
        },
        "cant_start": {
            "solution": "Правило 2-х минут + энергетические помидоры",
            "action": "Сделай только первые 2 минуты задачи. Можно бросить после!"
        }
    }

    return solutions.get(procrastination_type, solutions["cant_start"])