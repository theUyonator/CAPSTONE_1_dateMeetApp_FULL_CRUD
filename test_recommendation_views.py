"""
Recommendation View tests.
run these tests like:

FLASK_ENV=production python -m unittest test_recommendation_views.py

"""


import os
from unittest import TestCase

from models import db, connect_db, Recommendation, Location, User

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///dateMeet_test"


# Now we can import app

from app import app, CURR_USER_KEY, CURR_LOCATION

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False


class RecommendationViewTestCase(TestCase):
    """Test views for recommendations."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.testuser = User.register(
                                first_name="User",
                                last_name="Test",
                                email="test@test.com",
                                username="testuser",
                                password="testuser",
                                image_url=None,
                                header_url=None
                                )
        self.testuser_id = 1981
        self.testuser.id = self.testuser_id

        self.u2 = User.register(
                                first_name="User2",
                                last_name="Test",
                                email="testuser2@test.com",
                                username="testuser2",
                                password="testuser2",
                                image_url=None,
                                header_url=None
                            )
        
        self.u2id = 930
        self.u2.id = self.u2id

        db.session.commit()

    def tearDown(self):
        """Clean up any fouled transactions."""

        res = super().tearDown()
        db.session.rollback()
        return res

    def test_add_recommendation(self):
        """Can user add a recommendation?"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id


            resp = c.post("/recommendations/new", data={"title": "Best buns in the DMV",
                                                        "content": "mAN i have never had better buns than this, shit go crazy!",
                                                        "business_name": "Nana Buns",
                                                        "business_address": "2568 Nappy Ave DMV",
                                                        "business_city": "Houston",
                                                        "business_state": "Texas",
                                                        "business_country": "USA",
                                                        "business_rating": 4,
                                                        "user_id": self.testuser_id})

            # Make sure it redirects
            self.assertEqual(resp.status_code, 302)

            rec = Recommendation.query.one()
            self.assertEqual(rec.business_state, "Texas")
            
    def test_unauthorized_add_recommendation(self):
        """This test method tests to confirm that an unauthoritzed 
           user is unable to add a recommendation.
        """

        with self.client as c:
            resp = c.post("/recommendations/new", data={"title": "Best buns in the DMV",
                                                        "content": "mAN i have never had better buns than this, shit go crazy!",
                                                        "business_name": "Nana Buns",
                                                        "business_address": "2568 Nappy Ave DMV",
                                                        "business_city": "Houston",
                                                        "business_state": "Texas",
                                                        "business_country": "USA",
                                                        "business_rating": 4,
                                                        "user_id": self.testuser_id}, 
                                                        follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Access unauthorized", str(resp.data))

   
    def test_list_recommendations(self):
        """This test method tests to confirm that the logged in user can only
        view recommendations in their state and city."""

        L = Location(
            name="Home",
            address="False Test Creek SW, Long Beach CA",
            long=143.12,
            lat=-234.5,
            city="Long Beach",
            state="CA",
            user_id=self.testuser_id
        )
        L_id = 124
        L.id = L_id

        db.session.add(L)
        db.session.commit()

        r1 = Recommendation(
           title="Fire Doughnuts in LA",
           content="Bro these mf doughnuts be smacking like gahdamn!. Check out Leonards bro!",
           business_name="Leonards",
           business_address="2345 Rodeo Ave",
           business_city="Long Beach",
           business_state="CA",
           business_country="US",
           business_rating=5,
           user_id=self.testuser_id
           )
       

        r2 = Recommendation(
            id=365,
            title="Deep Dish Pizza in Edmonton, Canada",
            content="Looking for delicious deep dish pizza?, Chicago 001 has the best on Whyte Ave",
            business_name="Chicago 001",
            business_address="1946 Whyte Ave NW",
            business_city="Edmonton",
            business_state="Alberta",
            business_country="Canada",
            business_rating=5,
            user_id=self.u2id
        )

        db.session.add_all([r1, r2])
        db.session.commit()


        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY]=self.testuser_id
                sess[CURR_LOCATION]=L_id


            resp = c.get("/recommendations/list")

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Fire Doughnuts in LA", str(resp.data))
            self.assertNotIn("Deep Dish Pizza in Edmonton, Canada", str(resp.data))


    def test_delete_recommendation(self):
        """This test method tests to confirm that a recommendation is deleted when a delete request is sent by a logged in user."""

        r = Recommendation(
           id=419,
           title="Fire Doughnuts in LA",
           content="Bro these mf doughnuts be smacking like gahdamn!. Check out Leonards bro!",
           business_name="Leonards",
           business_address="2345 Rodeo Ave",
           business_city="Long Beach",
           business_state="CA",
           business_country="US",
           business_rating=5,
           user_id=self.testuser_id
           )

        db.session.add(r)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id
            
            
            resp = c.post("/recommendations/419/delete", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)

            r = Recommendation.query.get(419)
            self.assertIsNone(r)


    def test_unauthorized_recommendation_delete(self):
        """This test method confirms that an unauthorized user 
           cannot delete a recommendation.
        """

        # We create a separate user first
        u = User.register(
                        first_name="Userrrr",
                        last_name="Test",
                        email="testuserrrr@test.com",
                        username="testuserrrr",
                        password="testuserrrr",
                        image_url=None,
                        header_url=None
                            )

        u.id = 589

        # Now we create a recommendation made by testuser

        r = Recommendation(
           id=419,
           title="Fire Doughnuts in LA",
           content="Bro these mf doughnuts be smacking like gahdamn!. Check out Leonards bro!",
           business_name="Leonards",
           business_address="2345 Rodeo Ave",
           business_city="Long Beach",
           business_state="CA",
           business_country="US",
           business_rating=5,
           user_id=self.testuser_id
           )

        db.session.add_all([u,r])
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = 589
            
            resp = c.post("/recommendations/419/delete", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Access unauthorized.", str(resp.data))

            r = Recommendation.query.get(419)
            self.assertIsNotNone(r)

    
   