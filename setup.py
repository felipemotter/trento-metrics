from database import engine, SessionLocal
from models import Base, User, Group
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

if __name__ == '__main__':
    create_tables()
    # Criar grupos
    create_group('grupo1')
    create_group('grupo2')
    create_group('grupo3')

    # Criar usuários
    create_user('Alice', 'alice', 'senha_alice', ['grupo1', 'grupo2'])
    create_user('Bob', 'bob', 'senha_bob', ['grupo2'])
    create_user('Carlos', 'carlos', 'senha_carlos', ['grupo3'])
