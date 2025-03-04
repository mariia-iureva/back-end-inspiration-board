import pytest
from app import create_app
from app import db
from app.models.card import Card
from app.models.board import Board


@pytest.fixture
def app():
    # create the app with a test config dictionary
    app = create_app({"TESTING": True})

    with app.app_context():
        db.create_all()
        yield app

    # close and remove the temporary database
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def one_board(app):
    new_board = Board(title="Reminders", owner="Thao")
    db.session.add(new_board)
    db.session.commit()

@pytest.fixture
def three_boards(app):
    db.session.add_all([
        Board(title="Reminders", owner="Thao"),
        Board(title="Pick Me Up Quotes", owner="Masha"),
        Board(title="Inspiration", owner="Neema")
    ])
    db.session.commit()

@pytest.fixture
def one_card_to_one_board(app, one_board):
    new_card = Card(message="Finish Inspiration Board", likes_count=0, board_id=1)
    board = Board.query.first()
    db.session.add(new_card)
    board.cards.append(new_card)
    db.session.commit()