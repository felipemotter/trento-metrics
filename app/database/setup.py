# database/setup.py
from database.database import engine, SessionLocal
from database.models import Base, User, Group
import bcrypt

def create_tables():
    Base.metadata.create_all(bind=engine)

def create_group(name):
    session = SessionLocal()
    group = Group(name=name)
    session.add(group)
    session.commit()
    session.close()

def create_user(name, username, password, group_names):
    session = SessionLocal()
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user = User(
        name=name,
        username=username,
        password_hash=password_hash.decode('utf-8')
    )

    groups = session.query(Group).filter(Group.name.in_(group_names)).all()
    user.groups.extend(groups)

    session.add(user)
    session.commit()
    session.close()

# database/setup.py (adicionando criação do grupo admin)
if __name__ == '__main__':
    create_tables()
    create_group('admin')  # Adicionando o grupo admin

    create_user('Admin', 'admin', 'senha1234', ['admin'])  # Criando um usuário admin

