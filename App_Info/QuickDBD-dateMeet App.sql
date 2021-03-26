-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- Link to schema: https://app.quickdatabasediagrams.com/#/d/3KEjdd
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.

-- This code creates the DB schema diagram for the dateMeet app.
-- This app has 5 tables users, locations, posts, likes and history

CREATE TABLE "User" (
    "UserID" int   NOT NULL,
    "Email" string   NOT NULL,
    "First_name" string   NOT NULL,
    "Last_name" string   NOT NULL,
    "Username" string   NOT NULL,
    "Image_Url" string   NULL,
    "Bio" string   NULL,
    "Password" string   NOT NULL,
    "created_on" dateTime   NOT NULL,
    CONSTRAINT "pk_User" PRIMARY KEY (
        "UserID"
     ),
    CONSTRAINT "uc_User_Email" UNIQUE (
        "Email"
    ),
    CONSTRAINT "uc_User_Username" UNIQUE (
        "Username"
    )
);

CREATE TABLE "Location" (
    "LocationID" int   NOT NULL,
    "Name" string   NULL,
    "Address" string   NOT NULL,
    "Longitude" float   NOT NULL,
    "Latitude" float   NOT NULL,
    "UserID" int   NOT NULL,
    CONSTRAINT "pk_Location" PRIMARY KEY (
        "LocationID"
     ),
    CONSTRAINT "uc_Location_Address" UNIQUE (
        "Address"
    ),
    CONSTRAINT "uc_Location_Longitude" UNIQUE (
        "Longitude"
    ),
    CONSTRAINT "uc_Location_Latitude" UNIQUE (
        "Latitude"
    )
);

CREATE TABLE "Post" (
    "PostID" int   NOT NULL,
    "Title" varchar(250)   NOT NULL,
    "Content" varchat(500)   NOT NULL,
    "Image_Url_1" string   NULL,
    "Image_Url_2" string   NULL,
    "Image_Url_3" string   NULL,
    "Image_Url_4" string   NULL,
    "created_on" dateTime   NOT NULL,
    "UserID" int   NOT NULL,
    CONSTRAINT "pk_Post" PRIMARY KEY (
        "PostID"
     )
);

CREATE TABLE "Likes" (
    "LikesID" int   NOT NULL,
    "UserID" int   NOT NULL,
    "PostID" int   NOT NULL,
    CONSTRAINT "pk_Likes" PRIMARY KEY (
        "LikesID"
     ),
    CONSTRAINT "uc_Likes_PostID" UNIQUE (
        "PostID"
    )
);

CREATE TABLE "History" (
    "HistoryID" int   NOT NULL,
    "UserID" int   NOT NULL,
    "Business_Name" string   NOT NULL,
    "Business_Address" string   NOT NULL,
    "Yelp_business_id" string   NOT NULL,
    CONSTRAINT "pk_History" PRIMARY KEY (
        "HistoryID"
     ),
    CONSTRAINT "uc_History_Business_Name" UNIQUE (
        "Business_Name"
    ),
    CONSTRAINT "uc_History_Business_Address" UNIQUE (
        "Business_Address"
    ),
    CONSTRAINT "uc_History_Yelp_business_id" UNIQUE (
        "Yelp_business_id"
    )
);

ALTER TABLE "Location" ADD CONSTRAINT "fk_Location_UserID" FOREIGN KEY("UserID")
REFERENCES "User" ("UserID");

ALTER TABLE "Post" ADD CONSTRAINT "fk_Post_UserID" FOREIGN KEY("UserID")
REFERENCES "User" ("UserID");

ALTER TABLE "Likes" ADD CONSTRAINT "fk_Likes_UserID" FOREIGN KEY("UserID")
REFERENCES "User" ("UserID");

ALTER TABLE "Likes" ADD CONSTRAINT "fk_Likes_PostID" FOREIGN KEY("PostID")
REFERENCES "Post" ("PostID");

ALTER TABLE "History" ADD CONSTRAINT "fk_History_UserID" FOREIGN KEY("UserID")
REFERENCES "User" ("UserID");

