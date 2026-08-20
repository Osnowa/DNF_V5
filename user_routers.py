from fastapi import APIRouter, FastAPI, HTTPException, status
from database.user_repositories import UserRepository
from beanie import PydanticObjectId
from schemas import UserCreate, UserUpdate, UserResponse



router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(user: UserCreate):
    '''Создание пользователя'''
    user_repository = UserRepository()
    return await user_repository.add(user.name, user.surname, user.age, user.notes)

@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(user_id: PydanticObjectId):
    '''Получение 1 пользователя'''
    user_repository = UserRepository()
    return await user_repository.get_user(user_id)

@router.patch("/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(user_id: PydanticObjectId, user: UserUpdate):
    '''Обновляем пользователя (patch)'''
    user_repository = UserRepository()
    return await user_repository.update_user(user_id, user.name, user.surname, user.age, user.notes)

@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: PydanticObjectId):
    '''Удаляем пользователя'''
    user_repository = UserRepository()
    return await user_repository.delete_user(user_id)