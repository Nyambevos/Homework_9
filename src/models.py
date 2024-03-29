from mongoengine import EmbeddedDocument, Document
from mongoengine.fields import EmbeddedDocumentField, ListField, StringField, ReferenceField


class Tag(EmbeddedDocument):
    name = StringField()


class Authors(Document):
    fullname = StringField(unique=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Quotes(Document):
    tags =  ListField(EmbeddedDocumentField(Tag))
    author = ReferenceField('Authors')
    quote = StringField()