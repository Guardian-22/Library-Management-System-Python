from storage import load_books, load_loans
from models import Loan

def search_catalog(books_file):
    books = load_books(books_file)
    term = input("Search by title or author: ").lower()
    found = [b for b in books if term in b.title.lower() or term in b.author.lower()]
    if not found:
        print("No matching books found.")
        return
    for b in found:
        print(f"{b.isbn}: {b.title} by {b.author} ({b.year}) - Available: {b.copies_available}")

def check_availability(books_file):
    isbn = input("Enter ISBN to check: ")
    books = load_books(books_file)
    book = next((b for b in books if b.isbn == isbn), None)
    if book:
        print(f"'{book.title}' copies available: {book.copies_available}")
    else:
        print("Book not found.")

def borrow_book(books_file, loans_file, member):
    # This is same as issuing a book but for the logged-in member
    from librarian import issue_book
    # Override input prompts for member usage:
    print(f"Issuing book to you, {member.name} (MemberID: {member.member_id})")
    # simulate input by overriding or by refactoring issue_book logic to accept parameters
    issue_book(books_file, loans_file, None)

def view_history(loans_file, member):
    loans = load_loans(loans_file)
    member_loans = [l for l in loans if l.member_id == member.member_id]
    if not member_loans:
        print("No loan history.")
        return
    print(f"{'LoanID':<6} {'ISBN':<13} {'IssueDate':<12} {'DueDate':<12} {'ReturnDate':<12}")
    for l in member_loans:
        ret = l.return_date if l.return_date else "Not returned"
        print(f"{l.loan_id:<6} {l.isbn:<13} {l.issue_date:<12} {l.due_date:<12} {ret:<12}")
