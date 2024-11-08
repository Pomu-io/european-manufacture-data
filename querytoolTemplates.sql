-- *****************   Fashion Manufactures  ***************

-- select * from fashion_name_url;
-- select * from fashion_manufactures;
-- select * from fashion_manufactures where product_amount != -1

-- ****************   Apparel Manufactures   ****************

-- select * from apparel_manufactures

-- select max(product_page_total) as max_product_page_total from apparel_manufactures

-- select * from apparel_manufactures where manufacture_name like 'ME%'
-- select * from apparel_manufactures where product_amount != -1
-- select * from apparel_manufactures where product_page_total != -1


-- ****************   Apparel Manufactures products   ****************

-- select * from apparel_manufactures_product_links



-- WITH duplicates AS (
--     SELECT 
--         id,
--         ROW_NUMBER() OVER (PARTITION BY manufacture_name ORDER BY id) AS row_num
--     FROM 
--         apparel_manufactures_product_links
-- )
-- DELETE FROM apparel_manufactures_product_links
-- WHERE id IN (
--     SELECT id
--     FROM duplicates
--     WHERE row_num > 1
-- );

-- SELECT manufacture_name, COUNT(*) AS duplicate_count
-- FROM manufacture_ref
-- GROUP BY manufacture_name
-- HAVING COUNT(*) > 1;

-- select * from apparel_manufactures_product_links where manufacture_name='ALTA SETA GMBH & CO KG'; 

-- See how many products are there by counting commas in product_links column
-- SELECT
--     manufacture_name,
--     (LENGTH(product_links) - LENGTH(REPLACE(product_links, ',', ''))) AS product_amount
-- FROM
    -- apparel_manufactures_product_links;

-- ****************  Updating url  ******************
-- update apparel_manufactures_product_links as links 
-- set europe_page_url = url.europe_page_url
-- from apparel_name_url as url
-- where links.manufacture_name = url.manufacture_name

-- select * from apparel_manufacture_product_details

-- select * from products; 

-- select * from manufacture_ref

-- ****************   Luxury Manufactures products   ****************
-- select * from luxury_name_url;
-- select * from luxury_manufactures;




-- ********** play for fun ***********
-- create table if not exists trial (id serial primary key, person TEXT, phone_number text, location text);

-- select * from trial;

-- alter table trial
-- drop column email

-- CREATE TABLE IF NOT EXISTS {self.table_name} ( id serial PRIMARY KEY, manufacture_name VARCHAR(255), europe_page_url TEXT    )""")

-- alter table trial add email text null


-- do $$
-- begin
-- 	if not exists (
-- 	SELECT 1 FROM information_schema.columns 
-- 	where table_name = 'trial'
-- 	and column_name = 'email'
-- 	) then
-- 		alter table trial
-- 		add column email varchar(100) null;
-- 	end if;
-- end $$;

