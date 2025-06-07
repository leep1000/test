from app import create_app, db
from app.models import User, Asset

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()
    users = []
    for i in range(10):
        role = 'admin' if i == 0 else 'regular'
        user = User(username=f'user{i}', role=role)
        user.set_password('pass')
        users.append(user)
        db.session.add(user)
    db.session.commit()

    for i in range(10):
        asset = Asset(
            name=f'Asset{i}',
            asset_type='Device',
            serial_number=f'SN{i}',
            location='Office',
            owner_id=users[i % len(users)].id
        )
        db.session.add(asset)
    db.session.commit()
    print('Sample data inserted.')
