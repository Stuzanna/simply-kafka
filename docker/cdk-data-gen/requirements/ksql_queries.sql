CREATE STREAM
    customers
WITH (
    KAFKA_TOPIC = 'customers',
    VALUE_FORMAT = 'AVRO'
);

CREATE STREAM products (
    id varchar KEY,
    name string,
    price bigint
)
WITH (
    KAFKA_TOPIC = 'products',
    VALUE_FORMAT = 'AVRO'
);

CREATE STREAM
    purchases
WITH (
    KAFKA_TOPIC = 'purchases',
    VALUE_FORMAT = 'AVRO'
);

CREATE TABLE
    purchase_per_product
    AS SELECT
        products.id as product,
        LATEST_BY_OFFSET(products.name) as product_name,
        sum(purchases.quantity) as total_quantity,
        sum(products.price * purchases.quantity) as total_price
    FROM purchases
    JOIN products WITHIN 5 MINUTES
    ON purchases.productId = products.id
    GROUP BY products.id;