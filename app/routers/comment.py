from fastapi import status, HTTPException, Depends, APIRouter
from .. import database, schemas, models, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    tags=['Comment']
)


@router.get("/posts/{post_id}/comments/", response_model=list[schemas.CommentOut])
def get_comments(post_id: int, db: Session = Depends(database.get_db), current_user = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {post_id} doesn't exist")
    comments = db.query(models.Comment).filter(models.Comment.post_id == post_id).all()
    return comments


@router.get("/comments/{comment_id}", response_model=schemas.CommentOut)
def get_comment_by_id(comment_id: int, db: Session = Depends(database.get_db), current_user= Depends(oauth2.get_current_user)):
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Comment with id: {comment_id} doesn't exist")
    return comment


@router.post("/posts/{post_id}/comments/", status_code=status.HTTP_201_CREATED, response_model=schemas.CommentOut)
def post_comment(comment: schemas.CommentCreate, post_id: int, db: Session = Depends(database.get_db), current_user = Depends(oauth2.get_current_user)):
    new_comment = models.Comment(owner_id=current_user.id, post_id=post_id, **comment.model_dump())
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment
    


@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id: int, db: Session = Depends(database.get_db), current_user = Depends(oauth2.get_current_user)):
    comment_query = db.query(models.Comment).filter(models.Comment.id == comment_id)
    comment = comment_query.first()

    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Comment with id: {comment_id} does not exist")
    
    if comment.owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")

    comment_query.delete(synchronize_session=False)
    db.commit()


@router.put("/comments/{comment_id}", response_model=schemas.CommentOut)
def update_comment(updated_comment: schemas.CommentCreate, comment_id: int, db: Session = Depends(database.get_db), current_user = Depends(oauth2.get_current_user)):
    comment_query = db.query(models.Comment).filter(models.Comment.id == comment_id)
    old_comment = comment_query.first()
    
    if not old_comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Comment with id: {comment_id} does not exist")

    if old_comment.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    
    comment_query.update(updated_comment.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(old_comment)
    return old_comment
