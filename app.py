import os
import simplekml
import csv
import argparse
import pysrt
import fnmatch
from image_data import image_data
from geopy.distance import vincenty
from datetime import datetime, timedelta

def construct_img_map(img_dir, img_pattern):
       imgToGPS = {}
       img_list = os.listdir(img_dir)
       for image in img_list:
            if fnmatch.fnmatch(image, img_pattern):
                img_path = '/'.join([img_dir, image])
                lat, lng = image_data(img_path).get_lat_lng()
            if lat and lng:
                imgToGPS[image] = (lat, lng)
       return imgToGPS

def get_img_radius(curr_coords, imgToGPS, radius):
        img_list = []
        for image, coords in imgToGPS.items():
            if vincenty(curr_coords, coords).meters <= radius:
                img_list.append(image)
        return img_list

def get_coords_srt(srt):
        return (curr_lat, curr_lng)
def get_img_list(srt_list, imgToGPS, radius):
        return img_list
def get_srt_time(srt, curr_time, end_time):
        return srt.slice(
                starts_after={'minutes':curr_time.minute, 'seconds':curr_time.second},
                starts_before={'minutes':end_time.minute, 'seconds':end_time.second})
    
def write_to_csv(data, csv_name):
        with open(csv_name, "w") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(data)

def create_filename(prefix, filename, ext):
        filename = filename.split(".")[0]
        return prefix + filename + "." + ext

def video_process(video, vid_path, imgToGPS):
        srt = pysrt.open(vid_path)
        curr_time = datetime(2000, 1, 1 ,minute = 0, second = 0)
        next_time = curr_time + timedelta(seconds = 1)
        data = []
        data.append(["time", "image_names"])
        while True:
            parts = get_srt_time(srt, curr_time, next_time)
            if not parts:
                break
            img_list = get_img_radius(parts, imgToGPS, vid_radius)
            curr_time, next_time = next_time, next_time + timedelta(seconds = 1)
            data.append([curr_time.strftime("%M:%S"), ", ".join(img_list)])
            write_to_csv(data, create_filename("images_", video, "csv"))

def generate_kml(video, vid_path):
        subs = pysrt.open(vid_path)
        data = []
        for srt in subs:
            latitude, longitude = get_coords_srt(srt)
            data.append([sub.start, latitude, longitude])
        csv_name = create_filename("kml_", video, "csv")
        write_to_csv(data, csv_name)
        inputfile = csv.reader(open(csv_name, "r"))
        kml = simplekml.Kml()
        for row in inputfile:
            kml.newpoint(name=row[0], coords=[(row[2], row[1])])
            kml.save(create_filename("", video, "kml"))

def vid_process(imgToGPS, vid_dir, vid_pattern):
        vid_list = os.list_dir(vid_dir)
        for video in vid_list:
            if fnmatch.fnmatch(video, vid_pattern):
                vid_path = '/'.join([vid_dir, video])
                vid_proc(video, vid_path, imgToGPS)
                generate_kml(video, vid_path)

def csv_read(csv_name):
        data = []
        with open(csv_name) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                data.append(row)
        return data

def POI_process(imgToGPS, csv_name):
        assests_data = csv_read(csv_name)
        image_data = []
        image_data.append(["asset_name", "image_names"])
        for asset in assets_data:
            curr_coords = (asset["latitude"], asset["longitude"])
            img_list = img_radius(curr_coords, imgToGPS, poi_radus)
            image_data.append([asset["asset_name"], ", ".join(img_list)])
            write_to_csv(image_data, create_filename("images_", csv_name, "csv"))

def parse_args():
        parser = argparse.ArgumentParser()
        parser.add_argument("vid_radius", type=int)
        parser.add_argument("poi_radius", type=int)
        args = parser.parse_args()
        return args.vid_radius, args.poi_radius

img_dir = "images"
vid_dir = "videos"
img_pattern = "*.JPG"
vid_pattern = "*.SRT"
vid_radius, poi_radius = parse_args()
imgToGPS = construct_img_map(img_dir, img_pattern)
vid_process(imgToGPS, vid_dir, vid_pattern)
POI_process(imgToGPS, "assets.csv") 


