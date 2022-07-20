

CREATE TABLE userdata(
   id  SERIAL   PRIMARY KEY,
   full_name   VARCHAR(255)  NOT NULL,
   email       VARCHAR(255)  NOT NULL,
   username VARCHAR (50) UNIQUE NOT NULL,
   password TEXT NOT NULL,
   address   VARCHAR(255) NOT NULL,
   dob timestamp NOT NULL,
   gender VARCHAR(10)  NOT NULL,
   active    bool  default false,
   is_admin bool  default false,
   is_customer bool  default false,
   is_shopuser bool  default false,
   created_at timestamp with time zone NOT NULL,
   updated_at  timestamp with time zone NOT NULL,
   );


CREATE TABLE otp (
   id  SERIAL   PRIMARY KEY,
   user_id int NOT NULL,
   otp int NOT NULL,
   created_at timestamp with time zone NOT NULL,
   updated_at  timestamp with time zone NOT NULL,
   CONSTRAINT fk_User  
   FOREIGN KEY(user_id)   
   REFERENCES userdata(id)  );


CREATE TABLE Shop(
   id  SERIAL   PRIMARY KEY,
   user_id int NOT NULL,
   store_name   VARCHAR(255)  NOT NULL,
   description   VARCHAR(255) NOT NULL,
   active    bool  default false,
   status   VARCHAR(10)  NOT NULL,
   created_at timestamp with time zone NOT NULL,
   updated_at  timestamp with time zone NOT NULL,
   CONSTRAINT fk_User  
   FOREIGN KEY(user_id)   
   REFERENCES userdata(id) );


CREATE TABLE ShopRejection(
   id  SERIAL   PRIMARY KEY,
   user_id int NOT NULL,
   shop_id int NOT NULL,
   description   VARCHAR(255) NOT NULL,
   created_at timestamp with time zone NOT NULL,
   updated_at  timestamp with time zone NOT NULL,
   CONSTRAINT fk_User  
   FOREIGN KEY(user_id)   
   REFERENCES userdata(id),
   CONSTRAINT fk_Shop 
   FOREIGN KEY(shop_id)   
   REFERENCES Shop(id), );

CREATE TABLE Category(
   id  SERIAL   PRIMARY KEY,
   user_id int NOT NULL,
   category_name   VARCHAR(255)  NOT NULL,
   active    bool  default false,
   created_at timestamp with time zone NOT NULL,
   updated_at  timestamp with time zone NOT NULL,
   CONSTRAINT fk_User  
   FOREIGN KEY(user_id)   
   REFERENCES userdata(id)  );


CREATE TABLE Product(
   id  SERIAL   PRIMARY KEY,
   user_id int NOT NULL,
   shop_id int NOT NULL,
   category_id int NOT NULL,
   product_name   VARCHAR(255)  NOT NULL,
   stock_quantity int NOT NULL,
   sold_quantity int NOT NULL,
   brand VARCHAR(30)  NOT NULL,
   price VARCHAR(15)  NOT NULL,
   active    bool  default false,
   created_at timestamp with time zone NOT NULL,
   updated_at  timestamp with time zone NOT NULL,
   CONSTRAINT fk_User  
   FOREIGN KEY(user_id)   
   REFERENCES userdata(id),
   CONSTRAINT fk_Shop 
   FOREIGN KEY(shop_id)   
   REFERENCES Shop(id),
   CONSTRAINT fk_category 
   FOREIGN KEY(category_id)   
   REFERENCES Category(id) );


CREATE TABLE Wishlist(
   id  SERIAL   PRIMARY KEY,
   user_id int NOT NULL,
   product_id int [] NOT NULL,
   created_at timestamp with time zone NOT NULL,
   updated_at  timestamp with time zone NOT NULL,
   CONSTRAINT fk_User  
   FOREIGN KEY(user_id)   
   REFERENCES userdata(id) );

