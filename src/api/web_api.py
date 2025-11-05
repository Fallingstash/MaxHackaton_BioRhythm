from aiohttp import web
import json
import sqlite3


class WebAPI:
    def __init__(self, db_path='focus_bot.db'):
        self.db_path = db_path
        self.app = web.Application()
        self.setup_routes()

    def setup_routes(self):
        self.app.router.add_get('/api/user/{user_id}', self.get_user_stats)
        self.app.router.add_get('/api/leaderboard', self.get_leaderboard)

    async def get_user_stats(self, request):
        user_id = request.match_info['user_id']
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            user = cursor.fetchone()

        if user:
            return web.json_response({
                "user_id": user[0],
                "username": user[1],
                "focus_time": user[2],
                "level": user[2] // 60  # 1 уровень за каждый час
            })
        return web.json_response({"error": "User not found"}, status=404)

    async def get_leaderboard(self, request):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT username, focus_time FROM users ORDER BY focus_time DESC LIMIT 10')
            leaders = cursor.fetchall()

        leaderboard = [{"username": u[0], "focus_time": u[1]} for u in leaders]
        return web.json_response(leaderboard)

    def run(self):
        web.run_app(self.app, port=8080, host='0.0.0.0')