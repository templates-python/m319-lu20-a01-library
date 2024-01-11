import pytest
from library import show_balance, read_int, read_date, read_rental, add_rental, init_books
from rental import Rental
from datetime import datetime

@pytest.fixture
def sample_books_filled():
    books = {
        "LOTR 1": [
            Rental(datetime(2023, 1, 5), datetime(2023, 3, 6), 60),
        ],
        "LOTR 2": [
            Rental(datetime(2023, 1, 6), datetime(2023, 2, 23), 49),
        ],
        "LOTR 3": [
            Rental(datetime(2023, 1, 6), datetime(2023, 2, 23), 49),
            Rental(datetime(2023, 1, 6), datetime(2023, 2, 23), 49),
        ],
    }
    return books

@pytest.fixture
def empty_books():
    return {
        "LOTR 1": [],
        "LOTR 2": [],
        "LOTR 3": [],
    }

@pytest.fixture
def sample_books():
    books = {
        "LOTR 1": [],
        "LOTR 2": [],
        "LOTR 3": [],
    }
    return books
def test_show_balance(sample_books_filled, capsys):
    show_balance(sample_books_filled)
    captured = capsys.readouterr()

    expected_output = """Statement for LOTR 1
  - 05.01.2023: CHF 205.5
Total: CHF 205.5
Statement for LOTR 2
  - 06.01.2023: CHF 165.3
Total: CHF 165.3
Statement for LOTR 3
  - 06.01.2023: CHF 165.3
  - 06.01.2023: CHF 165.3
Total: CHF 330.6
"""
    assert captured.out == expected_output


def test_init_books(empty_books):
    books = init_books()
    assert books == empty_books

def test_read_rental(monkeypatch):
    inputs = iter(['05.01.2023','60','06.03.2023','n'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    rental = read_rental()
    assert rental.rental_date == datetime(2023, 1, 5)
    assert rental.num_rental_days == 60
    assert rental.return_date == datetime(2023, 3, 6)

def test_add_rental_empty_books(empty_books, monkeypatch):
    inputs = iter(['LOTR 1','05.01.2023','60','06.03.2023','n'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    add_rental(empty_books)
    assert len(empty_books["LOTR 1"]) == 1
    assert len(empty_books["LOTR 2"]) == 0

def test_add_rental_existing_books(sample_books_filled, monkeypatch):
    inputs = iter(['LOTR 1','05.01.2023','60','06.03.2023','n'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    add_rental(sample_books_filled)
    assert len(sample_books_filled["LOTR 1"]) == 2
    assert len(sample_books_filled["LOTR 2"]) == 1
    assert len(sample_books_filled["LOTR 3"]) == 2

def test_read_int_valid_input(monkeypatch):
    inputs = iter(['5'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    value = read_int("Enter a number: ")
    assert value == 5

def test_read_int_invalid_input(monkeypatch, capsys):
    inputs = iter(['abs','-5','1'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    value = read_int("Enter a number: ")
    captured = capsys.readouterr()
    assert value == 1  # Should return 0 for invalid input
    assert captured.out == "Please enter a positive number.\nPlease enter a positive number.\n"

def test_read_date_valid_input(monkeypatch, capsys):
    # Mocking user input with valid date format
    inputs = iter(['05.01.2023'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    date = read_date("Enter a date (dd.mm.yyyy): ")
    captured = capsys.readouterr()
    assert date == datetime(2023, 1, 5)  # Should return the valid date
    assert captured.out == ""  # No error message should be printed

def test_read_date_invalid_input(monkeypatch, capsys):
    # Mocking user input with invalid date format
    inputs = iter(['abc', '01/05/2023', '05.01.2023'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    date = read_date("Enter a date (dd.mm.yyyy): ")
    captured = capsys.readouterr()
    assert date == datetime(2023, 1, 5)  # Should return the valid date
    assert captured.out == "Please enter a valid date.\nPlease enter a valid date.\n"  # Error messages should be printed