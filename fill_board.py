from monopoly.app import app
from monopoly.database.dao import CardDAO


def initialize_board():
    CardDAO.get_or_create(id=1, title='Go')
    CardDAO.get_or_create(id=2, title='Mediterranean Avenue', color='Brown', cost=60, rental_price=10)
    CardDAO.get_or_create(id=3, title='Community Chest')
    CardDAO.get_or_create(id=4, title='Baltic Avenue', color='Brown', cost=60, rental_price=60)
    CardDAO.get_or_create(id=5, title='Income Tax')
    CardDAO.get_or_create(id=6, title='Reading Railroad', color='Railroad', cost=200)
    CardDAO.get_or_create(id=7, title='Oriental Avenue', color='Light Blue', cost=100, rental_price=90)
    CardDAO.get_or_create(id=8, title='Community Chest')
    CardDAO.get_or_create(id=9, title='Vermont Avenue', color='Light Blue', cost=100, rental_price=90)
    CardDAO.get_or_create(id=10, title='Connecticut Avenue', color='Light Blue', cost=120, rental_price=100)
    CardDAO.get_or_create(id=11, title='Jail/Visiting Jail')
    CardDAO.get_or_create(id=12, title='St. Charles Place', color='Pink', cost=140, rental_price=150)
    CardDAO.get_or_create(id=13, title='Electric Company', color='Utilities', cost=150)
    CardDAO.get_or_create(id=14, title='States Avenue', color='Pink', cost=140, rental_price=150)
    CardDAO.get_or_create(id=15, title='Virginia Avenue', color='Pink', cost=160, rental_price=180)
    CardDAO.get_or_create(id=16, title='Pennsylvania Railroad', color='Railroad', cost=200)
    CardDAO.get_or_create(id=17, title='St. James Place', color='Orange', cost=180, rental_price=200)
    CardDAO.get_or_create(id=18, title='Tennessee Avenue', color='Orange', cost=180, rental_price=200)
    CardDAO.get_or_create(id=19, title='New York Avenue', color='Orange', cost=200, rental_price=220)
    CardDAO.get_or_create(id=20, title='Free Parking')
    CardDAO.get_or_create(id=21, title='Kentucky Avenue', color='Red', cost=220, rental_price=220)
    CardDAO.get_or_create(id=22, title='Indiana Avenue', color='Red', cost=220, rental_price=250)
    CardDAO.get_or_create(id=23, title='Illinois Avenue', color='Red', cost=240, rental_price=300)
    CardDAO.get_or_create(id=24, title='B.& O. Railroad', color='Railroad', cost=200)
    CardDAO.get_or_create(id=25, title='Atlantic Avenue', color='Yellow', cost=260, rental_price=330)
    CardDAO.get_or_create(id=26, title='Ventnor Avenue', color='Yellow', cost=260, rental_price=330)
    CardDAO.get_or_create(id=27, title='Water Works', color='Utilities', cost=150)
    CardDAO.get_or_create(id=28, title='Marvin Gardens', color='Yellow', cost=280, rental_price=360)
    CardDAO.get_or_create(id=29, title='Go to Jail')
    CardDAO.get_or_create(id=30, title='Pacific Avenue', color='Green', cost=300, rental_price=390)
    CardDAO.get_or_create(id=31, title='North Carolina Avenue', color='Green', cost=140, rental_price=390)
    CardDAO.get_or_create(id=32, title='Pennsylvania Avenue', color='Green', cost=300, rental_price=150)
    CardDAO.get_or_create(id=33, title='Short Line', color='Railroad', cost=200)
    CardDAO.get_or_create(id=34, title='Park Place', color='Blue', cost=350, rental_price=500)
    CardDAO.get_or_create(id=35, title='Luxury Tax')
    CardDAO.get_or_create(id=36, title='Boardwalk', cost=400, rental_price=600)


if __name__ == "__main__":
    with app.app_context():
        initialize_board()
