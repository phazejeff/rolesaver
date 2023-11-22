from sqlalchemy import create_engine, select, delete
from sqlalchemy.orm import Session, contains_eager
import os
from typing import List
import discord
from dotenv import load_dotenv
from .tables import Role, User, Nickname, Base, Blacklist, userroles, usernicknames
load_dotenv()

class Database:
    def __init__(self):
        user = os.environ["MYSQL_USER"]
        password = os.environ["MYSQL_PASSWORD"]
        host = os.environ["MYSQL_HOST"]
        db_name = os.environ["MYSQL_DATABASE"]
        self.engine = create_engine(f"mysql+mysqldb://{user}:{password}@{host}/{db_name}")

        Base.metadata.create_all(self.engine)

    def upsert_member(self, member: discord.Member):
        session = Session(self.engine)
        user = self._fetch_member(session, member)

        if not user:
            user = User(member.id)
            session.add(user)
        
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

        nickname = session.query(Nickname).filter_by(discord_server_id=member.guild.id).first()
        if nickname:
            nickname.nickname = member.nick
        else:
            nickname = Nickname(member.guild.id, member.nick)
            session.add(nickname)
        user.nickname = nickname

        session.commit()

    def _fetch_member(self, session: Session, member: discord.Member) -> User | None:
        stmt = (
            select(User)
            .where(User.discord_id == member.id)
            .join(User.roles)
            .filter(Role.discord_server_id == member.guild.id)
            .options(contains_eager(User.roles))
        )

        r = session.execute(stmt)
        user = r.unique().first()
        print(user)

        if not user:
            return None
        else:
            return user[0]
        
    def fetch_member(self, member: discord.Member) -> User | None:
        session = Session(self.engine)
        return self._fetch_member(session, member)

    def _fetch_blacklist(self, session: Session, guild: discord.Guild) -> Blacklist | None:
        stmt = (
            select(Blacklist)
            .where(Blacklist.discord_server_id == guild.id)
        )

        r = session.execute(stmt)
        blacklist = r.first()

        if not blacklist:
            return None
        else:
            return blacklist[0]

    def fetch_blacklist(self, guild: discord.Guild) -> Blacklist | None:
        session = Session(self.engine)
        return self._fetch_blacklist(session, guild)
    
    def insert_or_remove_into_blacklist(self, guild: discord.Guild, role: discord.Role) -> bool:
        session = Session(self.engine)
        blacklist = self._fetch_blacklist(session, guild)

        if not blacklist:
            blacklist = Blacklist(guild.id)
            session.add(blacklist)

        r = session.query(Role).filter_by(discord_role_id=role.id).first()
        if not r:
            r = Role(guild.id, role.id)
            session.add(r)
        
        added = True
        if r in blacklist.roles:
            blacklist.roles.remove(r)
            added = False
        else:
            blacklist.roles.add(r)

        session.commit()

        return added