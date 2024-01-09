from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import Session, contains_eager
import os
import discord
from dotenv import load_dotenv
from database.tables import Role, User, Nickname, Base, Blacklist, Log, Patreon, userroles, usernicknames
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
        session.close()

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
            session.close()
            return user
        else:
            session.close()
            return user[0]
        
    def fetch_member(self, member: discord.Member) -> User:
        session = Session(self.engine)
        return self._fetch_member(session, member)

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
            session.close()
            return blacklist
        else:
            session.close()
            return blacklist[0]

    def fetch_blacklist(self, guild: discord.Guild) -> Blacklist:
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
        session.close()

        return added
    
    def switch_list(self, guild):
        session = Session(self.engine)
        blacklist = self._fetch_blacklist(session, guild)
        blacklist.roles.clear()
        blacklist.is_blacklist = not blacklist.is_blacklist
        session.commit()
        session.close()

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
            session.close()
            return log
        else:
            session.close()
            return log[0]
        
    def fetch_log(self, guild: discord.Guild):
        session = Session(self.engine)
        return self._fetch_log(session, guild)
    
    def disable_logging(self, guild: discord.Guild):
        session = Session(self.engine)
        log = self._fetch_log(session, guild)
        log.is_logging = False

        session.commit()
        session.close()
    
    def enable_logging(self, guild: discord.Guild, channel: discord.TextChannel):
        session = Session(self.engine)
        log = self._fetch_log(session, guild)
        log.log_channel = channel.id
        log.is_logging = True

        session.commit()
        session.close()

    # Unlike the other fetches, this will return none if it doesn't exist.
    def _fetch_patreon(self, session: Session, user: discord.User = None, guild: discord.Guild = None) -> Patreon | None:
        if guild:
            stmt = (
                select(Patreon)
                .where(Patreon.discord_server_id == guild.id)
            )
        elif user:
            stmt = (
                select(Patreon)
                .where(Patreon.discord_user_id == user.id)
            )
        else:
            return
        
        r = session.execute(stmt)
        patreon = r.first()
        if not patreon:
            return None
        else:
            session.close()
            return patreon[0]

    def fetch_patreon(self, user: discord.User = None, guild: discord.Guild = None):
        session = Session(self.engine)
        return self._fetch_patreon(session, user, guild)

    def is_server_patreon(self, guild: discord.Guild):
        patreon = self.fetch_patreon(guild=guild)
        if patreon:
            return True
        return False
    
    def add_user_to_patreon(self, user: discord.User):
        session = Session(self.engine)
        patreon = self._fetch_patreon(session, user=user)
        if patreon:
            session.close()
            return
        
        patreon = Patreon(user.id)
        session.add(patreon)
        session.close()

    def update_patreon_user_guild(self, user: discord.User, guild: discord.Guild):
        session = Session(self.engine)
        patreon = self._fetch_patreon(session, user=user)
        if patreon == None:
            patreon = Patreon(user.id)
            session.add(patreon)
        
        patreon.discord_server_id = guild.id
        session.commit()
        session.close()

    def remove_patreon_user(self, user: discord.User):
        session = Session(self.engine)
        patreon = self._fetch_patreon(session, user=user)
        if patreon == None:
            return
        
        session.delete(patreon)
        session.close()

    def user_count(self):
        session = Session(self.engine)
        count = session.query(func.count(User.id)).scalar()
        session.close()
        return count
    
    def role_count(self):
        session = Session(self.engine)
        count = session.query(func.count(Role.id)).scalar()
        session.close()
        return count
    
    # since every user gets nickname saved, even if null, this is an accurate count for members
    def nickname_count(self):
        session = Session(self.engine)
        count = session.query(func.count()).select_from(usernicknames).scalar()
        session.close()
        return count
    
    def member_count(self, guild: discord.Guild):
        session = Session(self.engine)
        count = session.query(func.count()).select_from(User).join(User.nickname).where(Nickname.discord_server_id == guild.id).scalar()
        session.close()
        return count
    
    def guild_role_count(self, guild: discord.Guild):
        session = Session(self.engine)
        count = session.query(func.count()).select_from(Role).where(Role.discord_server_id == guild.id).scalar()
        session.close()
        return count
    