from app import schemas
import pytest

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    # posts = [schemas.PostOut(**post) for post in res.json()]
    assert res.status_code == 200

def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unauthorized_user_get_one_posts(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get("/posts/88888")
    assert res.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content


@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesome new content", True),
    ("more new title", "more new content", False),
    ("favourite pizza", "i love cheeeeeees", True)
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']


def test_default_published_true(authorized_client, test_posts):
    res = authorized_client.post("/posts/", json={"title": "aaaa", "content": "boooo"})
    created_post = schemas.Post(**res.json())
    assert created_post.published == True

def test_unauthorized_user_create_posts(client, test_posts):
    res = client.post("/posts/", json={"title": "aaaa", "content": "boooo"})
    assert res.status_code == 401


def test_unauthorized_user_delete_post(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_delete_post_success(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_delete_post_non_exist(authorized_client):
    res = authorized_client.delete("/posts/88888888")
    assert res.status_code == 404

def test_delete_other_user_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403


def test_update_post(authorized_client, test_posts, test_updated_data):
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=test_updated_data)
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == test_updated_data['title']
    assert updated_post.content == test_updated_data['content']

def test_update_other_user_post(authorized_client, test_posts, test_updated_data):
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=test_updated_data)
    assert res.status_code == 403

def test_unauthorized_user_update_post(client, test_posts, test_updated_data):
    res = client.put(f"/posts/{test_posts[0].id}", json=test_updated_data)
    assert res.status_code == 401

def test_update_post_non_exist(authorized_client, test_posts, test_updated_data):
    res = authorized_client.put("/posts/888888", json=test_updated_data)
    assert res.status_code == 404