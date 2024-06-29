from VisionVoice import db,app
app.app_context().push()


class Video(db.Model):
    __tablename__="Video"
    id=db.Column(db.Integer,primary_key=True, autoincrement=True, nullable=False)
    video_name=db.Column(db.Text,server_default='')
    video_content=db.Column(db.Text,server_default='')
    video_url=db.Column(db.Text,server_default='')
    video_summary = db.Column(db.Text,server_default='')

    def __init__(self, video_name,video_content,video_url,video_summary):
        self.video_name=video_name
        self.video_content=video_content
        self.video_url=video_url
        self.video_summary=video_summary

    def __repr__(self):
        return f"{self.video_name}"