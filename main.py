'''Execute script and fill fake data in db'''
from sql_db import *
# rom sql_db import connect_to_db
from mimesis import Generic
from sqlalchemy.orm import sessionmaker


# write type of connection - sqlite/mysql, database_name, password
db = connect_to_db('mysql', 'drink_magazine', '')

if __name__ == '__main__':

    # create a top level Session configuration
    Session = sessionmaker(bind=db)
    session = Session()

    Base.metadata.create_all(db)

    g = Generic()

    for i in range(1, 11):
        supp = Suppliers(CompanyName=g.business.company(), ContactName=g.personal.full_name(),
                         Adress=g.address.street_name() + ' ' + g.address.street_suffix(),
                         Phone=g.personal.telephone(), Country=g.address.country()
                        )
        orders = Orders(CustomerID=i, ShipName=g.food.drink(), ShipAdress=g.address.state())
        category = Categories(CategoryName=g.food.drink(), Description=g.text.sentence())
        product = Products(SupplierID=i, CategoryID=i, ProductName=g.personal.name(), UnitPrice=10)
        orderDet = OrderDetail(ProductID=i, UnitPrice=15, Quantity=1, Discount=1.5)
        session.add_all([supp, orders, category, product, orderDet])

    session.commit()
    '''
    for orderD in session.query(Orders):
        print(orderD)
    '''
    print('[OK]')

