"""
Author: Scott Urbanski (code modified from Caleb Curry tutorial)
Date Modified: February 7, 2025
Project: application.py
Project Description: This project allows the user to send requests to add or delete books in a database.
"""


from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)



class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bookName = db.Column(db.String(120), unique=True, nullable = False)
    bookAuthor = db.Column(db.String(80))
    bookPublisher = db.Column(db.String(80))

    def __repr__(self):
        return f"{self.bookName}, {self.bookAuthor}, {self.bookPublisher}"

@app.route('/')
def index():
    return 'Hello!'

@app.route('/books')
def get_books():
    theBooks = Book.query.all()
    output = []
    for book in theBooks:
        book_data = {'Book Name': book.bookName, 'Book Author': book.bookAuthor, 'Book Publisher': book.bookPublisher}
        output.append(book_data)
    return {"books ": output}

@app.route('/books/<id>')
def get_book(id):
    book = Book.query.get_or_404(id)
    return {"Book Name": book.bookName, "Book Author": book.bookAuthor, "Book Publisher": book.bookPublisher}

@app.route('/books', methods=['POST'])
def add_book():
    book = Book(bookName=request.json["bookName"], bookAuthor=request.json["bookAuthor"], bookPublisher=request.json["bookPublisher"])
    db.session.add(book)
    db.session.commit()

@app.route('/books/<id>', method=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if book is None:
        return {"error": "not found"}
    else:
        db.session.delete(book)
        db.session.commit()