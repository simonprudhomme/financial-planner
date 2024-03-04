from src.entity import BankAccount, Entity, Loan, RealEstate

# ASSETS
INFLATION_RATE = 3
bank_account = BankAccount(
    name="Bank Account", # Banq/Investment account
    amount=650_000,
    annual_inflation_rate=6, # 6% is the average return of the stock market
    start_date="2023-10-01",
)

triplex_acquisition_date = "2023-12-01"
triplex = RealEstate(
    name="Triplex",
    amount=1_000_000,
    cashdown=200_000,
    annual_expected_return=INFLATION_RATE,
    acquisition_entities=[
        Entity(
            name="Cashdown_Triple",
            amount=-200_000,
            start_date=triplex_acquisition_date,
            end_date=triplex_acquisition_date,
        ),
        Entity(
            name="Renovations_Triple",
            amount=-12_000,
            start_date=triplex_acquisition_date,
            end_date=triplex_acquisition_date,
        ),
        Entity(
            name="Welcome Taxe_Triple",
            amount=-12_000,
            start_date=triplex_acquisition_date,
            end_date=triplex_acquisition_date,
        ),
        Entity(
            name="Inspection_Triple",
            amount=-1200,
            start_date=triplex_acquisition_date,
            end_date=triplex_acquisition_date,
        ),
        Entity(
            name="Notary_Triple",
            amount=-1200,
            start_date=triplex_acquisition_date,
            end_date=triplex_acquisition_date,
        ),
        Entity(
            name="Moving_Triple",
            amount=-1200,
            start_date=triplex_acquisition_date,
            end_date=triplex_acquisition_date,
        ),
        Entity(
            name="Taxes_Triple",
            amount=-450,
            annual_inflation_rate=4,
            start_date=triplex_acquisition_date,
        ),
        Entity(
            name="Recurring_Renovations_Triple",
            amount=-650,
            annual_inflation_rate=INFLATION_RATE,
            start_date=triplex_acquisition_date,
        ),
        Entity(
            name="Rents_Triple",
            amount=1300 * 3,
            annual_inflation_rate=4,
            start_date=triplex_acquisition_date,
        ),
    ],
    loan=Loan(
        name="Triplex Loan",
        amount=800_000,
        annual_interest_rate=6.5,
        term_in_year=30,
        annual_inflation_rate=INFLATION_RATE,
        start_date=triplex_acquisition_date,
    ),
    start_date=triplex_acquisition_date,
)


house_acquisition_date = "2024-11-01"
house = RealEstate(
    name="House",
    amount=800_000,
    cashdown=200_000,
    annual_expected_return=4,
    acquisition_entities=[
        Entity(
            name="Cashdown_House",
            amount=-200_000,
            start_date=house_acquisition_date,
            end_date=house_acquisition_date,
        ),
        Entity(
            name="Renovations_House",
            amount=-12_000,
            start_date=house_acquisition_date,
            end_date=house_acquisition_date,
        ),
        Entity(
            name="Welcome Taxe_House",
            amount=-12_000,
            start_date=house_acquisition_date,
            end_date=house_acquisition_date,
        ),
        Entity(
            name="Inspection_House",
            amount=-1200,
            start_date=house_acquisition_date,
            end_date=house_acquisition_date,
        ),
        Entity(
            name="Notary_House",
            amount=-1200,
            start_date=house_acquisition_date,
            end_date=house_acquisition_date,
        ),
        Entity(
            name="Moving_House",
            amount=-1200,
            start_date=house_acquisition_date,
            end_date=house_acquisition_date,
        ),
        Entity(
            name="Recurring_Renovations_House",
            amount=-650,
            annual_inflation_rate=4,
            start_date=house_acquisition_date,
        ),
        Entity(
            name="Taxes_House",
            amount=-450,
            annual_inflation_rate=4,
            start_date=house_acquisition_date,
        ),
    ],
    loan=Loan(
        name="House Loan",
        amount=600_000,
        annual_interest_rate=6.1,
        term_in_year=25,
        annual_inflation_rate=0,
        start_date=house_acquisition_date,
    ),
    start_date=house_acquisition_date,
)


# BUDGET
# Income
salary_1 = Entity(
    name="Salary 1", amount=8_000, annual_inflation_rate=4, start_date="2023-10-01"
)

salary_2 = Entity(
    name="Salary 2",
    amount=6_000,
    annual_inflation_rate=4,
    start_date="2023-10-01",
)

# Expenses
rent = Entity(
    name="Rent",
    amount=-1400,
    annual_inflation_rate=5,
    start_date="2023-10-01",
    end_date="2024-12-01",
)
amenities = Entity(
    name="Amenities", amount=-600, annual_inflation_rate=4, start_date="2023-10-01"
)
transport = Entity(
    name="Transport", amount=-500, annual_inflation_rate=10, start_date="2023-10-01"
)
entertainment = Entity(
    name="Entertainment", amount=-650, annual_inflation_rate=4, start_date="2023-10-01"
)
travelling = Entity(
    name="travelling", amount=-1000, annual_inflation_rate=4, start_date="2023-10-01"
)
food = Entity(
    name="Food", amount=-800, annual_inflation_rate=4, start_date="2023-10-01"
)
other = Entity(
    name="Other", amount=-500, annual_inflation_rate=2, start_date="2023-10-01"
)

ENTITIES = [
    salary_1,
    salary_2,
    rent,
    amenities,
    transport,
    entertainment,
    travelling,
    food,
    other,
]

ASSETS_LIAIBILITIES = [bank_account, house, triplex]
