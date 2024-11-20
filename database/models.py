from sqlalchemy import DateTime, String, Text, Float, Integer, func, BigInteger, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    update: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    image: Mapped[str] = mapped_column(String(150))
    latitude : Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)

    category_id:Mapped[int] = mapped_column(ForeignKey('category.id', ondelete='CASCADE'), nullable=False)
    category: Mapped['Category'] = relationship(backref='product')

    item_id: Mapped[int] = mapped_column(ForeignKey('item.id', ondelete='CASCADE'), nullable=False)
    item: Mapped['Item'] = relationship(backref='product')

    description: Mapped[str] = mapped_column(String(200), nullable=True)

class Category(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    first_name: Mapped[str] = mapped_column(String(150), nullable=True)
    last_name: Mapped[str]  = mapped_column(String(150), nullable=True)
    balance: Mapped[int] = mapped_column(Float, nullable=False)


class Item(Base):
    __tablename__ = 'item'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    price: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)