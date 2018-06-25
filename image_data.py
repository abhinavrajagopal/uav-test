""" Extract the GPS coordinates from images"""

import piexif

class image_data(object):
    exif_data = None
    img_path = None

    def __init__(self, img_path):
        self.img_path = img_path
        self.get_exif_data()
        super(image_data, self).__init__()
    
    def get_exif_data(self):
        self.exit_data = piexif.load(self.img_path)
        return self.exif_data

    def get_if_exist(self, data, key):
        if key in data:
            return data[key]
        return None

    def convert_to_degrees(self, value):
        degrees = float(value[0][0]) / float(value[0][1])
        minutes = float(value[1][0]) / float(value[1][1])
        seconds = float(value[2][0]) / float(value[2][1])
        return degrees + (minutes / 60.0) + (seconds / 3600.0)
    
    def get_lat_lng(self):
        lat = None
        lng = None
        exif_data = self.get_exif_data()
        if exif_data and "GPS" in exif_data:
            gps_data = exif_data["GPS"]
            gps_latitude = self.get_if_exist(gps_data, piexif.GPSIFD.GPSLatitude)
            gps_latitude = self.get_if_exist(gps_data, piexif.GPSIFD.GPSLatitudeRef)
            gps_longitude = self.get_if_exist(gps_data, piexif.GPSIFD.GPSLongitude)
            gps_longitude = self.get_if_exist(gps_data, piexif.GPSIFD.GPSLongitudeRef)
            if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
                gps_latitude_ref = gps_latitude_ref.decode("UTF-8")
                gps_longitude_ref = gps_longitude_ref.decode("UTF-8")
                lat = self.convert_to_degrees(gps_latitude)
                if gps_latitude_ref != 'N':
                    lat = 0 - lat
                lng = self.convert_to_degrees(gps_longitude)
                if gps_longitude_ref != 'E':
                    lng = 0 - lng
        return lat, lng

