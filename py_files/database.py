from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('postgres://gknnjekrhkwmhs:0f5fbcce429f5bbba7ddc755b70249e62a5ed79b4051e2afc4b59853a32a40a3@ec2-52-200-134-180.compute-1.amazonaws.com:5432/d7e3rr57djdonl')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    
    from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
    from sqlalchemy.orm import backref, relationship
    
    class Provider(Base):
        __tablename__ = 'provider'
        provider_id = Column(Integer, primary_key=True)
        first_name = Column(String)
        last_name = Column(String)
    
    
    class Provider_Review(Base):
        __tablename__ = 'provider_review'
        id = Column(Integer, primary_key=True)
        p_id = Column(Integer, ForeignKey('provider.provider_id'))
        review = Column(String)
        result = Column(String)
        provider = relationship(
            Provider,
            backref=backref('provider',
                            uselist=True,
                            cascade='delete,all'))
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Create the fixtures

    deepak = Provider(provider_id = 1000, first_name='deepak', last_name = 'bairwa')
    db_session.add(deepak)
    gaurav = Provider(provider_id = 1001, first_name='gaurav', last_name = 'bhandari')
    db_session.add(gaurav)
    meenakshi = Provider(provider_id = 1002, first_name='meenakshi', last_name = 'gupta')
    db_session.add(meenakshi)
    alka = Provider(provider_id = 1003, first_name='alka', last_name = 'singh')
    db_session.add(alka)
    sneha = Provider(provider_id = 1004, first_name='sneha', last_name = 'aggarwal')
    db_session.add(sneha)

    p1 = Provider_Review(p_id=1000, review="Movie was good.", result='')
    db_session.add(p1)
    p2 = Provider_Review(p_id=1000, review="Movie was really bad.", result='')
    db_session.add(p2)
    p3 = Provider_Review(p_id=1001, review="Lengthy and Boring.", result='')
    db_session.add(p3)
    p4 = Provider_Review(p_id=1002, review="Engaging and wonderful", result='')
    db_session.add(p4)
    
    
    db_session.commit()
