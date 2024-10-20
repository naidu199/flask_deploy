from flask import Flask, request, jsonify,abort
from flask_cors import CORS
import json
app=Flask(__name__)
CORS(app)

with open('books.json', 'r') as f:
    books = json.load(f)
def save_books(data):
    with open('books.json', 'w') as f:
        json.dump(data, f, indent=4)
@app.route('/<name>')
def index(name):
    return 'Welcome {}'.format(name)
@app.route('/books',methods=['GET'])
def get_books():
    return jsonify(books)
@app.route('/books/<int:book_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_book(book_id):
    # Find the book by book_id
    book = next((book for book in books if book['book_id'] == book_id), None)

    # Handle GET request to fetch the book by ID
    if request.method == 'GET':
        if book is None:
            abort(404, description="Book not found")
        return jsonify(book)

    # Handle PUT request to update the book by ID
    if request.method == 'PUT':
        if not request.json:
            abort(400, description="Invalid input: Must provide a JSON body")

        if 'name' in request.json:
            book['name'] = request.json['name']
        if 'author' in request.json:
            book['author'] = request.json['author']
        if 'language' in request.json:
            book['language'] = request.json['language']

        save_books(books)
        return jsonify(book)

    # Handle DELETE request to delete the book by ID
    if request.method == 'DELETE':
        if book is None:
            abort(404, description="Book not found")
        books.remove(book)
        save_books(books)
        return jsonify({'message': 'Book deleted'}), 200

# @app.route('/books/<int:book_id>',methods=['GET'])
# def get_book(book_id):
#     book = next((book for book in books if book['book_id'] == book_id), None)
#     if book is None:
#         abort(404,description="Book not found")
#     return jsonify(book)
@app.route('/books',methods=['POST'])
def add_book():

    if not request.json or not 'name' in request.json:
        abort(400, description="Invalid input: Must include 'name' in the JSON request")
    new_book={
		'book_id':books[-1]['book_id']+1 if books else 1,
		'name':request.json.get('name'),
		'author':request.json.get('author',"Unknown"),
		'language':request.json.get('language',"Unknown")
	}
    books.append(new_book)
    save_books(books)
    return jsonify(new_book), 201
if(__name__=='__main__'):
    app.run(host='0.0.0.0',port=5000)
