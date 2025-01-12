from flask import Flask,jsonify,request,render_template
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(app.instance_path, 'books.db')}"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////books.db'  # SQLite URI for file-based database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Book {self.name}, Author {self.Author}>"


books = []


@app.route("/", methods = ["GET"])
def home():
    return render_template('index.html')



@app.route("/api/v1/books",methods = ["GET"])
def get_books():
    books_db= Book.query.all();
    books.clear()
    for book in books_db:
        x = {"id":book.id,"name":book.name,"Author":book.author}
        books.append(x)
    return jsonify(books)

@app.route("/api/v1/book/<int:book_id>",methods=["GET"])
def get_book(book_id):
    try:
        data= db.session.get(Book,book_id)
        book={"id":data.id,"name":data.name,"Author":data.author}
        return jsonify(book)
    except Exception as e:
        return jsonify({"error" : "Book not found"}),404



# Using Query Param
@app.route("/api/v1/get_book_by_id",methods=["GET"])
def get_book_by_id():
    try:
        data=db.session.get(Book,request.args['id'])
        book={"id":data.id,"name":data.name,"Author":data.author}
        return jsonify(book)
    except Exception as e:
        return jsonify({"error" : "Book not found"}),404
    

@app.route("/api/v1/get_book_by_author",methods=["GET"])
def get_book_by_author():
    books.clear()
    try:
        data = Book.query.filter_by(author=request.args['Author']).all()
        for book in data:
            x={"id":book.id,"name":book.name,"Author":book.author}
            books.append(x)
        if(books):
            return jsonify(books)
        else:
            raise KeyError("")
    except Exception as e:
        return jsonify({"error" : "Book not found"}),404
    

@app.route("/api/v1/get_book_by_name",methods=["GET"])
def get_book_by_name():
    books.clear()
    try:
        data = Book.query.filter_by(name=request.args['name']).all()
        for book in data:
            x={"id":book.id,"name":book.name,"Author":book.author}
            books.append(x)
        if(books):
            return jsonify(books)
        else:
            raise KeyError("")
    except Exception as e:
        return jsonify({"error" : "Book not found"}),404


@app.route("/api/v1/addbooks",methods = ["POST"])
def add_book():
    # Process 1:
    # new_book = {
    #     "id": request.json["id"],
    #     "name": request.json["name"],
    #     "Author": request.json["Author"]
    # }
    # Process 2:
    if((request.json.get("id")!=None)and(request.json.get("name")!=None)and(request.json.get("Author")!=None)):
        id = request.json["id"]
        name = request.json['name']
        Author =request.json['Author']
        try:
            new_book=Book(id=id,name=name,author=Author)
            db.session.add(new_book)
            db.session.commit()
            return jsonify({"message":"Book added successfully"})
        except Exception as e:
            return jsonify({"error":"Already exists with same id"}),400
    else:
        return jsonify({"error":"Missing fields"}),400


@app.route("/api/v1/delete/<int:id>", methods = ["DELETE"])
def delete(id):
    try:
        book = db.session.get(Book,id)
        db.session.delete(book)
        db.session.commit()
        return jsonify({"message" : "Book deleted sucessfully"})
    except:
        return jsonify({"error": "Book not found"}),404


@app.route("/api/v1/update_book/<int:id>",methods=["PUT"])
def update(id):
    try:
        if(request.json.get('Author')is None or request.json.get('name')is None ):
            return jsonify({"error":"Missing fields"}),400
        book = db.session.get(Book,id)
        db.session.delete(book)
        db.session.commit()
        book = Book(id=id,name=request.json.get('name'),author=request.json.get('Author'))
        db.session.add(book)
        db.session.commit()
        return jsonify({"id":book.id,"name":book.name,"Author":book.author})
    except:
        return jsonify({"error":"Book not found"}),404


@app.route("/api/v1/update_book_details/<int:id>",methods=["PATCH"])
def update_details(id):
    if(request.json.get('Author')!=None and request.json.get('name')!=None):
        book = db.session.get(Book,id)
        book.name= request.json['name']
        book.author = request.json['Author']
        db.session.commit()
        return jsonify({"id":book.id,"name":book.name,"Author":book.author})
    elif(request.json.get('Author') is not None):
        book = db.session.get(Book,id)
        book.author = request.json['Author']
        db.session.commit()
        return jsonify({"id":book.id,"name":book.name,"Author":book.author})
    elif(request.json.get('name') is not None):
           book = db.session.get(Book,id)
           book.name= request.json['name']
           db.session.commit()
           return jsonify({"id":book.id,"name":book.name,"Author":book.author})    
    return jsonify({"error": "Bad request"}),400

if __name__=="__main__":
    app.run(debug=True)