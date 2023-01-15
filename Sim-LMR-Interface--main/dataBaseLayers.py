import sqlite3 

class dataBaseLayers:
    def __init__(self, name = 'Layers.db') -> None:
        self.name = name

    def connect(self):
        self.connection = sqlite3.connect(self.name)

    def close_connection(self):
        try:
            self.connection.close()
        except:
            pass
    
    def create_table_layers(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Layers(
            Material TEXT,
            Thickness FLOAT,
            'Refract. Index' TEXT,
            Description TEXT );
        """)

    def insert_layer(self, fullDataSet):
        label_columns = ('Material', 'Thickness', 'Refract. Index', 'Description')
        qntd = ("?,?,?,?")

        cursor = self.connection.cursor()
        try:
            cursor.execute(f""" INSERT INTO Layers {label_columns}
                            VALUES({qntd})""", fullDataSet)
            self.connection.commit()
            return "Successfully Inserted Layer"
        except:
            return "ERROR"
    
    def select_all_layers(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute(""" SELECT * FROM Layers """)
            return cursor.fetchall()
        except:
            pass
    
    def clear_dataset(self):
        cursor = self.connection.cursor()
        cursor.execute(f""" DELETE FROM Layers """)
        self.connection.commit()

    def remove_layer(self, material):
        try:
            cursor = self.connection.cursor()
            cursor.execute(f""" DELETE FROM Layers WHERE Material = '{material}' """)
            self.connection.commit()

            return "Successfully Removed Layer"
        except:
            return "Error Removing Layer"
    
    def update_layers(self, fulldDataSet):
        cursor = self.connection.cursor()
        cursor.execute(f""" UPDATE Layers set
                Material = '{fulldDataSet[0]}'
                Thickness = '{fulldDataSet[1]}'
                'Refract. Index' = '{fulldDataSet[2]}'
                Description = '{fulldDataSet[3]}'

                WHERE Material = '{fulldDataSet[0]}' """)
        self.connection.commit()


