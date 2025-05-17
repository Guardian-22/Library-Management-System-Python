from dataclasses import dataclass, asdict

@dataclass
class Book:
    isbn: str
    title: str
    author: str
    year: str
    copies_total: int
    copies_available: int

    @staticmethod
    def csv_headers():
        return ["ISBN", "Title", "Author", "Year", "CopiesTotal", "CopiesAvailable"]

@dataclass
class Member:
    member_id: str
    name: str
    email: str
    password_hash: str
    role: str  # "Librarian" or "Member"

    @staticmethod
    def csv_headers():
        return ["MemberID", "Name", "Email", "PasswordHash", "Role"]

@dataclass
class Loan:
    loan_id: str
    member_id: str
    isbn: str
    issue_date: str  # ISO date string
    due_date: str    # ISO date string
    return_date: str  # ISO date string or empty if not returned

    @staticmethod
    def csv_headers():
        return ["LoanID", "MemberID", "ISBN", "IssueDate", "DueDate", "ReturnDate"]
