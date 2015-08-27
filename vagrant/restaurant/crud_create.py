from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, Menu, Item

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()
myFirstRestaurant = Restaurant(name = "Pizza Palace")
session.add(myFirstRestaurant)
session.commit()
session.query(Restaurant).all()
cheesepizza = MenuItem(name)