import datetime

import motor.motor_asyncio

from config import Config


class Singleton(type):
    __instances__ = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances__:
            cls.__instances__[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls.__instances__[cls]


class Database(metaclass=Singleton):
    def __init__(self):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(Config.DATABASE_URL)
        self.db = self._client[Config.SESSION_NAME]
        self.col = self.db.users

        self.cache = {}

    def new_user(self, id):
        return dict(
            id=id,
            join_date=datetime.date.today().isoformat(),
            last_used_on=datetime.date.today().isoformat(),
            as_file=False,
            watermark_text="",
            sample_duration=30,
            as_round=False,
            watermark_color=0,
            screenshot_mode=0,
            font_size=1,
            ban_status=dict(
                is_banned=False,
                ban_duration=0,
                banned_on=datetime.date.max.isoformat(),
                ban_reason="",
            ),
        )

    async def get_user(self, id):
        user = self.cache.get(id)
        if user is not None:
            return user

        user = await self.col.find_one({"id": int(id)})
        self.cache[id] = user
        return user

    async def add_user(self, id):
        user = self.new_user(id)
        await self.col.insert_one(user)

    async def is_user_exist(self, id):
        user = await self.get_user(id)
        return True if user else False

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        all_users = self.col.find({})
        return all_users

    async def delete_user(self, user_id):
        user_id = int(user_id)
        if self.cache.get(user_id):
            self.cache.pop(user_id)
        await self.col.delete_many({"id": user_id})
