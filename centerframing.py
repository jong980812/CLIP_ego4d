# Copyright (c) OpenMMLab. All rights reserved.
import os
import os.path as osp
import subprocess
import pandas as pd
import csv

video_root = '/local_datasets/ego4d_clips/lta_4s/videos'
anno_file = 'annotations/my_annotations/lta_val.csv' #! 참조할 어노테이션
event_root = '/data/datasets/ego4d_center/lta/images_val' #! 클립이 저장되는 위치


cleaned = pd.read_csv(anno_file, header=None, delimiter=',')
# action_unique_id = list(cleaned[0][:])
# #####!!!!!!!!!!!!!!!!!!!!!!!!
video_id = list(cleaned[0][:])#! 항상 신경쓰기
# state_change=list(cleaned[7][:])
# start = list(cleaned[3][:])
# stop = list(cleaned[4][:])
#!#!#!#!!###################
# verb = list(cleaned[8][:])
# noun = list(cleaned[10][:])

def convert_second(date_time):
     hour = float(date_time[0:2]) * 3600
     min = float(date_time[3:5]) * 60
     sec = float(date_time[6:])
     return hour + min + sec
def centerframe():
     videos = os.listdir(video_root)
     videos = set(videos)
     for i, k in enumerate(video_id):#! timestamp csv의 actionm unique id가 저장된 클립들 mp4이름임.
        k=str(k)
        if k + '.mp4' not in videos:
            print(f'video {k} has not been downloaded')
            continue
        video_path = osp.join(video_root, k+'.mp4')
        result = subprocess.run(['ffmpeg', '-i', video_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stderr.decode()
        duration_hms = output[output.index('Duration: ') + 10:output.index(', start')]
        hours, minutes, seconds = duration_hms.split(':')
        duration=float(seconds)
        center=duration/2.0
        output_filename=k.split('.')[0]+".jpg"# aa.mp4  aa, mp4
        command = [
            'ffmpeg', '-i',
            '"%s"' % video_path, '-ss',
            str(center),'-vframes','1',
            '-threads', '12',
            '"%s"' % osp.join(event_root, output_filename)
        ]
        command = ' '.join(command)
        try:
            subprocess.check_output(
                command, shell=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError:
            print(
                f'Extracting of the center frame {k} of Video {k} Failed',
                flush=True)
if __name__=="__main__":
    centerframe()