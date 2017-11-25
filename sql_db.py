'''Create db and tables'''
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)

def connect_to_db(t_engine, n_db, password, login='root', server='localhost'):
    '''t_engine = type of database, n_db = name of database'''
    DB_NAME = n_db

    if t_engine == 'sqlite':
        db = create_engine('sqlite:///{0}.db'.format(DB_NAME))
        return db

    elif t_engine == 'mysql':
        db = create_engine('mysql://{0}:{1}@{2}'.format(login, password, server))
        db.execute('CREATE DATABASE IF NOT EXISTS {0}'.format(DB_NAME))
        db.execute('USE {0}'.format(DB_NAME))
        return db

    else:
        print('wrong engine type!!!!')
        quit()


# construct a base class for declarative class definitions
Base = declarative_base()


class Suppliers(Base):
    '''Create suppliers table'''
    __tablename__ = 'Suppliers'

    SupplierID = Column(Integer, primary_key=True, unique=True)
    CompanyName = Column(String(250))
    ContactName = Column(String(120))
    Adress = Column(String(250))
    Phone = Column(String(250))
    Country = Column(String(100))

    def __repr_(self):
        '''it`s how we represent table'''
        return """id: '{0} CompanyName: '{1}' ContactName: '{2}'
            Adress: '{3}' Phone: '{4}'Country: '{5}'""".format(
                self.SupplierID, self.CompanyName, self.ContactName,
                self.Adress, self.Phone, self.Country)

class Orders(Base):
    '''Create orders table'''
    __tablename__ = 'Orders'

    OrderID = Column(Integer, primary_key=True)
    CustomerID = Column(Integer)
    OrderDate = Column(DateTime, default=datetime.datetime.utcnow)
    ShippedDate = Column(DateTime, default=datetime.datetime.utcnow)
    ShipName = Column(String(120))
    ShipAdress = Column(String(250))

    def __repr__(self):
        return """id: '{0}' CustomerID: '{1}' OrderDate: '{2}'
        ShippedDate: '{3}' ShipeName: '{4}' ShipAdress: '{5}'\n""".format(
            self.OrderDate, self.CustomerID, self.OrderDate,
            self.ShippedDate, self.ShipName, self.ShipAdress
        )

class Categories(Base):
    '''Create categories table'''
    __tablename__ = 'Categories'

    CategoryID = Column(Integer, primary_key=True, unique=True)
    CategoryName = Column(String(80))
    Description = Column(String(500))

    def __repr___(self):
        return """id: '{0}' CategoryName: '{1}' Description: '{2}'\n""".format(
            self.CategoryID, self.CategoryName, self.Description
        )

class Products(Base):
    '''Create products table'''
    __tablename__ = 'Products'

    ProductID = Column(Integer, primary_key=True, unique=True)
    ProductName = Column(String(100))
    SupplierID = Column(Integer, ForeignKey(Suppliers.SupplierID))
    CategoryID = Column(Integer, ForeignKey(Categories.CategoryID))
    UnitPrice = Column(Integer)

    #productD = relationship('OrderDetail', backref='product',
     #                       order_by='OrderDetail.OrderDetID')

    def __repr_(self):
        return """id: '{0}' ProductName: '{1}' SupplierID: '{2}' CategoryID: '{2}'
    UnitPrice: '{3}'\n""".format(self.ProductID, self.ProductName, self.SupplierID,
                                 self.CategoryID, self.UnitPrice
                                )

class OrderDetail(Base):
    '''Create OderDetail table'''
    __tablename__ = 'OrderDetails'

    OrderDetID = Column(Integer, primary_key=True, unique=True)
    ProductID = Column(ForeignKey('Products.ProductID'))
    UnitPrice = Column(Integer)
    Quantity = Column(Integer)
    Discount = Column(Integer)

    prod = relationship('Products', backref='Products')

    def __repr_(self):
        return """id: '{0}' ProductID: '{1}' UnitPrice: '{2}' Quantity: '{3}'
    Discount: '{4}'\n""".format(self.OrderDetID, self.ProductID, self.UnitPrice,
                                self.Quantity, self.Discount
                               )
