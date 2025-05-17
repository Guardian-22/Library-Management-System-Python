import datetime
from storage import load_books, save_books, load_loans, save_loans, load_members, save_members
from models import Book, Loan, Member
from auth import register_member


def add_book(books_file):
    books = load_books(books_file)
    isbn = input("ISBN: ")
    if any(b.isbn == isbn for b in books):
        print("Error: Book with this ISBN already exists.")
        return
    title = input("Title: ")
    author = input("Author: ")
    year = input("Year: ")
    try:
        copies = int(input("Copies: "))
        if copies < 0:
            print("Error: Copies cannot be negative.")
            return
    except ValueError:
        print("Error: Invalid number of copies.")
        return
    new_book = Book(isbn=isbn, title=title, author=author, year=year,
                    copies_total=copies, copies_available=copies)
    books.append(new_book)
    save_books(books_file, books)
    print(f"Book '{title}' added.")

def delete_book(books_file, loans_file):
    books = load_books(books_file)
    loans = load_loans(loans_file)
    isbn = input("Enter ISBN to delete: ")
    for b in books:
        if b.isbn == isbn:
            # Check if any active loans for this book
            if any(l.isbn == isbn and not l.return_date for l in loans):
                print("Error: Book is currently loaned out.")
                return
            books.remove(b)
            save_books(books_file, books)
            print(f"Book {b.title} deleted.")
            return
    print("Error: Book not found.")

def register_member_cli(members_file):
    new_member = register_member(members_file)
    # Optionally more processing

def issue_book(books_file, loans_file, members_file):
    books = load_books(books_file)
    members = load_members(members_file)
    loans = load_loans(loans_file)
    member_id = input("Enter Member ID to issue to: ")
    member = next((m for m in members if m.member_id == member_id), None)
    if not member:
        print("Error: Member not found.")
        return
    isbn = input("Enter ISBN to issue: ")
    book = next((b for b in books if b.isbn == isbn), None)
    if not book:
        print("Error: Book not found.")
        return
    if book.copies_available <= 0:
        print("No copies available.")
        return
    # Update book availability
    book.copies_available -= 1
    # Create loan record
    issue_date = datetime.date.today()
    due_date = issue_date + datetime.timedelta(days=14)  # 14-day due date:contentReference[oaicite:9]{index=9}
    loan_id = str(len(loans) + 1)
    loan = Loan(loan_id=loan_id, member_id=member_id,
                isbn=isbn,
                issue_date=str(issue_date),
                due_date=str(due_date),
                return_date="")
    loans.append(loan)
    save_books(books_file, books)
    save_loans(loans_file, loans)
    print(f"Issued '{book.title}' to {member.name}. Due on {due_date}.")

def return_book(books_file, loans_file):
    books = load_books(books_file)
    loans = load_loans(loans_file)
    loan_id = input("Enter Loan ID to return: ")
    loan = next((l for l in loans if l.loan_id == loan_id), None)
    if not loan:
        print("Error: Loan not found.")
        return
    if loan.return_date:
        print("Book already returned.")
        return
    # Set return date
    return_date = datetime.date.today()
    loan.return_date = str(return_date)
    # Update book availability
    book = next((b for b in books if b.isbn == loan.isbn), None)
    if book:
        book.copies_available += 1
    save_books(books_file, books)
    save_loans(loans_file, loans)
    print(f"Loan {loan_id} marked as returned on {return_date}.")

def overdue_report(loans_file):
    loans = load_loans(loans_file)
    today = datetime.date.today()
    overdue_loans = [l for l in loans if not l.return_date and l.due_date < str(today)]
    if not overdue_loans:
        print("No overdue loans.")
        return
    print(f"{'LoanID':<6} {'MemberID':<10} {'ISBN':<13} {'DueDate':<10}")
    for l in overdue_loans:
        print(f"{l.loan_id:<6} {l.member_id:<10} {l.isbn:<13} {l.due_date:<10}")
