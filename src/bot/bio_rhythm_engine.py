import sys
import os
import re

current_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.insert(0, project_root)

from src.api.max_client import MaxBot
from src.bot.database import Database
from src.bot.procrastination_db import PROCRASTINATION_PATTERNS
from src.bot.pattern_analyzer import analyze_tasks
from aiomax import buttons


class BioRhythmEngine:
    def __init__(self):
        self.max_bot = MaxBot()
        self.db = Database()
        self.setup_handlers()

    def setup_handlers(self):
        bot = self.max_bot.bot

        # 🎯 ГЛАВНОЕ МЕНЮ - переиспользуем везде
        def get_main_menu():
            kb = buttons.KeyboardBuilder()
            kb.add(buttons.CallbackButton('🧠 Диагностика', 'diagnostics'))
            kb.add(buttons.CallbackButton('🎯 Анти-прокрастинация', 'antiprocrastination'))
            kb.add(buttons.CallbackButton('📝 Анализ задач', 'structure_tasks'))
            kb.add(buttons.CallbackButton('📊 Прогресс', 'progress'))
            return kb

        @bot.on_bot_start()
        async def welcome(pd):
            user = pd.user
            await pd.send(
                f"🧠 **MAX-Биоритм** - твой ИИ-тренер!\n\n"
                f"Просто напиши задачи типа:\n"
                f"• 'домашка математика уборка'\n"
                f"• 'проект спортзал звонок маме'\n\n"
                f"Я всё проанализирую и дам решение!",
                keyboard=get_main_menu()
            )

        @bot.on_message()
        async def handle_message(message):
            """Обрабатываем ЛЮБЫЕ сообщения - текст и голосовые!"""
            user_text = message.content

            if user_text and not user_text.startswith('/'):
                analysis = analyze_tasks(user_text)

                kb = buttons.KeyboardBuilder()
                kb.add(buttons.CallbackButton('🎯 Применить решение', f"apply_{analysis['type']}"))
                kb.add(buttons.CallbackButton('📅 Запланировать', 'schedule_tasks'))
                kb.add(buttons.CallbackButton('⬅️ Главное меню', 'back_main'))

                await message.reply(
                    f"🔮 **Анализ задач:**\n\n"
                    f"**Задачи:** {analysis['tasks']}\n\n"
                    f"**Проблема:** {analysis['procrastination_type']}\n"
                    f"**Решение:** {analysis['solution']}\n\n"
                    f"**Действие:** {analysis['action']}",
                    keyboard=kb
                )

        @bot.on_button_callback('diagnostics')
        async def start_diagnostics(callback):
            kb = buttons.KeyboardBuilder()
            kb.add(buttons.CallbackButton('🌅 Жаворонок', 'chrono_morning'))
            kb.add(buttons.CallbackButton('🌙 Сова', 'chrono_evening'))
            kb.add(buttons.CallbackButton('⚖️ Голубь', 'chrono_flex'))
            kb.add(buttons.CallbackButton('⬅️ Назад', 'back_main'))

            await callback.answer(
                text="🧠 **Диагностика биоритмов**\n\n"
                     "Когда пик твоей энергии?",
                keyboard=kb
            )

        # 🎯 ОБРАБОТЧИКИ ХРОНОТИПОВ
        @bot.on_button_callback('chrono_morning')
        async def set_morning_chrono(callback):
            kb = buttons.KeyboardBuilder()
            kb.add(buttons.CallbackButton('⬅️ Главное меню', 'back_main'))

            await callback.answer(
                text="🌅 **Ты Жаворонок!**\n\n"
                     "✅ Лучшие часы: 8:00-12:00\n"
                     "✅ Сложные задачи - утром\n"
                     "✅ Вечером - отдых и планирование\n\n"
                     "Используй утреннюю энергию по максимуму!",
                keyboard=kb
            )

        @bot.on_button_callback('chrono_evening')
        async def set_evening_chrono(callback):
            kb = buttons.KeyboardBuilder()
            kb.add(buttons.CallbackButton('⬅️ Главное меню', 'back_main'))

            await callback.answer(
                text="🌙 **Ты Сова!**\n\n"
                     "✅ Лучшие часы: 18:00-23:00\n"
                     "✅ Утром - легкие задачи\n"
                     "✅ Вечером - сложные проекты\n\n"
                     "Работай когда ты наиболее продуктивен!",
                keyboard=kb
            )

        # 🎯 ВОЗВРАТ В ГЛАВНОЕ МЕНЮ
        @bot.on_button_callback('back_main')
        async def back_to_main(callback):
            await callback.answer(
                text="🔄 Возвращаемся в главное меню!",
                keyboard=get_main_menu()
            )

        # 🎯 ЗАГЛУШКИ ДЛЯ ОСТАЛЬНЫХ КНОПОК
        @bot.on_button_callback('antiprocrastination')
        async def show_antiprocrastination(callback):
            kb = buttons.KeyboardBuilder()
            kb.add(buttons.CallbackButton('⬅️ Главное меню', 'back_main'))

            await callback.answer(
                text="🎯 **Анти-прокрастинация**\n\n"
                     "Скоро здесь будут:\n"
                     "• Методы борьбы с прокрастинацией\n"
                     "• Персональные рекомендации\n"
                     "• Система мотивации\n\n"
                     "⚡ В разработке!",
                keyboard=kb
            )

        @bot.on_button_callback('progress')
        async def show_progress(callback):
            kb = buttons.KeyboardBuilder()
            kb.add(buttons.CallbackButton('⬅️ Главное меню', 'back_main'))

            await callback.answer(
                text="📊 **Твой прогресс**\n\n"
                     "Скоро здесь будут:\n"
                     "• Статистика продуктивности\n"
                     "• Уровни и достижения\n"
                     "• Графики прогресса\n\n"
                     "⚡ В разработке!",
                keyboard=kb
            )

    def run(self):
        self.max_bot.run()