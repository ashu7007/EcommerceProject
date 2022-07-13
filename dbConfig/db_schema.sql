

CREATE TABLE userdata(
   id  SERIAL   PRIMARY KEY,
   full_name   VARCHAR(255)  NOT NULL,
   email       VARCHAR(255)  NOT NULL,
   username VARCHAR (50) UNIQUE NOT NULL,
   password TEXT NOT NULL,
   address   VARCHAR(255) NOT NULL,
   dob timestamp NOT NULL,
   gender VARCHAR(10)  NOT NULL,
   user_type VARCHAR (50) NOT NULL,
   active    bool  default false,
   created_at timestamp with time zone not null     ,
   updated_at  timestamp with time zone not null );


CREATE TABLE otp (
   id  SERIAL   PRIMARY KEY,
   user_id int NOT NULL,
   otp int NOT NULL,
   created_at timestamp with time zone not null     ,
   updated_at  timestamp with time zone not null     ,
   CONSTRAINT fk_User  
   FOREIGN KEY(user_id)   
   REFERENCES Userdata(id)  );