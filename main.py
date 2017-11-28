'''Execute script and fill fake data in db'''
import random
from sql_db import *
from mimesis import Generic
from sqlalchemy.orm import sessionmaker


# write type of connection - sqlite/mysql, database_name
db = connect_to_db('sqlite', 'drink_magazine')

if __name__ == '__main__':

    # create a top level Session configuration
    Session = sessionmaker(bind=db)
    session = Session()

    Base.metadata.create_all(db)

    g = Generic()

    for i in range(1, 11):
        disc = random.random()
        price = random.randint(10, 50)
        quantity = random.randint(1, 10)
        supp = Suppliers(CompanyName=g.business.company(), ContactName=g.personal.full_name(),
                         Adress=g.address.street_name() + ' ' + g.address.street_suffix(),
                         Phone=g.personal.telephone(), Country=g.address.country()
                        )
        orders = Orders(CustomerID=i, ShipName=g.food.drink(), ShipAdress=g.address.state())
        category = Categories(CategoryName=g.food.drink(), Description=g.text.sentence())
        product = Products(SupplierID=i, CategoryID=i, ProductName=g.personal.name(), UnitPrice=price)
        orderDet = OrderDetail(ProductID=i, UnitPrice=price, Quantity=quantity, Discount=disc)
        session.add_all([supp, orders, category, product, orderDet])

    session.commit()

    print('[OK]')
