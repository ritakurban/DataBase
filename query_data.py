from create import *
from insert_data import *

# Query 1: Find the top 5 offices with the most sales for that month.

month = 11
top_offices = session.query(Offices.name, func.sum(Houses.price), func.extract('month', Sales.date)).join(Houses, and_(Offices.ID == Houses.office_id)).join(Sales, and_(Sales.house_id == Houses.ID)).group_by(Offices.ID).order_by(func.sum(Houses.price).desc()).filter(func.extract('month', Sales.date) == month).limit(5).statement

top_offices = pd.read_sql(top_offices, session.bind)
top_offices.columns=['Office', 'Sales', 'Month']
print(top_offices)

# Query 5: For all houses that were sold that month, calculate the average selling price

# Change the month variable above and run both сells to see results for other months.
if len(top_offices) >= 1:
    print("The average selling price for the {0}th month is ${1}".format(month, int(top_offices.mean()[0])))
else:
    print("No houses were sold in the {0}th month".format(month))

# Query 2: Find the top 5 estate agents who have sold the most (include their contact
# details and their sales details so that it is easy contact them and congratulate them).

# Names and contact info
top_agents = session.query(Agents.name, Agents.email, func.count(Houses.price), func.sum(Houses.price)).join(Houses, and_(Agents.ID == Houses.agent_id)).group_by(Agents.name).order_by(func.sum(Houses.price).desc()).limit(5).statement
top_agents = pd.read_sql(top_agents, session.bind)
top_agents.columns=['Agent', 'Email', 'Houses Sold','Sales']
print(top_agents)

#Sales details
agent = "Fenni Hoasner"

sales= session.query(Sales.ID, Buyers.name, Sellers.name, Sales.date, Houses.price).join(Houses, and_(Sales.house_id == Houses.ID)).join(Buyers, and_(Buyers.ID == Sales.buyer_id)).join(Agents, and_(Houses.agent_id == Agents.ID)).join(Sellers, and_(Houses.seller_id == Sellers.ID)).order_by(Sales.date).filter(Agents.name == agent).limit(5).statement
sales = pd.read_sql(sales, session.bind)
sales.columns=['Sale ID', 'Buyer', 'Seller','Date',"Price"]
print(sales)

# Query 3: Calculate the commission that each estate agent must receive and store the results in a separate table.

commissions_per_agent = session.query(Agents.name, func.sum(Commissions.amount), func.count(Commissions.amount)).join(Commissions, and_(Commissions.agent_id == Agents.ID)).group_by(Agents.name).order_by(func.sum(Commissions.amount).desc()).statement
commissions_per_agent = pd.read_sql(commissions_per_agent, session.bind)
commissions_per_agent.columns=['Agent', 'Total Commission', 'Number of Sales']
print(commissions_per_agent)

# Query 4: For all houses that were sold that month, calculate the average number of days that the house was on the market.

month = 4
dates = session.query(Houses.ID, Sales.date, Houses.date).join(Sales, and_(Sales.house_id == Houses.ID)).all()

n_days = []
for date in dates:
    n_days.append(date[1]-date[2])
avg_days = np.mean(n_days).days

print("Average number of days that the house was on the market is {0}.".format(avg_days))


# Query 6: Find the zip codes with the top 5 average sales prices

zip_codes = session.query(Houses.zip_code, func.sum(Houses.price)).group_by(Houses.zip_code).order_by(func.sum(Houses.price).desc()).limit(5).statement

zip_codes = pd.read_sql(zip_codes, session.bind)
zip_codes.columns=['Zip Code', 'Average Price']
print(zip_codes)

# Cleanup
session.close()
Base.metadata.drop_all(bind=engine)
