from typing import List, Optional

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, Float

Base = declarative_base()


class Building(Base):
    '''Модель здания, содержащая информацию о местоположении'''
    __tablename__ = 'buildings'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    '''Уникальный идентификатор здания'''
    address: Mapped[str] = mapped_column(String(255))
    '''Адрес здания в формате: г. Москва, ул. Ленина 1, офис 3'''
    latitude: Mapped[float] = mapped_column(Float)
    '''Географическая широта местоположения здания'''
    longitude: Mapped[float] = mapped_column(Float)
    '''Географическая долгота местоположения здания'''
    
    organizations: Mapped[List['Organization']] = relationship(
        back_populates='building',
        cascade='all, delete-orphan',
        lazy='selectin'
    )
    '''Список организаций, расположенных в этом здании'''


class Activity(Base):
    '''Модель вида деятельности для классификации организаций'''
    __tablename__ = 'activities'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    '''Уникальный идентификатор вида деятельности'''
    name: Mapped[str] = mapped_column(String(100))
    '''Название вида деятельности (например, 'Молочная продукция')'''
    
    parent_id: Mapped[Optional[int]] = mapped_column(
        Integer, 
        ForeignKey('activities.id', ondelete='CASCADE'), 
        nullable=True
    )
    '''Идентификатор родительской деятельности для построения дерева'''
    
    parent: Mapped[Optional['Activity']] = relationship(
        'Activity', 
        remote_side=[id],
        back_populates='children'
    )
    '''Родительский вид деятельности'''
    
    children: Mapped[List['Activity']] = relationship(
        back_populates='parent',
        lazy='selectin',
        join_depth=3
    )
    '''Дочерние виды деятельности'''
    
    organizations: Mapped[List['Organization']] = relationship(
        secondary='organization_activities',
        back_populates='activities'
    )
    '''Организации, занимающиеся этим видом деятельности'''


class OrganizationActivity(Base):
    '''Вспомогательная таблица для связи многие-ко-многим между организациями и видами деятельности'''
    __tablename__ = 'organization_activities'
    
    organization_id: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey('organizations.id', ondelete='CASCADE'), 
        primary_key=True
    )
    '''Идентификатор организации'''
    
    activity_id: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey('activities.id', ondelete='CASCADE'), 
        primary_key=True
    )
    '''Идентификатор вида деятельности'''


class PhoneNumber(Base):
    '''Модель телефонного номера организации'''
    __tablename__ = 'phone_numbers'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    '''Уникальный идентификатор телефонного номера'''
    number: Mapped[str] = mapped_column(String(50))
    '''Номер телефона в произвольном формате (2-222-222, 3-333-333, 8-923-666-13-13)'''

    organization_id: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey('organizations.id', ondelete='CASCADE')
    )
    '''Идентификатор организации, к которой относится номер'''
    
    organization: Mapped['Organization'] = relationship(back_populates='phone_numbers')
    '''Организация, которой принадлежит этот номер телефона'''


class Organization(Base):
    '''Модель организации - карточка в справочнике'''
    __tablename__ = 'organizations'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    '''Уникальный идентификатор организации'''
    name: Mapped[str] = mapped_column(String(255), unique=True)
    '''Название организации (например, ООО 'Рога и Копыта')'''
    
    building_id: Mapped[int] = mapped_column(
        Integer, 
        ForeignKey('buildings.id', ondelete='CASCADE')
    )
    '''Идентификатор здания, в котором расположена организация'''
    
    building: Mapped['Building'] = relationship(back_populates='organizations')
    '''Здание, в котором расположена организация'''
    
    phone_numbers: Mapped[List['PhoneNumber']] = relationship(
        back_populates='organization',
        cascade='all, delete-orphan',
        lazy='selectin'
    )
    '''Список телефонных номеров организации'''
    
    activities: Mapped[List['Activity']] = relationship(
        secondary='organization_activities',
        back_populates='organizations',
        lazy='selectin'
    )
    '''Виды деятельности, которыми занимается организация'''