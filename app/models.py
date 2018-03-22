from . import db


class UserProfile(db.Model):
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    gender =  db.Column(db.String(1))
    email = db.Column(db.String(255), unique=True)
    location = db.Column(db.String(80))
    biography = db.Column(db.Text)
    image = db.Column(db.String(255))
    created_on = db.Column(db.String(80))
    uid = db.Column(db.Integer, primary_key=True, autoincrement=False)
    
    __tablename__ = "profiles"
    
    
    def __init__(self,first_name, last_name, gender,email,location,biography,image,created_on,uid):
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.email = email
        self.location = location
        self.biography = biography
        self.image = image
        self.created_on = created_on
        self.uid = uid

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
			return "User: {0} {1}".format(self.firstname, self.lastname)