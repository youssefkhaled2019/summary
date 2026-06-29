
# user = db.get(User, 1)
# print(user.posts)












# أما db.query() فهو ما زال شائعًا، لكن ستتعلم لاحقًا الأسلوب الأحدث:

# from sqlalchemy import select

# stmt = select(User)
# users = db.execute(stmt).scalars().all()

# لكن ابدأ أولًا بـ query() لأنه أسهل لفهم CRUD، ثم انتقل إلى select() بعد أن تنتهي من CRUD الأساسي.
# =================================

# db.query(User).all()
# db.query(User).filter(User.email == user.email).first()
# db_user=db.query(User).filter(  (User.email == user.email) | (User.username == user.username)).first()
#  db_user = db.query( User).filter( or_( User.email == user.email,User.username == user.username ) ).first()
#  db.query(User).filter(User.id == user_id).first()

#  db_user = User( name=user.name, email=user.email,  hashed_password=hash_password(user.password))
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)