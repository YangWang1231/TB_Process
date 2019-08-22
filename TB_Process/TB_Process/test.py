

from TB_Process import db
from TB_Process.module import User

if __name__ == '__main__':
    #u = User(name = 'hello', password = '433')
    #db.session.add(u)
    #db.session.commit()
    users = User.query.all()
    for u in users:
        print(u.id, u.name, u.password)
