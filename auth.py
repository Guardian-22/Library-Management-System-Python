import bcrypt
from storage import load_members, save_members
from models import Member

def hash_password(plain):
    return bcrypt.hashpw(plain.encode('utf-8'), bcrypt.gensalt())

def check_password(plain, hashed):
    return bcrypt.checkpw(plain.encode('utf-8'), hashed)

def register_member(members_file):
    members = load_members(members_file)
    member_id = input("Enter new Member ID: ")
    if any(m.member_id == member_id for m in members):
        print("Error: Member ID already exists.")
        return None
    name = input("Enter name: ")
    email = input("Enter email: ")
    pwd = input("Enter password: ")
    pwd_confirm = input("Confirm password: ")
    if pwd != pwd_confirm:
        print("Error: Passwords do not match.")
        return None
    password_hash = hash_password(pwd)
    # First member can be made librarian
    role = "Member"
    if not any(m.role == "Librarian" for m in members):
        choice = input("First user! Make this user a Librarian? (y/n): ")
        if choice.lower().startswith('y'):
            role = "Librarian"
    new_member = Member(member_id=member_id, name=name, email=email,
                        password_hash=password_hash, role=role)
    members.append(new_member)
    save_members(members_file, members)
    print(f"Member {name} registered successfully with role {role}.")
    return new_member

def login(members_file):
    members = load_members(members_file)
    member_id = input("Member ID: ")
    password = input("Password: ")
    for m in members:
        if m.member_id == member_id:
            if check_password(password, m.password_hash.encode('utf-8')):
                print(f"Login successful. Welcome, {m.name} ({m.role}).")
                return m
            else:
                print("Error: Incorrect password.")
                return None
    print("Error: Member ID not found.")
    return None
