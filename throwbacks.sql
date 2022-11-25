CREATE TABLE quotes.throwback(
	id int NOT NULL AUTO_INCREMENT PRIMARY KEY , 
    name varchar(255) NOT NULL, 
	photo BLOB, 
    date varchar(255) NOT NULL, 
    context varchar(255) NOT NULL 
);

