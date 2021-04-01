"""Seed file to make sample data for the dateMeet db"""

from models import db, User
from app import app

# Create all tables

db.drop_all()
db.create_all()

# If table isn't empty, empty it 
User.query.delete()


# Add users 

pete = User.register("Peter", "Davidson", "petedavidson@yahoo.com", "peted9v3007", "hack9sh9q", "https://assets.teenvogue.com/photos/5b3a5abacd6b096ecd5879ef/4:3/w_1911,h_1433,c_limit/GettyImages-840000222.jpg")

Mahomes =  User.register("Patrick", "Mahomes", "patrickmahomes@nfl.com", "Mahomeboi", "TBd9g09t", "https://www.si.com/.image/ar_1:1%2Cc_fill%2Ccs_srgb%2Cfl_progressive%2Cq_auto:good%2Cw_1200/MTcwMTMyMDcwODUxNDIyMDA4/patrick-mahomes-chiefs-super-bowl-liv.jpg")

Mikey = User.register("Mikey", "Williams", "mikeywilliams@aau.com", "Mikeyyyy", "B1gsh0t!!", "https://marriedbiography.com/wp-content/uploads/2020/06/Mikey-Williams.jpg")

Bronny = User.register("Bronny", "James", "bronnyJames@aau.com", "Bronny0", "Myd9dak1ng!", "https://cdn.vox-cdn.com/thumbor/trU9GmuulQyztTGaTGDjAWymLMk=/1400x1400/filters:format(jpeg)/cdn.vox-cdn.com/uploads/chorus_asset/file/21929209/usa_today_13792544.jpg")

Ani = User.register("Aniolla", "Ojoro", "anioojoro@gmail.com", "An10j0", "L0v315beautiful!", None)

Joseph = User.register("Joseph", "Levitt", "levitt@screw.com", "daB3stR0b1n", "D9rkKn1ght!", None)


#Now we add the objects to seession, so they'll persist

db.session.add(pete)
db.session.add(Mahomes)
db.session.add(Mikey)
db.session.add(Bronny)
db.session.add(Ani)
db.session.add(Joseph)


# To save these in the db we commit 
db.session.commit()

# #Add posts 

petes_first = Post(title="Arbys is trash",
            content="So me and my friends went to the Arbys on Argyl Road in Edmonton and boy was it terrible, food sucked, place dirty, eww!",
            image_url_1="https://s3-media0.fl.yelpcdn.com/bphoto/cCl5RgD9ymSGbpq1ZO_xAg/o.jpg")

db.session.add(petes_first)
# db.session.add(petes_second)
# db.session.add(Mahomes_first)

db.session.commit()