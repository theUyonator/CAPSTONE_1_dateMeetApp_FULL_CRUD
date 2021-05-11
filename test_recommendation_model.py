"""Recommendation model tests for the dateMeet app."""

# run these tests like:
#
#    python -m unittest test_recommendation_model.py


import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Recommendation, Follows, Location, Likes

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///dateMeet_test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class   RecommendationModelTestCase(TestCase):
    """Test views for recommendations."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        user = User.register("User", "Test", "user@test.com", "testuser", "passWord4u", None, None)
        uid = 1111
        user.id = uid

        db.session.commit()

        user = User.query.get(uid)
    

        self.user = user
        self.uid = uid
    
        self.client = app.test_client()


    def tearDown(self):
        """Clean up any fouled transactions."""

        res = super().tearDown()
        db.session.rollback()
        return res


    def test_recommendation_model(self):
        """Does the basic recommendation model work?"""

        r = Recommendation(
            title="The best burger in the world",
            content="The best burger in the entire world definitely is Marcos Famous DT Edmonton",
            business_name="Marcos Famous",
            business_address="13425 36 Ave NW",
            business_city="Edmonton",
            business_state="Alberta",
            business_country="Canada",
            business_rating=4,
            user_id=self.uid
        )

        db.session.add(r)
        db.session.commit()

        # User should have 1 message 
        self.assertEqual(self.user.recommendations[0].business_country, "Canada")
        self.assertEqual(self.user.recommendations[0].business_rating, 4)
        self.assertEqual(len(self.user.recommendations), 1)


    def test_recommendation_likes(self):
        """This test method tests recommendation likes model"""

        r1 = Recommendation(
            title="Fire Doughnuts in Canada",
            content="Ever tried jerk flavored doughnuts?, then you haven't lived!. Marley's yard gotchu!",
            business_name="Marleys Yard",
            business_address="2345 67 Ave NW",
            business_city="Edmonton",
            business_state="Alberta",
            business_country="Canada",
            business_rating=4,
            user_id=self.uid
        )

        u = User.register("User2", "Test", "user2@test.com", "testuser2", "passWord4u2", None, None)
        uid2 = 2222
        u.id = uid2

        db.session.add(r1)
        db.session.commit()

        u.likes.append(r1)

        db.session.commit()

        l = Likes.query.filter(Likes.user_id == uid2).all()

        # There should be only one liked message and it should be m1

        self.assertEqual(len(l), 1)
        self.assertEqual(l[0].recommendation_id, r1.id)