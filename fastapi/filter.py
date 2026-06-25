
# user = db.get(User, 1)
# print(user.posts)












# أما db.query() فهو ما زال شائعًا، لكن ستتعلم لاحقًا الأسلوب الأحدث:

# from sqlalchemy import select

# stmt = select(User)
# users = db.execute(stmt).scalars().all()

# لكن ابدأ أولًا بـ query() لأنه أسهل لفهم CRUD، ثم انتقل إلى select() بعد أن تنتهي من CRUD الأساسي.
# =================================


