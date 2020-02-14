# Either create a super user with this name, or change superUser to match yours
superUser = 'postgres'
databaseName = 'earnup'
postgres_host = 'localhost'
postgres_port = '5432'

dataFile = './data/AB_NYC_2019.csv'
cleanDataFile = './data/AB_NYC_2019_CLEAN.csv'

# This table will be overwritten, so make sure you don't need data inside it.
tableName = 'rentals'
tableSQL = "CREATE TABLE {table} (\
        id INT PRIMARY KEY,\
        name TEXT,\
        host_id INT,\
        host_name TEXT,\
        neighbourhood_group TEXT,\
        neighbourhood TEXT,\
        latitude FLOAT,\
        longitude FLOAT,\
        room_type TEXT,\
        price INT,\
        minimum_nights INT,\
        number_of_reviews INT,\
        last_review DATE,\
        reviews_per_month FLOAT(2),\
        calculated_host_listings_count INT,\
        availability_365 INT\
        )"

distanceSQL = "CREATE OR REPLACE FUNCTION distance(lat1 FLOAT, lon1 FLOAT,\
                lat2 FLOAT, lon2 FLOAT)\
                RETURNS FLOAT AS $$\
                DECLARE\
                    x float = 69.1 * (lat2 - lat1);\
                    y float = 69.1 * (lon2 - lon1) * cos(lat1 / 57.3);\
                BEGIN\
                    RETURN sqrt(x * x + y * y);\
                END\
                $$ LANGUAGE plpgsql;"