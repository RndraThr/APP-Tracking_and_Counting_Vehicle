import pymysql
from datetime import datetime

class VehicleRepository:
    """
    Kelas untuk menangani operasi database kendaraan berdasarkan struktur database vehicle_db.
    """
    def __init__(self, host, user, password, database):
        self.db_config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database
        }
        self.db = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            self.db = pymysql.connect(**self.db_config)
            self.cursor = self.db.cursor()
            return True
        except Exception as e:
            print(f"Database connection error: {e}")
            return False

    def test_connection(self):
        try:
            if self.db is None or not self.db.open:
                return self.connect()
            self.cursor.execute("SELECT 1")
            return True
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False

    def save_vehicle(self, vehicle_id, klasifikasikendaraan, timestamp, drivingspeed, 
                    drivingdirection, koordinat, warna, lokasisurvey):
        """
        Menyimpan data kendaraan ke database sesuai dengan struktur tabel vehicle_data.
        """
        try:
            sql = """
                INSERT INTO vehicle_data 
                (vehicle_id, klasifikasikendaraan, timestamp, drivingspeed, 
                drivingdirection, koordinat, warna, lokasisurvey) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """

            self.cursor.execute(sql, (
                str(vehicle_id),
                klasifikasikendaraan,
                timestamp,
                float(drivingspeed) if drivingspeed is not None else 0,
                drivingdirection,
                koordinat,
                warna,
                lokasisurvey
            ))
            self.db.commit()
            return True

        except pymysql.Error as e:
            print(f"Database error: {e}")
            self.db.rollback()
            return False

    def get_vehicle_count_by_location(self, lokasisurvey):
        """
        Mendapatkan jumlah kendaraan berdasarkan lokasi survei.
        """
        try:
            self.cursor.execute(
                "SELECT COUNT(*) FROM vehicle_data WHERE lokasisurvey = %s",
                (lokasisurvey,)
            )
            return self.cursor.fetchone()[0]
        except pymysql.Error as e:
            print(f"Database error: {e}")
            return 0

    def get_vehicle_statistics(self, lokasisurvey):
        """
        Mendapatkan statistik kendaraan berdasarkan klasifikasi untuk lokasi tertentu.
        """
        try:
            sql = """
                SELECT 
                    klasifikasikendaraan,
                    COUNT(*) as total,
                    AVG(drivingspeed) as avg_speed
                FROM vehicle_data 
                WHERE lokasisurvey = %s
                GROUP BY klasifikasikendaraan
            """
            self.cursor.execute(sql, (lokasisurvey,))
            return self.cursor.fetchall()
        except pymysql.Error as e:
            print(f"Database error: {e}")
            return []

    def close(self):
        """
        Menutup koneksi database.
        """
        try:
            self.cursor.close()
            self.db.close()
        except pymysql.Error as e:
            print(f"Error closing database connection: {e}")