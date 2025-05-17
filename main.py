import argparse
import os
from auth import login, register_member
from librarian import add_book, delete_book, register_member_cli, issue_book, return_book, overdue_report
from member import search_catalog, check_availability, view_history

def main():
    parser = argparse.ArgumentParser(description="Library Management System")
    parser.add_argument("--data-dir", default="data", help="Directory for CSV data files")
    args = parser.parse_args()
    data_dir = args.data_dir
    # Define CSV file paths
    books_file = os.path.join(data_dir, "books.csv")
    members_file = os.path.join(data_dir, "members.csv")
    loans_file = os.path.join(data_dir, "loans.csv")
    # Initialize CSVs with headers if needed
    from storage import ensure_csv
    ensure_csv(books_file, ["ISBN", "Title", "Author", "Year", "CopiesTotal", "CopiesAvailable"])
    ensure_csv(members_file, ["MemberID", "Name", "Email", "PasswordHash", "Role"])
    ensure_csv(loans_file, ["LoanID", "MemberID", "ISBN", "IssueDate", "DueDate", "ReturnDate"])

    session = {"user": None}
    print("Welcome to the Library Management System.")
    while True:
        if session["user"] is None:
            choice = input("\nEnter 'r' to register, 'l' to login, or 'q' to quit: ").lower()
            if choice == 'r':
                user = register_member(members_file)
                if user:
                    session["user"] = user
            elif choice == 'l':
                user = login(members_file)
                if user:
                    session["user"] = user
            elif choice == 'q':
                print("Exiting.")
                break
            else:
                print("Invalid option.")
        else:
            user = session["user"]
            print(f"\nLogged in as {user.name} ({user.role})")
            if user.role == "Librarian":
                print("Actions: [A]dd book, [D]elete book, [R]egister member, [I]ssue book, [T]Return book, [O]verdue report, [L]ogout")
                action = input("Choose action: ").lower()
                if action == 'a':
                    add_book(books_file)
                elif action == 'd':
                    delete_book(books_file, loans_file)
                elif action == 'r':
                    register_member_cli(members_file)
                elif action == 'i':
                    issue_book(books_file, loans_file, members_file)
                elif action == 't':
                    return_book(books_file, loans_file)
                elif action == 'o':
                    overdue_report(loans_file)
                elif action == 'l':
                    session["user"] = None
                else:
                    print("Invalid action.")
            else:  # Member role
                print("Actions: [S]earch, [C]heck availability, [B]orrow book, [H]istory, [L]ogout")
                action = input("Choose action: ").lower()
                if action == 's':
                    search_catalog(books_file)
                elif action == 'c':
                    check_availability(books_file)
                elif action == 'b':
                    print("Feature: Borrow Book (issues a book to you).")
                    issue_book(books_file, loans_file, members_file)
                elif action == 'h':
                    view_history(loans_file, user)
                elif action == 'l':
                    session["user"] = None
                else:
                    print("Invalid action.")

if __name__ == "__main__":
    main()
# This is the main entry point for the library management system.