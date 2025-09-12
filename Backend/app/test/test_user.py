from models.user import User, db


def test_crear_usuario(app):
    user = User(nombre="Santi", email="test@example.com", rol="usuario")
    user.set_password("123456")
    
    db.session.add(user)
    db.session.commit()

    u = User.query.filter_by(email="test@example.com").first()
    assert u is not None
    assert u.check_password("123456")
    assert not u.check_password("mala")


def test_email_unico(app):
    user1 = User(nombre="A", email="unique@example.com")
    user1.set_password("123")
    db.session.add(user1)
    db.session.commit()

    user2 = User(nombre="B", email="unique@example.com")
    user2.set_password("123")
    db.session.add(user2)
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        assert "UNIQUE constraint" in str(e)
