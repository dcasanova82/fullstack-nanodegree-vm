from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

MenuItems = session.query(MenuItem).delete()
# session.delete(MenuItems)
session.commit()
Restaurants = session.query(Restaurant).delete()
# session.delete(Restaurants)
session.commit()
