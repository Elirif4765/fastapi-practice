import pytest
from app import schemas

def test_get_all_comments(authorized_client, test_comments):
    res = authorized_client.get("/posts/1/comments/")
    assert res.status_code == 200

def test_unauthorized_user_get_all_comments(client, test_comments):
    res = client.get("/posts/1/comments/")
    assert res.status_code == 401

def test_get_comment_by_id(authorized_client, test_comments):
    res = authorized_client.get(f"/comments/{test_comments[0].id}")
    assert res.status_code == 200

def test_get_comment_not_exist(authorized_client):
    res = authorized_client.get(f"/comments/9213912")
    assert res.status_code == 404

def test_unauthorized_user_get_comment_by_id(client, test_comments):
    res = client.get(f"/comments/{test_comments[0].id}")
    assert res.status_code == 401

@pytest.mark.parametrize("content", [
    "1st comment",
    "2nd comment",
    "3rd comment"
])
def test_post_comment(authorized_client, test_posts, test_user, content):
    res = authorized_client.post(f"/posts/{test_posts[0].id}/comments/", json={"content": content})
    created_comment = schemas.CommentOut(**res.json())
    assert res.status_code == 201
    assert created_comment.content == content
    assert created_comment.post_id == test_posts[0].id
    assert created_comment.owner_id == test_user['id']

def test_unauthorized_user_post_comment(client, test_posts):
    res = client.post(f"/posts/{test_posts[0].id}/comments/", json={"content": "test comment"})
    assert res.status_code == 401

def test_delete_comment(authorized_client, test_comments):
    res = authorized_client.delete(f"/comments/{test_comments[0].id}")
    assert res.status_code == 204
    
def test_delete_comment_by_other_user(authorized_client, test_comments):
    res = authorized_client.delete(f"/comments/{test_comments[2].id}")
    assert res.status_code == 403
    
def test_delete_comment_not_exist(authorized_client):
    res = authorized_client.delete("/comments/219381")
    assert res.status_code == 404

def test_unauthorized_user_delete_comment(client, test_comments):
    res = client.delete(f"/comments/{test_comments[0].id}")
    assert res.status_code == 401

@pytest.mark.parametrize("content", [
    "updated comment 1",
    "updated comment 2",
    "updated comment 3"
])
def test_update_comment(authorized_client, test_comments, content):
    res = authorized_client.put(f"/comments/{test_comments[0].id}", json={"content": content})
    updated_comment = schemas.CommentOut(**res.json())
    assert res.status_code == 200
    assert updated_comment.content == content
    assert updated_comment.post_id == test_comments[0].post_id
    assert updated_comment.id == test_comments[0].id
    assert updated_comment.owner_id == test_comments[0].owner_id

def test_unauthorized_user_update_comment(client, test_comments, updated_comment):
    res = client.put(f"/comments/{test_comments[0].id}", json=updated_comment)
    assert res.status_code == 401

def test_update_comment_by_other_user(authorized_client, test_comments, updated_comment):
    res = authorized_client.put(f"/comments/{test_comments[2].id}", json=updated_comment)
    assert res.status_code == 403
    
def test_update_comment_not_exist(authorized_client, updated_comment):
    res = authorized_client.put(f"/comments/123124214", json=updated_comment)
    assert res.status_code == 404