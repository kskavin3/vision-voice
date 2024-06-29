from VisionVoice import db,app
from VisionVoice.Models import Video
app.app_context().push()
db.create_all()
ap=Video("Hello","afd","afadf","asdasdasdas")
db.session.add(ap)
db.session.commit()

db.session.delete(ap)
db.session.commit()