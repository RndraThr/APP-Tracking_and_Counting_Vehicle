import pymysql
from datetime import datetime
import requests
import base64
class VehicleRepository:
    """
    Kelas untuk menangani operasi database kendaraan berdasarkan struktur database ataupun API.
    """
    def __init__(self, host, user, password, database):
        """
        Inisialisasi repository dengan konfigurasi database dan API.
        """
        self.api_url = "https://dishub.smartlinks.id/a8ddda94f941c4e530cecebdd2c985d6"
        self.api_auth = "Basic Y2Vrc21hcnRjb3VudGluZ1NjcDEwOmQ5MmU3MTIzYWE1MGM5OTRiODQ4YWJiZWVjZmIwYTBhMDZmMzY3MGRjOGFiYmYxYzU5MTQ2Y2ExMGRlOTJjOGEwYmM2ZGMxNzE2OGE0NjFmYTk5ZDg4MDlhMDQ3YTgyYjRkZjcwMmRhZTFkOGJiODlmYzcyOWZjZDJkZjkxMjk3"
        
        self.db_config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database
        }
        
        self.db = None
        self.cursor = None
        self.db_available = False

        try:
            self.db_pool = pymysql.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True
            )
            self.connect()
            self.db_available = True
            print("Database connection successful.")
        except Exception as e:
            print(f"Database connection failed: {e}. Will use API only.")

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

    def send_to_api(self, klasifikasikendaraan, warnakendaraan, drivingspeed, 
                    drivingdirection, lokasisurvey):
        """
        Mengirim data kendaraan ke API Dishub.
        """
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            payload = {
                'tgl': current_time,
                'waktusurvey': current_time,
                'klasifikasikendaraan': klasifikasikendaraan,
                'warnakendaraan': warnakendaraan,
                'drivingspeed': str(drivingspeed),
                'drivingdirection': drivingdirection,
                'lokasisurvey': lokasisurvey
            }

            headers = {
                'Authorization': self.api_auth
            }

            response = requests.post(
                self.api_url,
                data=payload,
                headers=headers
            )
            
            if not isinstance(drivingspeed, (int, float)):
                try:
                    drivingspeed = float(drivingspeed)
                except ValueError:
                    print("Invalid speed value")
                    return False

            if response.status_code == 200:
                print(f"Data successfully sent to API: {response.text}")
                return True
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            print(f"Error sending data to API: {str(e)}")
            return False
    
    def save_vehicle(self, vehicle_id, klasifikasikendaraan, timestamp, drivingspeed, 
                drivingdirection, koordinat, warna, lokasisurvey):
        """
        Menyimpan data kendaraan ke database lokal dan mengirim ke API.
        """
        db_success = False
        
        # Simpan ke database jika tersedia
        if self.db_available:
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
                db_success = True
                print(f"Data saved to database for ID: {vehicle_id}")
            except Exception as e:
                print(f"Error saving to database: {str(e)}. Will try API only.")
                if self.db_available and hasattr(self, 'db') and self.db:
                    try:
                        self.db.rollback()
                    except:
                        pass

        # Selalu coba kirim ke API
        api_success = False
        try:
            api_success = self.send_to_api(
                klasifikasikendaraan=klasifikasikendaraan,
                warnakendaraan=warna,
                drivingspeed=drivingspeed,
                drivingdirection=drivingdirection,
                lokasisurvey=lokasisurvey
            )
            if api_success:
                print(f"Data sent to API for ID: {vehicle_id}")
        except Exception as e:
            print(f"Error sending to API: {str(e)}")

        # Berhasil jika database atau API berhasil
        return db_success or api_success

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