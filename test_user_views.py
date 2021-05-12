"""This file tests the User view functions for the dateMeet app."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_user_views.py


import os
from unittest import TestCase

from models import db, connect_db, User, Recommendation, Location, Likes, Follows
from bs4 import BeautifulSoup

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests 

os.environ['DATABASE_URL'] = "postgresql:///dateMeet_test"


# Now we can import app

from app import app, CURR_USER_KEY, CURR_LOCATION

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

# We turn off CSRF in WTFORMS because it makes the test process alot more difficult

app.config['WTF_CSRF_ENABLED'] = False


class UserViewsTestCase(TestCase):
    """Test views for users."""

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

        self.testuser_id = 911
        self.testuser.id = self.testuser_id

        self.u1 = User.register(
                                first_name="User1",
                                last_name="Test",
                                email="testuser1@test.com",
                                username="testuser1",
                                password="testuser1",
                                image_url=None,
                                header_url=None
                            )
        
        self.u1id = 837
        self.u1.id = self.u1id

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

        self.u3 = User.register(
                                first_name="User3",
                                last_name="Test",
                                email="three@test.com",
                                username="three",
                                password="testuser3",
                                image_url=None,
                                header_url=None
                            )

        self.u4 = User.register(
                                first_name="User4",
                                last_name="Test",
                                email="four@test.com",
                                username="four",
                                password="testuser4",
                                image_url=None,
                                header_url=None
                            )

        db.session.commit()


    def tearDown(self):
        """Clean up any fouled transactions."""

        res = super().tearDown()
        db.session.rollback()
        return res

    def test_users_index(self):
        """This test methods test to confirm user 
        information is showing up on the /users route
        when a user is logged in.
        """


        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id
                 
            resp = c.get("/users")
                 
            self.assertIn("@three", str(resp.data))
                 
            self.assertIn("@testuser1", str(resp.data))
                 
            self.assertIn("@testuser2", str(resp.data))


    def test_users_search(self):
        """This test method test to confim that
            when a search term that is part of a username
            is entered, all users having the same search term show up
        """

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id

            resp = c.get("/users?q=testuser")

            self.assertIn("@testuser", str(resp.data))
            self.assertIn("@testuser1", str(resp.data))
            self.assertIn("@testuser2", str(resp.data))

            self.assertNotIn("three", str(resp.data))
            self.assertNotIn("four", str(resp.data))

    def test_users_show_location(self):
        """This test method will confirm that a 
            logged in user location is displayed 
            on the page when a user logs in.
        """
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

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id
                sess[CURR_LOCATION] = L_id

            resp = c.get("/users/datelocations")

            self.assertIn("False Test Creek SW, Long Beach CA", str(resp.data))
            self.assertIn("Home", str(resp.data))
            

   

    def setup_recommendations_and_likes(self):
        """This method sets up recommendationss to be tested in 
            other test methods.
        """
        r1 = Recommendation(
           title="Fire Doughnuts in Canada",
           content="Ever tried jerk flavored doughnuts?, then you haven't lived!. Marley's yard gotchu!",
           business_name="Marleys Yard",
           business_address="2345 67 Ave NW",
           business_city="Edmonton",
           business_state="Alberta",
           business_country="Canada",
           business_rating=4,
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

        l1 =  Likes(user_id=self.testuser_id, recommendation_id=365)
        db.session.add(l1)
        db.session.commit()

    def test_show_likes(self):
        """This test method tests to see if user likes
           show up in the user profile.
        """
        self.setup_recommendations_and_likes()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id

            resp = c.get(f"/users/{self.testuser_id}")

            self.assertEqual(resp.status_code, 200)

            self.assertIn("@testuser", str(resp.data))
            soup = BeautifulSoup(str(resp.data), 'html.parser')
            found = soup.find_all("li", {"class" : "stat"})
            self.assertEqual(len(found), 4)

            # test for a count of recommendations of 1
            self.assertIn("1", found[0].text)

            # test for a count of following of 0 
            self.assertIn("0", found[1].text)

            # test for a count of followers of 0
            self.assertIn("0", found[2].text)

            # test for a count of likes of 1
            self.assertIn("1", found[3].text)

    def test_like_recommendation(self):
        """This test method tests to confirm that the 
            like recommendation functionality works.
        """
        r = Recommendation(
           id=3000,
           title="Jamaican Doughnuts in Canada",
           content="Jamaican Doughnuts are the bomb, got to Marley's on 67th!",
           business_name="Marleys Yard",
           business_address="2345 67 Ave NW",
           business_city="Edmonton",
           business_state="Alberta",
           business_country="Canada",
           business_rating=5,
           user_id=self.u2id
           )

        db.session.add(r)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id
            
            
            resp = c.post("/recommendations/3000/like", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)

            likes = Likes.query.filter(Likes.recommendation_id == 3000).all()
            self.assertEqual(len(likes), 1)
            self.assertEqual(likes[0].user_id, self.testuser_id)


    def test_unlike_recommendation(self):
        """This test method tests to confirm that an existing 
           liked recommendation can be unliked.
        """
        self.setup_recommendations_and_likes()
        r = Recommendation.query.filter(Recommendation.title == "Deep Dish Pizza in Edmonton, Canada").one()
        self.assertIsNotNone(r)
        self.assertNotEqual(r.user_id, self.testuser_id)

        l = Likes.query.filter(Likes.user_id == self.testuser_id and Likes.recommendation_id == r.id).one()

        # Now lets make sure that the testuser liked this recommendation
        self.assertIsNotNone(l)

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id
            
            
            resp = c.post(f"/recommendations/{r.id}/like", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)

            likes = Likes.query.filter(Likes.recommendation_id == r.id).all()
            # Noting that this recommendation has been unliked, we expect to get 
            # a length of 0 for likes
            self.assertEqual(len(likes), 0)
    

    def setup_followers(self):
        """This is a helper method used to set up followers
            to be used in the next few test methods.
        """

        f1 = Follows(user_being_followed_id=self.u1id, user_following_id=self.testuser_id)
        f2 = Follows(user_being_followed_id=self.u2id, user_following_id=self.testuser_id)
        f3 = Follows(user_being_followed_id=self.testuser_id, user_following_id=self.u1id)

        db.session.add_all([f1, f2, f3])
        db.session.commit()

    def test_user_profile_with_follows(self):
        """This test method, test to confirm that the right number of 
            users following logged in user and the right number of users the logged in
            user is following are shown in the user profile.
        """

        self.setup_followers()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id

            resp = c.get(f"/users/{self.testuser_id}")

            self.assertEqual(resp.status_code, 200)

            self.assertIn("@testuser", str(resp.data))
            soup = BeautifulSoup(str(resp.data), 'html.parser')
            found = soup.find_all("li", {"class" : "stat"})
            self.assertEqual(len(found), 4)

            # test for a count of recommendation of 0 
            self.assertIn("0", found[0].text)

            # test for a count of following of 2
            self.assertIn("2", found[1].text)

            # test for a count of followers of 1
            self.assertIn("1", found[2].text)

            # test for a count of likes of 0
            self.assertIn("0", found[3].text)

    
    def test_show_following(self):
        """This test method, tests to confirm that when the following show following route is requested
            the right follower information appears.
        """

        self.setup_followers()
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id
            
            
            resp = c.get(f"/users/{self.testuser_id}/following", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("@testuser1", str(resp.data))
            self.assertIn("@testuser2", str(resp.data))
            self.assertNotIn("@three", str(resp.data))
            self.assertNotIn("@four", str(resp.data))

    def test_show_followers(self):
        """This test method tests the user_following view function in the app.py
           to confirm that the acurate user accounts are following the current loggedin user.
        """

        self.setup_followers()
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id
            
            
            resp = c.get(f"/users/{self.testuser_id}/followers", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("@testuser1", str(resp.data))
            self.assertNotIn("@testuser2", str(resp.data))
            self.assertNotIn("@three", str(resp.data))
            self.assertNotIn("@four", str(resp.data))

    
    
