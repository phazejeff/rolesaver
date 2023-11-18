from sqlalchemy import create_engine, select, delete
from sqlalchemy.orm import Session, aliased, selectinload, joinedload, contains_eager
import os
from typing import List
from discord import Member
from dotenv import load_dotenv
from tables import Role, User, Base, userroles
load_dotenv()

class Database:
    def __init__(self):
        user = os.environ["MYSQL_USER"]
        password = os.environ["MYSQL_PASSWORD"]
        host = os.environ["MYSQL_HOST"]
        db_name = os.environ["MYSQL_DATABASE"]
        self.engine = create_engine(f"mysql+mysqldb://{user}:{password}@{host}/{db_name}")

        Base.metadata.create_all(self.engine)

    def upsert_member(self, member: Member):
        session = Session(self.engine)
        stmt = (
            select(User)
            .join(User.roles)
            .filter(Role.discord_server_id == member.guild.id)
            .options(contains_eager(User.roles))

        )

        r = session.execute(stmt)
        user = r.unique().first()

        if not user:
            user = User(member.id)
            session.add(user)
        else:
            user: User = user[0]
        
        roles = set()
        for role in member.roles:
            r = session.query(Role).filter_by(discord_role_id=role.id).first()
            if r:
                roles.add(r)
            else:
                r = Role(member.guild.id, role.id)
                session.add(r)
                roles.add(r)

        user.roles = roles
        
        session.commit()
        
