CREATE TABLE Animation(
				Animation_ID	varchar(255), --NOT NULL
				Atitle			varchar(255),
				Language		varchar(20),
				Seasons			integer,
				Episodes		integer,
				Released_date 	DATE,
				Company_Name	varchar(255) NOT NULL,
				Comic_ID		int NOT NULL,
				primary key(Animation_ID),
				foreign key(Company_Name) references Company
				ON DELETE NO ACTION,
				foreign key(Comic_ID) references Comic_Draw_Publish
				ON DELETE NO ACTION
				--ON DELETE NO ACTION 
)


CREATE TABLE Dubbing_Actor(
				Actor_Name			varchar(255),
				Actor_Gender		char(1) CHECK (Actor_Gender = 'F' OR Actor_Gender = 'M'),
				Actor_Nationality	varchar(50),
				Actor_Birthday		date,
				Actor_Age			integer CHECK (Actor_Age >0),
				primary key(Actor_Name, Actor_Birthday)
)

CREATE TABLE Character(
				Character_Name 		varchar(255),
				Character_Birthday  date,
				Character_Gender 	char(1),
				primary key(Character_Name, Character_Birthday)
)

CREATE TABLE Voice(
				Actor_Name			varchar(255) NOT NULL,
				Actor_Birthday		date NOT NULL,
				Character_Name		varchar(255),
				Character_Birthday  date,				
				primary key(Actor_Name, Actor_Birthday, Character_Name),
				foreign key(Actor_Name, Actor_Birthday) references Dubbing_Actor,
				foreign key(Character_Name,Character_Birthday) references Character
)



CREATE TABLE Has(
				Animation_ID			varchar(255),
				Actor_Name 				varchar(255),
				Actor_Birthday			date, 
				Character_Name 			varchar(255),
				Character_Birthday		date,
				primary key (Animation_ID, Actor_Name, Actor_Birthday,Character_Name,Character_Birthday),
				foreign key(Animation_ID) references Animation,
				foreign key(Actor_Name, Actor_Birthday) references Dubbing_Actor,
				foreign key (Character_Name,Character_Birthday) references Character
)



CREATE TABLE Magazine(
	ISSN				int,
	Magazine_Name 		varchar(255),
	Magazine_Language	varchar(255),
	Magazine_Description varchar(255),
	PRIMARY KEY (ISSN)
	)

CREATE TABLE Cartoonists(
	Cartoonist_ID 			int,
	Cartoonist_Name 		varchar(255) NOT NULL,
	Date_of_Birth 			date,
	Cartoonist_Gender 		char(1),
	Cartoonist_Description	varchar(255),
	PRIMARY KEY (Cartoonist_ID)
	)

CREATE TABLE Comic_Draw_Publish(
	Comic_ID 			int,
	Comic_Description 	varchar(255),
	Comic_Name 			varchar(255),
	Cartoonist_ID		int NOT NULL,
	ISSN				int NOT NULL,
	PRIMARY KEY (Comic_ID),
	FOREIGN KEY (Cartoonist_ID) REFERENCES Cartoonists,
	FOREIGN KEY (ISSN) REFERENCES Magazine
	)

CREATE TABLE Company(
	Company_Name 	varchar(255),
	Company_Website varchar(255),
	Company_Country varchar(255),
	Company_Description Varchar(255),
	PRIMARY KEY (Company_Name)
	)

CREATE TABLE Usr(
	UID 			int,
	User_Name		varchar(50),
	User_Gender 	char(1),
	User_Age		int,
	User_Password	varchar(50),
	PRIMARY KEY (UID)
	)

CREATE TABLE Comment(
	Comment_Content varchar(255),
	Time_Posted 	varchar(255),
	UID 			int,
	Animation_ID	varchar(255) NOT NULL,
	PRIMARY KEY (UID, Time_Posted),
	FOREIGN KEY (UID) REFERENCES Usr
		ON DELETE CASCADE,
	FOREIGN KEY (Animation_ID) REFERENCES Animation 
		ON DELETE CASCADE
	)

