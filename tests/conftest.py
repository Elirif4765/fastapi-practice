from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db, Base
import pytest
from app.oauth2 import create_access_token
from app import models


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    # def override_get_db():
    #     return session
    app.dependency_overrides[get_db] = lambda: session #override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(client):
    user_data = {"email": "hello123@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email": "world456@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture
def test_posts(test_user, test_user2, session):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    }, {
        "title": "second title",
        "content": "second content",
        "owner_id": test_user['id']
    }, {   
        "title": "third title",
        "content": "third content",
        "owner_id": test_user['id']
    }, {   
        "title": "4th title",
        "content": "4th content",
        "owner_id": test_user2['id']
    }]
    
    def create_post_model(post):
        return models.Post(**post)

    posts = list(map(create_post_model, posts_data))

    session.add_all(posts)
    session.commit()
    return session.query(models.Post).all()

@pytest.fixture
def test_updated_data(test_posts):
    return {"title": "updated title", "content": "updated content"}


@pytest.fixture
def test_vote(test_posts, session, test_user):
    new_vote = models.Vote(post_id = test_posts[3].id, user_id = test_user['id'])
    session.add(new_vote)
    session.commit()
    

@pytest.fixture
def test_comments(test_posts, test_user, test_user2, session):
    comments_data = [{
        "content": "1st comment",
        "post_id": test_posts[0].id,
        "owner_id": test_user['id']
    }, {
        "content": "2nd comment",
        "post_id": test_posts[0].id,
        "owner_id": test_user['id']
    }, {
        "content": "3rd comment",
        "post_id": test_posts[1].id,
        "owner_id": test_user2['id']
    }, {
        "content": "4th comment",
        "post_id": test_posts[3].id,
        "owner_id": test_user['id']
    }]

    comments = [models.Comment(**comment) for comment in comments_data]

    session.add_all(comments)
    session.commit()
    return session.query(models.Comment).all()

@pytest.fixture
def updated_comment():
    return {"content" : "updated comment"}