from sqlalchemy import create_engine
import psycopg2
import pandas as pd
from io import StringIO

#conn = psycopg2.connect(user="postgres", password="trivisono", host="localhost", port="5432", database="postgres")
#cursor = conn.cursor()


class PostgreSQL:

    # Initilize the common usable variables in below function:
    def __init__(self, data_config):
        self.data_sources = data_config
        self.user = self.data_sources['data_sources']['postgreSQL']['username']
        self.password = self.data_sources['data_sources']['postgreSQL']['password']
        self.host = self.data_sources['data_sources']['postgreSQL']['host']
        self.port = self.data_sources['data_sources']['postgreSQL']['port']
        self.db_name = self.data_sources['data_sources']['postgreSQL']['database']
        self.uri = f'postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}'

        try:
            # Connect to an existing database
            self.engine = create_engine(self.uri)
            self.conn = self.engine.raw_connection()
            # Create a cursor to perform database operations
            self.cursor = self.conn.cursor()
            # Print PostgreSQL details
            print("PostgreSQL server information")
            print(self.conn.get_dsn_parameters(), "\n")
            # Executing a SQL query
            self.cursor.execute("SELECT version();")
            # Fetch result
            record = self.cursor.fetchone()
            print("PostgreSQL Connection Successful: ", record, "\n")

        except Exception as error:
            print("Error while connecting to PostgreSQL", error)

    # Function to insert data in DB, could handle Python dictionary and Pandas dataframes
    def load_into_staging(self, df, table_name):
        """
        Saves the provided dataframe to memory in a buffer and copies the data to a temp table in SQL.
        :param df: DF to copy
        :param table_name: SQL Table to replace
        :return:

        """
        # drops old table and creates new empty table
        df.head(0).to_sql(f"{table_name}", self.engine, if_exists='replace', index=False, schema="staging")

        # save dataframe to an in memory buffer
        buffer = StringIO()
        df.to_csv(buffer, header=False, index=False, sep='|')
        buffer.seek(0)

        try:
            self.cursor.copy_from(buffer, f"staging.{table_name}", sep='|', null="NULL")
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            self.conn.rollback()
            return 1

    def insert_from_staging(self, table_name):
        """
        Inserts the records of the created temp table that don't exist in the input table. Then it drops the temp table.
        :param table_name: SQL Table to replace
        :return:
        """
        self.cursor.execute(f'SELECT * FROM staging.{table_name} EXCEPT SELECT * FROM fdm.{table_name};')
        rows = len(self.cursor.fetchall())

        self.cursor.execute(f'INSERT INTO fdm.{table_name} SELECT * FROM staging.{table_name} EXCEPT SELECT * FROM '
                            f'fdm.{table_name};')

        self.cursor.execute(f'TRUNCATE TABLE staging.{table_name}')
        self.conn.commit()

        print(f'Se han insertado {rows} registros')

    def load_batch(self, df, table_name):
        """
        Inserts a batch from a dataframe into a SQL table.
        :param df: DF to copy
        :param table_name: SQL Table to replace
        :return:
        """
        try:
            self.load_into_staging(df, table_name)
            self.insert_from_staging(table_name)
            print(f"La tabla {table_name} fue actualizada")

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            self.conn.rollback()
            return 1

    def insert_leagues(self, name, details):
        self.cursor.execute("INSERT INTO records (name,details) VALUES ('%s','%s')" % (name, details))

    def read_record(self, field, name, engine):
        result = self.cursor.execute("SELECT %s FROM records WHERE name = '%s'" % (field, name))
        return result.first()[0]

    def update_record(self, field, name, new_value, engine):
        self.cursor.execute("UPDATE records SET %s = '%s' WHERE name = '%s'" % (field, new_value, name))

    def write_dataset(self, name, dataset, engine):
        dataset.to_sql('%s' % (name), engine, index=False, if_exists='replace', chunksize=1000)

    def read_dataset(self, name, engine):
        try:
            dataset = pd.read_sql_table(name, engine)
        except:
            dataset = pd.DataFrame([])
        return dataset

    def list_datasets(self, engine):
        datasets = self.cursor.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name;")
        return datasets.fetchall()


