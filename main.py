
import streamlit as st
import json

class BookCollection:
    """A class to manage a collection of books, allowing users to store and organize their reading materials."""

    def __init__(self):
        """Initialize a new book collection with an empty list and set up file storage."""
        self.book_list = []
        self.storage_file = "books_data.json"
        self.read_from_file()

    def read_from_file(self):
        """Load saved books from a JSON file into memory."""
        try:
            with open(self.storage_file, "r") as file:
                self.book_list = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.book_list = []

    def save_to_file(self):
        """Store the current book collection to a JSON file."""
        with open(self.storage_file, "w") as file:
            json.dump(self.book_list, file, indent=4)

    def create_new_book(self, title, author, year, genre, read):
        """Add a new book to the collection."""
        new_book = {
            "title": title,
            "author": author,
            "year": year,
            "genre": genre,
            "read": read,
        }

        self.book_list.append(new_book)
        self.save_to_file()

    def delete_book(self, title):
        """Remove a book from the collection using its title."""
        for book in self.book_list:
            if book["title"].lower() == title.lower():
                self.book_list.remove(book)
                self.save_to_file()
                return True
        return False

    def find_book(self, search_text):
        """Search for books in the collection by title or author name."""
        return [
            book
            for book in self.book_list
            if search_text.lower() in book["title"].lower()
            or search_text.lower() in book["author"].lower()
        ]

    def update_book(self, old_title, new_title, new_author, new_year, new_genre, new_read):
        """Modify the details of an existing book in the collection."""
        for book in self.book_list:
            if book["title"].lower() == old_title.lower():
                book["title"] = new_title or book["title"]
                book["author"] = new_author or book["author"]
                book["year"] = new_year or book["year"]
                book["genre"] = new_genre or book["genre"]
                book["read"] = new_read if new_read is not None else book["read"]
                self.save_to_file()
                return True
        return False

    def show_all_books(self):
        """Return all books in the collection."""
        return self.book_list

    def show_reading_progress(self):
        """Calculate and return reading progress statistics."""
        total_books = len(self.book_list)
        completed_books = sum(1 for book in self.book_list if book["read"])
        completion_rate = (completed_books / total_books * 100) if total_books > 0 else 0
        return total_books, completion_rate


# Initialize book collection manager
book_manager = BookCollection()

# Streamlit UI Design
st.title("📚 Book Collection Manager 📚")
st.sidebar.header("Manage Your Book Collection")

menu = ["Add a Book", "Remove a Book", "Search Books", "Update a Book", "View All Books", "Reading Progress", "Exit"]
choice = st.sidebar.selectbox("Select an Option", menu)

if choice == "Add a Book":
    st.subheader("Add a New Book")
    with st.form(key="add_book_form"):
        title = st.text_input("Book Title")
        author = st.text_input("Author")
        year = st.text_input("Year of Publication")
        genre = st.text_input("Genre")
        read = st.radio("Have you read this book?", ("Yes", "No"))
        submitted = st.form_submit_button("Add Book")
        if submitted:
            read_bool = True if read == "Yes" else False
            book_manager.create_new_book(title, author, year, genre, read_bool)
            st.success("Book added successfully!")

elif choice == "Remove a Book":
    st.subheader("Remove a Book")
    title_to_remove = st.text_input("Enter the title of the book to remove")
    if st.button("Remove Book"):
        if book_manager.delete_book(title_to_remove):
            st.success(f"Book '{title_to_remove}' removed successfully!")
        else:
            st.error("Book not found!")

elif choice == "Search Books":
    st.subheader("Search Books")
    search_term = st.text_input("Enter search term (title or author)")
    if st.button("Search"):
        results = book_manager.find_book(search_term)
        if results:
            for idx, book in enumerate(results, 1):
                status = "Read" if book["read"] else "Unread"
                st.write(f"{idx}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status}")
        else:
            st.warning("No books found.")

elif choice == "Update a Book":
    st.subheader("Update Book Details")
    old_title = st.text_input("Enter the title of the book to update")
    new_title = st.text_input("New Title (Leave blank to keep current)")
    new_author = st.text_input("New Author (Leave blank to keep current)")
    new_year = st.text_input("New Year (Leave blank to keep current)")
    new_genre = st.text_input("New Genre (Leave blank to keep current)")
    new_read = st.radio("New Reading Status", ("Leave unchanged", "Read", "Unread"))

    if st.button("Update Book"):
        read_bool = None
        if new_read == "Read":
            read_bool = True
        elif new_read == "Unread":
            read_bool = False

        if book_manager.update_book(old_title, new_title, new_author, new_year, new_genre, read_bool):
            st.success(f"Book '{old_title}' updated successfully!")
        else:
            st.error("Book not found.")

elif choice == "View All Books":
    st.subheader("Your Book Collection")
    books = book_manager.show_all_books()
    if books:
        for idx, book in enumerate(books, 1):
            status = "Read" if book["read"] else "Unread"
            st.write(f"{idx}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status}")
    else:
        st.warning("Your collection is empty.")

elif choice == "Reading Progress":
    st.subheader("Reading Progress")
    total_books, progress = book_manager.show_reading_progress()
    st.write(f"Total books: {total_books}")
    st.write(f"Reading Progress: {progress:.2f}%")

elif choice == "Exit":
    st.stop()