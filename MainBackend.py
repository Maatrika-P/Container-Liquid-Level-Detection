from flask import Flask, jsonify, render_template, Response
import cv2 as cv
import processing as p
import random
import os

app = Flask(__name__)
camera = cv.VideoCapture('C:\\xampp\\htdocs\\PHP\\Bottle_Damage_Detection_Backend\\F.mp4')
result_path = 'C:\\xampp\\htdocs\\PHP\\Bottle_Damage_Detection_Backend\\Frames'
list = []
frame_count = 0


@app.route('/new_rows')
def new_rows():
    rows = []
    for i in list:
        rows.append(i)
        yield jsonify(rows)


def vid_frames():
    while True:
        
        success, frames = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv.imencode('.jpg', frames)
            frames = buffer.tobytes()

            cv.imwrite(os.path.join(result_path,'frame'+str(frame_count)+'.jpg'), frames) 
            frame_count += 1
            for filename in sorted(os.listdir(result_path)):
                if filename.endswith('.jpg'):
                # Read the current image file using cv2.imread()
                    img_path = os.path.join(result_path, filename)
                    
            item = p.Colored_Liquid(img_path)
            # print("Item read")
            list.append(item)


@app.route('/')
def front_end():
    return render_template('index.html')


@app.route('/video')
def video():
    # switch_webpage()
    return Response(vid_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/table')
def table():
    return render_template('index.html', list)


if __name__ == '__main__':
    app.run()

