import psycopg2

from utils.validation.db_validation import (
    validated_sql, 
    validated_fetch_columns, 
    validate_postgres_data,
    validated_sql_condition
)

from exceptions.db_exceptions import TableNotFound, NoSchedule

class PostgreManager:
    def __init__(self, database, host, user, password, port):
        self.database = database
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        
        self.__connect_to_db()


    def __del__(self):
        self.__close_connection()


    def __connect_to_db(self):
        try:
            self.conn = psycopg2.connect(database=self.database,
                                    host=self.host,
                                    user=self.user,
                                    password=self.password,
                                    port=self.port)

            print(f"Connected to PostgreSQL database - {self.database} successfully!")
        except Exception as e:
            print(f"Error: {e}")
        else:
            self.cursor = self.conn.cursor()

    def __close_connection(self):
        self.cursor.close()
        self.conn.close()


    def commit_changes(self):
        self.conn.commit()


    def create_table(self, table_name, template):
        query = ""
        for key, type_of_data in template.items():
            query += f"{key} {type_of_data}, "
        
        query = query[:-2]
        
        try:
            self.cursor.execute(f"""CREATE TABLE {table_name} (
                                    {query}
                                    );""")
        except psycopg2.errors.DuplicateTable:
            self.rollback()
            raise ValueError(f"{table_name} already exist. Pass...")


    def drop_table(self, table_name):
        self.cursor.execute(f"DROP TABLE {table_name};")


    def delete_from(self, table_name, condition):
        self.cursor.execute(f"DELETE FROM {table_name} WHERE {condition};")


    def clear_table(self, table_name):
        self.cursor.execute(f"DELETE FROM {table_name};")


    def insert_into(self, table_name, values, columns=None):
        if columns is None:
            columns_query = ""
        else:
            columns_query = " ("
            for column in columns:
                columns_query += f"{column}, "
            columns_query = columns_query[:-2] + ")"
        
        values_query = "("
        for value in values:
            if isinstance(value, str) or isinstance(value, dict):
                value = f"'{value}'"
            values_query += f"{value}, "
        values_query = values_query[:-2] + ")"
        try:
            self.cursor.execute(f"""INSERT INTO {table_name}{columns_query}
                                    VALUES {values_query};""")
            self.commit_changes()
        except psycopg2.errors.InFailedSqlTransaction:
            print("Failed transaction")
    

    def update(self, table_name, data, conditions=None):
        set_query = ""
        for column, value in data.items():
            value = validated_sql(value)
            set_query += f"{column} = '{value}', "

        set_query = set_query[:-2]

        if conditions is None:
            self.cursor.execute(f"""UPDATE {table_name}
                                    SET {set_query};""")
        else:
            condition_query = validated_sql_condition(conditions, "and")
            self.cursor.execute(f"""UPDATE {table_name}
                                    SET {set_query}
                                    WHERE {condition_query};""")
            self.commit_changes()


    def select(self, table_name, conditions=None, columns=None, fetch="all"):
        columns_query = "*"
        if columns is not None:
            columns_query = ""
            for column in columns:
                columns_query += f"{column}, "
            columns_query = columns_query[:-2]

        try:
            if conditions is None or not conditions:
                self.cursor.execute(f"SELECT {columns_query} FROM {table_name}")
            else:
                condition_query = validated_sql_condition(conditions, "and")
                print("select: ", condition_query)
                self.cursor.execute(f"SELECT {columns_query} FROM {table_name} WHERE {condition_query};")
            
        except psycopg2.errors.UndefinedTable:
            self.rollback()
            raise TableNotFound(table_name)
        except psycopg2.errors.UndefinedColumn:
            self.rollback()
            raise NoSchedule()
        
        if fetch == "all":
            response = self.cursor.fetchall()
        elif fetch == "one" or fetch == "1":
            response = self.cursor.fetchone()
        else:
            response = self.cursor.fetchmany(int(fetch))

        if not response:
            raise NoSchedule()
        
        validate_postgres_data(response)
        return response
    
    
    def exists(self, table_name: str, conditions: dict) -> bool:
        conditions_query = validated_sql_condition(conditions=conditions)
        self.cursor.execute(f"SELECT EXISTS (SELECT 1 FROM {table_name} WHERE {conditions_query});")
        return self.cursor.fetchone()[0]



    def get_columns(self, table_name):
        self.cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}';")
        columns = self.cursor.fetchall()
        return validated_fetch_columns(columns)

    def rollback(self):
        self.cursor.execute("ROLLBACK;")