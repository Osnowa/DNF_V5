from fastapi import HTTPException
from beanie import PydanticObjectId

from database.models import User

class UserRepository:

    async def add(self, user_name: str, user_surname: str, user_age: int, user_notes: list[str]):
        '''Создание пользователя'''
        user = User(first_name=user_name, last_name=user_surname, age=user_age, notes=user_notes)
        await user.insert() # сохраняем 
        return user

    async def get_user(self, user_id: PydanticObjectId):
        '''Получение 1 пользователя'''
        res =  await User.find_one(User.id == user_id)
        if res is None:
            raise HTTPException(status_code=404, detail="User not found")
        return res

    async def update_user(self, user_id: PydanticObjectId, user_name: str | None, user_surname: str | None, user_age: int | None, user_notes: list[str] | None):
        '''Обновляем пользователя (patch)'''
        user = await User.find_one(User.id == user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        user.first_name = user_name if user_name is not None else user.first_name
        user.last_name = user_surname if user_surname is not None else user.last_name
        user.age = user_age if user_age is not None else user.age
        user.notes = user_notes if user_notes is not None else user.notes
        await user.save()
        return user

    async def delete_user(self, user_id: PydanticObjectId):
        '''Удаляем пользователя'''
        user = await User.find_one(User.id == user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        await user.delete()