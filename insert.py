from app import db, app
from app.models import User, Vote, Ballot, Candidate, Election

with app.app_context():
    u1 = User(email='22330522@dut4life.ac.za', fullname='Prevani Moodley', campus='Midlands', registered=True, role='admin')
    u1.set_password('password')
    db.session.add(u1)
    users = [
        {'email': '22242711@dut4life.ac.za', 'fullname': 'Ndingeko Unathi Gumede', 'campus': 'Durban'},
        {'email': '22338312@dut4life.ac.za', 'fullname': 'Amahle Bhulose', 'campus': 'Midlands'},
        {'email': '22346650@dut4life.ac.za', 'fullname': 'Nkanyiso Xaba', 'campus': 'Durban'},
        {'email': '22102825@dut4life.ac.za', 'fullname': 'Violan Reddy', 'campus': 'Midlands'},
        {'email': '21519471@dut4life.ac.za', 'fullname': 'Thabo Shabalala', 'campus': 'Durban'},
        {'email': '22282855@dut4life.ac.za', 'fullname': 'Keabetswe Kadiege', 'campus': 'Midlands'},
        {'email': '22228534@dut4life.ac.za', 'fullname': 'Tshepo Masiteng', 'campus': 'Durban'},
        {'email': '22282585@dut4life.ac.za', 'fullname': 'Siboniso Magubane', 'campus': 'Midlands'},
        {'email': 'freedomk@dut.ac.za', 'fullname': 'Freedom Mthobisi Khubisa', 'campus': 'Durban'}
    ]

    for user_data in users:
        user = User(
            email=user_data['email'],
            fullname=user_data['fullname'],
            campus=user_data['campus'],
            registered=True,
            role='admin'
        )
        user.set_password('password')  # Set a default password for all users
        db.session.add(user)

    db.session.commit()
    print("Users added successfully!")
