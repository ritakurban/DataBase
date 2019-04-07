from create import *


# Generate entries
office_keys = ['ID', 'name']
office_values = [
    [1,"California"],
    [2,"New York"],
    [3,"Massachusetts"],
    [4,"Washington"],
    [5,"Nevada"]]


house_keys = ['ID', 'seller_id', 'n_bedrooms', 'n_bathrooms', 'price', 'zip_code',
              'date', 'agent_id', 'office_id', 'status']
house_values = [
    [1,1,2,1,200000,94102,date(2018,4,25), 1,1,0],
    [2,2,1,1,100000,94102,date(2018,5,20), 2,1,0],
    [3,3,4,3,700000,94102,date(2018,8,18), 4,1,0],
    [4,4,4,3,600000,94103,date(2018,8,16), 5,2,0],
    [5,5,3,2,500000,94103,date(2018,9,5), 1,2,0],
    [6,1,2,2,300000,94103,date(2018,11,4), 2,2,0],
    [7,2,5,3,800000,94104,date(2018,2,25), 3,3,0],
    [8,3,1,1,200000,94104,date(2018,6,27), 2,3,0],
    [9,4,2,2,300000,94104,date(2018,7,11), 1,3,0],
    [10,5,3,2,400000,94105,date(2018,9,16), 2,4,0],
    [11,1,4,2,800000,94105,date(2018,10,5), 3,4,0],
    [12,2,2,1,400000,94105,date(2018,11,8), 4,4,0],
    [13,3,1,1,100000,94106,date(2018,12,1), 3,5,0],
    [14,4,3,2,600000,94106,date(2018,1,31), 5,5,0],
    [15,5,4,2,1000000,94106,date(2018,3,18), 5,5,0],
    [16,5,3,1,300000,94104,date(2019,1,27), 1,3,0],
    [17,5,2,1,150000,94104,date(2019,2,18), 2,3,0],
    [18,4,3,3,800000,94102,date(2019,3,4), 3,1,0],
    [19,2,6,3,1100000,94103,date(2019,4,6), 4,2,0],
    [20,3,4,2,700000,94103,date(2019,5,15), 5,2,0],
    [21,3,3,2,500000,94103,date(2019,6,14), 2,2,0],
    [22,1,6,3,700000,94104,date(2019,7,5), 3,3,0]]


agent_keys = ['ID', 'name', 'email']
agent_values = [
    [1,'Gregory Watson','watson@gmail.com'],
    [2,'Alice Gander','gander_alice@gmail.com'],
    [3,'Adam Walferd','walferd_ben@gmail.com'],
    [4,'Denis Cremen','cremen_denis@gmail.com'],
    [5,'Fenni Hoasner','hoasner@gmail.com']]

seller_keys = ['ID', 'name','email']
seller_values = [
    [1,'David Kahn','kahl@gmail.com'],
    [2,'Nancy Dawn','nancy_dawn@gmail.com'],
    [3,'Sherrill Mann','mann_sherrill@gmail.com'],
    [4,'Vera Benster','vera_benster@gmail.com'],
    [5,'Georg Miller','miller@gmail.com']]


buyer_keys = ['ID','name', 'email']
buyer_values = [
    [1,'Slava Kochitz','konchitz@gmail.com'],
    [2,'Pasha Sevkov','pasha_sevkov@gmail.com'],
    [3,'Jared Smith','jared_smith@gmail.com'],
    [4,'Mary Puffindor','mary_puff@gmail.com'],
    [5,'Kate Chervotkin','chechotkin@gmail.com']]

# Add entries to the session
Base.metadata.drop_all(bind=engine)

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

keys = [office_keys, house_keys, agent_keys, seller_keys, buyer_keys]
values = [office_values, house_values, agent_values, seller_values, buyer_values]
tables = [Offices, Houses, Agents, Sellers, Buyers]


def add_entries(keys, values, tables):
    '''
    Add entries to the table by combining keys, values,
    and table names.
    '''
    list_of_dict = []
    for value in values:
        item_dict = dict(zip(keys, value))
        list_of_dict.append(item_dict)

    for data_entry in list_of_dict:
        entry = tables(**data_entry)
        session.add(entry)


for i in range(len(tables)):
    add_entries(keys[i], values[i], tables[i])

session.commit()
session.close()

def sell_house(house_id, buyer_id, date):
    '''
    Add a transaction to the sales table.
    Update the status of the house from 0 to 1.
    Calculate commissions and populate the Commissions table.
    '''

    # Change the house status
    sold = session.query(Houses).filter(Houses.ID == house_id)
    sold.update({Houses.status: 1})

    # Calculate listing price, commission and total price
    listing_price = session.query(Houses.price).filter(Houses.ID == house_id).first()[0]
    agent_id = session.query(Houses.agent_id).filter(Houses.ID == house_id).first()[0]
    coef = case([(Houses.price < 100000, 0.01),
           (Houses.price < 200000, 0.075),
           (Houses.price < 500000, 0.06),
           (Houses.price < 1000000, 0.05),
           (Houses.price >= 1000000, 0.04),])
    commission = session.query(Houses.price*coef).filter(Houses.ID == house_id).first()[0]
    sale_price = listing_price + commission

    # Add Sales entry
    session.add(Sales(
        house_id = house_id,
        buyer_id = buyer_id,
        sale_price = sale_price,
        date = date))


    # Add Commissions entry
    sale = session.query(Sales.ID).filter(Houses.ID == house_id).first()[0]

    session.add(Commissions(
        sale_id = sale,
        amount = commission,
        agent_id = agent_id))

    session.commit()

# Insert new data
sale_values = [
    [1,5,date(2018,12,10)],
    [2,4,date(2018,6,8)],
    [3,3,date(2018,12,17)],
    [4,2,date(2018,11,23)],
    [5,1,date(2019,1,17)],
    [6,5,date(2019,4,8)],
    [7,4,date(2019,3,13)],
    [8,3,date(2018,12,27)],
    [9,2,date(2018,9,1)],
    [10,1,date(2019,4,23)],
    [11,5,date(2018,11,10)],
    [12,4,date(2019,4,10)],
    [13,3,date(2019,3,12)],
    [14,2,date(2018,9,18)],
    [15,1,date(2018,11,16)]]

for value in sale_values:
    sell_house(*value)
