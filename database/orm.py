from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Product, Category, User, Item

from sqlalchemy import select, update, delete

from sqlalchemy.orm import joinedload, selectinload



#Запрос товар+категорию
async def orm_get_product_by_category_and_item(session: AsyncSession, category_id: int, item_id: int):
    query = select(Product).where(
        Product.category_id == category_id,
        Product.item_id == item_id
    ).options(
        joinedload(Product.category),  # Чтобы сразу загрузить связанные категории и товары
        joinedload(Product.item)
    )
    result = await session.execute(query)
    return result.scalar()

# Админка: добавить/изменить/удалить товар
async def orm_add_product(session: AsyncSession, data: dict):
    obj = Product(
        image=data['image'],
        latitude=data['latitude'],
        longitude=data['longitude'],
        category_id=int(data['category']),
        item_id=int(data['item']),
        description = data['description']
    )
    session.add(obj)
    await session.commit()
    await session.refresh(obj)  # Обновляем объект после коммита
    return obj


#Запрос на продукты
async def orm_get_products(session: AsyncSession, category_id):
    query = select(Product).where(Product.category_id == int(category_id))
    result = await session.execute(query)
    return result.scalars().all()


#Запрос продукт
async def orm_get_product(session: AsyncSession, product_id: int):
    query = select(Product).where(Product.id == product_id)
    result = await session.execute(query)
    return result.scalar()


# Добавляем юзера в БД
async def orm_add_user(
    session: AsyncSession,
    user_id: int,
    first_name: str | None = None,
    last_name: str | None = None,
    balance: float | None = None
):
    query = select(User).where(User.user_id == user_id)
    result = await session.execute(query)
    if result.first() is None:
        session.add(
            User(user_id=user_id, first_name=first_name, last_name=last_name,
                 balance=balance if balance is not None else 0)
        )
        await session.commit()


#Запрос на получение юзера
async def orm_get_user(session: AsyncSession, user_id: int):
    query = select(User).where(User.user_id == user_id)
    result = await session.execute(query)
    user = result.scalar_one_or_none()  # Возвращаем объект User или None
    return user


#Запрос на все категории
async def orm_get_categories(session: AsyncSession):
    query = select(Category)
    result = await session.execute(query)
    return result.scalars().all()

#Запрос на создание категорий
async def orm_create_categories(session: AsyncSession, categories: list):
    query = select(Category)
    result = await session.execute(query)
    if result.first() is None:
        session.add_all([Category(name=name) for name in categories])
        await session.commit()


#Запрос на все товары
async def orm_get_items(session: AsyncSession):
    query = select(Item)
    result = await session.execute(query)
    return result.scalars().all()

#Запрос на создание товара
async def orm_create_items(session: AsyncSession, items: list[tuple[str, float]]):
    query = select(Item)
    result = await session.execute(query)
    if result.first() is None:
        session.add_all([Item(name=name, price=price) for name, price in items])
        await session.commit()


async def orm_get_category_by_id(session: AsyncSession, category_id: int):
    result = await session.execute(
        select(Category).where(Category.id == category_id)
    )
    category = result.scalar_one_or_none()  # Возвращает одну запись или None, если не найдено
    return category

async def orm_get_item_by_id(session: AsyncSession, item_id: int):
    result = await session.execute(
        select(Item).where(Item.id == item_id)
    )
    item = result.scalar_one_or_none()  # Возвращает одну запись или None, если не найдено
    return item
