import os
import csv
from models import Book, Member, Loan

def ensure_csv(file_path, headers):
    """Ensure the CSV file exists; if not, create it with headers."""
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)

def load_books(file_path):
    ensure_csv(file_path, Book.csv_headers())
    books = []
    with open(file_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            books.append(Book(
                isbn=row["ISBN"],
                title=row["Title"],
                author=row["Author"],
                year=row["Year"],
                copies_total=int(row["CopiesTotal"]),
                copies_available=int(row["CopiesAvailable"])
            ))
    return books

def save_books(file_path, books):
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(Book.csv_headers())
        for b in books:
            writer.writerow([b.isbn, b.title, b.author, b.year, b.copies_total, b.copies_available])

def load_members(file_path):
    ensure_csv(file_path, Member.csv_headers())
    members = []
    with open(file_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            members.append(Member(
                member_id=row["MemberID"],
                name=row["Name"],
                email=row["Email"],
                password_hash=row["PasswordHash"],
                role=row["Role"]
            ))
    return members

def save_members(file_path, members):
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(Member.csv_headers())
        for m in members:
            writer.writerow([m.member_id, m.name, m.email, m.password_hash, m.role])

def load_loans(file_path):
    ensure_csv(file_path, Loan.csv_headers())
    loans = []
    with open(file_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            loans.append(Loan(
                loan_id=row["LoanID"],
                member_id=row["MemberID"],
                isbn=row["ISBN"],
                issue_date=row["IssueDate"],
                due_date=row["DueDate"],
                return_date=row["ReturnDate"]
            ))
    return loans

def save_loans(file_path, loans):
    with open(file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(Loan.csv_headers())
        for l in loans:
            writer.writerow([l.loan_id, l.member_id, l.isbn, l.issue_date, l.due_date, l.return_date])
