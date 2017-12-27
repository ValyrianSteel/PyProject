

class Server(db.Model):

    id
    name
    description
    host
    port
    password
    updated_at
    created_at

    def __repr__(self):
        return '<Server(name=%s)>' % self.name

    def save(self):




