from VisionVoice import app,request,jsonify,db
from flask import render_template,send_from_directory,url_for,send_file,redirect



@app.route('/', methods= ['GET','POST'])
def home():
    return  {"code":201}

if __name__=='__main__':
    app.run(debug=False)