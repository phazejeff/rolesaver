from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import Session, contains_eager
import os
import discord
from dotenv import load_dotenv
from database.tables import Role, User, Nickname, Base, Blacklist, Log, userroles, usernicknames
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

    def _fetch_member(self, session: Session, member: discord.Member) -> User:
        stmt = (
            select(User)
            .where(User.discord_id == member.id)
            .join(User.roles)
            .filter(Role.discord_server_id == member.guild.id)
            .options(contains_eager(User.roles))
        )

        r = session.execute(stmt)
        user = r.unique().first()

        if not user:
            user = User(member.id)
            session.add(user)
            return user
        else:
            return user[0]
        
    def fetch_member(self, member: discord.Member) -> User:
        session = Session(self.engine)
        member = self._fetch_member(session, member)
        return member
    
    def _fetch_user(self, session: Session, user: discord.User) -> User:
        stmt = (
            select(User)
            .where(User.discord_id == user.id)
            .join(User.roles)
            .options(contains_eager(User.roles))
        )

        r = session.execute(stmt)
        userdb = r.unique().first()

        if not userdb:
            userdb = User(user.id)
            session.add(userdb)
            return userdb
        else:
            return userdb[0]
    
    def fetch_user(self, user: discord.User) -> User:
        session = Session(self.engine)
        user = self._fetch_user(session, user)
        return user
    
    def delete_user(self, user: discord.User):
        session = Session(self.engine)
        member = self._fetch_user(session, user)
        session.delete(member)

    def _fetch_blacklist(self, session: Session, guild: discord.Guild) -> Blacklist:
        stmt = (
            select(Blacklist)
            .where(Blacklist.discord_server_id == guild.id)
        )

        r = session.execute(stmt)
        blacklist = r.first()

        if not blacklist:
            blacklist = Blacklist(guild.id)
            session.add(blacklist)
            return blacklist
        else:
            return blacklist[0]

    def fetch_blacklist(self, guild: discord.Guild) -> Blacklist:
        session = Session(self.engine)
        blacklist = self._fetch_blacklist(session, guild)
        return blacklist
    
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
    
    def switch_list(self, guild):
        session = Session(self.engine)
        blacklist = self._fetch_blacklist(session, guild)
        blacklist.roles.clear()
        blacklist.is_blacklist = not blacklist.is_blacklist
        session.commit()

    def _fetch_log(self, session: Session, guild: discord.Guild) -> Log:
        stmt = (
            select(Log)
            .where(Log.discord_server_id == guild.id)
        )

        r = session.execute(stmt)
        log = r.first()
        if not log:
            log = Log(guild.id)
            session.add(log)
            return log
        else:
            return log[0]
        
    def fetch_log(self, guild: discord.Guild):
        session = Session(self.engine)
        log = self._fetch_log(session, guild)
        return log
    
    def disable_logging(self, guild: discord.Guild):
        session = Session(self.engine)
        log = self._fetch_log(session, guild)
        log.is_logging = False

        session.commit()
    
    def enable_logging(self, guild: discord.Guild, channel: discord.TextChannel):
        session = Session(self.engine)
        log = self._fetch_log(session, guild)
        log.log_channel = channel.id
        log.is_logging = True

        session.commit()

    def user_count(self):
        session = Session(self.engine)
        count = session.query(func.count(User.id)).scalar()
        return count
    
    def role_count(self):
        session = Session(self.engine)
        count = session.query(func.count(Role.id)).scalar()
        return count
    
    # since every user gets nickname saved, even if null, this is an accurate count for members
    def nickname_count(self):
        session = Session(self.engine)
        count = session.query(func.count()).select_from(usernicknames).scalar()
        return count
    
    def member_count(self, guild: discord.Guild):
        session = Session(self.engine)
        count = session.query(func.count()).select_from(User).join(User.nickname).where(Nickname.discord_server_id == guild.id).scalar()
        return count
    
    def guild_role_count(self, guild: discord.Guild):
        session = Session(self.engine)
        count = session.query(func.count()).select_from(Role).where(Role.discord_server_id == guild.id).scalar()
        return count
    