from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('postgresql://postgres:8991Ngu@007@localhost:5432/postgres')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    
    from models import Provider_Review, Provider
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
