import datetime
import os

from decouple import config
from playhouse.postgres_ext import *
from slugify import slugify

uri = config("DATABASE_URL")
print("URI: {}".format(uri))
db = PostgresqlDatabase(uri, autorollback=True)


class BaseModel(Model):
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    def update(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        return super(BaseModel, self).update(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        return super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        database = db


class Extract(BaseModel):
    slug = CharField(unique=True)
    id = PrimaryKeyField()
    title = CharField()
    fields = JSONField()
    output = JSONField()
    metadata = JSONField()
    favorite = BooleanField(default=False)
    review = CharField(null=True)
    review_at = DateTimeField(null=True)

    def save(self, *args, **kwargs):
        # Generate slug
        # Mix of title and 5 random characters in hex
        if not self.slug:
            self.slug = slugify(self.title) + "-" + os.urandom(5).hex()
        return super(Extract, self).save(*args, **kwargs)


class FormSubscriptions(BaseModel):
    id = PrimaryKeyField()
    email = CharField(unique=True)
    subscribed = BooleanField(default=True)


def create_tables():
    db.connect()
    db.create_tables([Extract, FormSubscriptions])
    db.close()


if __name__ == "__main__":
    create_tables()
