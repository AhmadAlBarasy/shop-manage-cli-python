CREATE TABLE products (
    product_id varchar(12) PRIMARY KEY,
    product_name varchar(20) NOT NULL,
    category varchar(25),
    wholesale_price numeric(6,2) NOT NULL CHECK (wholesale_price > 0),
    quantity int CHECK (quantity >= 0),
    final_price numeric(6,2)
);

create table reciept(
	rec_id varchar(10) primary key,
	rec_date date not null,
	rec_time time not null
);


create table sales(
	product_id varchar(12) references products on delete cascade,
	rec_id varchar(10) references reciept on delete cascade,
	quantity int check (quantity>=1),
	primary key(product_id,rec_id)
);


CREATE OR REPLACE FUNCTION update_final_price()
RETURNS TRIGGER AS $$
BEGIN
    NEW.final_price := (
        CASE
            WHEN NEW.wholesale_price > 500 THEN NEW.wholesale_price * 1.05
            WHEN NEW.wholesale_price > 300 THEN NEW.wholesale_price * 1.07
            WHEN NEW.wholesale_price > 200 THEN NEW.wholesale_price * 1.08
            WHEN NEW.wholesale_price > 100 THEN NEW.wholesale_price * 1.1
            ELSE NEW.wholesale_price + 10
        END
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER update_final_price_trigger
BEFORE INSERT OR UPDATE OF wholesale_price ON products
FOR EACH ROW
EXECUTE FUNCTION update_final_price();