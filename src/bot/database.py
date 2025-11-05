import sqlite3
import logging


class Database:
    def __init__(self, db_path='focus_bot.db'):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """Создаем таблицы если их нет"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Таблица пользователей
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    total_focus_time INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Таблица сессий фокусировки
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS focus_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    duration INTEGER,
                    completed BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(user_id)
                )
            ''')

            conn.commit()
            print("✅ База данных инициализирована!")

    def add_user(self, user_id, username):
        """Добавляем пользователя если его нет"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)',
                (user_id, username)
            )
            conn.commit()
            print(f"✅ Пользователь {username} добавлен в БД")

    def start_focus_session(self, user_id, duration):
        """Начинаем новую сессию фокусировки"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO focus_sessions (user_id, duration) VALUES (?, ?)',
                (user_id, duration)
            )
            conn.commit()
            print(f"✅ Сессия фокусировки начата для пользователя {user_id}")

    def get_user_stats(self, user_id):
        """Получаем статистику пользователя"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Считаем сессии и общее время
            cursor.execute(
                'SELECT COUNT(*), COALESCE(SUM(duration), 0) FROM focus_sessions WHERE user_id = ?',
                (user_id,)
            )
            result = cursor.fetchone()
            sessions, total_time = result if result else (0, 0)

            # Получаем имя пользователя
            cursor.execute('SELECT username FROM users WHERE user_id = ?', (user_id,))
            user_result = cursor.fetchone()
            username = user_result[0] if user_result else "Anonymous"

            return {
                'username': username,
                'sessions': sessions,
                'total_time': total_time,
                'level': total_time // 60 + 1  # 1 уровень за каждый час
            }

    def save_task_analysis(self, user_id, user_input, analysis_result):
        """Сохраняем анализ задач пользователя"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO task_analyses (user_id, user_input, procrastination_type, solution)
                VALUES (?, ?, ?, ?)
            ''', (user_id, user_input, analysis_result['procrastination_type'], analysis_result['solution']))
            conn.commit()

    def get_user_patterns(self, user_id):
        """Получаем паттерны прокрастинации пользователя"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT procrastination_type, COUNT(*) as count 
                FROM task_analyses 
                WHERE user_id = ? 
                GROUP BY procrastination_type 
                ORDER BY count DESC
            ''', (user_id,))
            return cursor.fetchall()