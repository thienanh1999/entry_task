import sys, os, django
import hashlib
import random
import datetime
sys.path.append("/entry_task")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "entry_task.settings")
django.setup()

from entry_task.commonlib.models import User, Event, Category, Like, Comment, Participant, EventCategory

superuser = 'athen'
superpassword = '1'

NUMBER_OF_EVENT = 10000
NUMBER_OF_USER = 10000
NUMBER_OF_LIKE = 1000000
NUMBER_OF_PARTICIPANT = 1000000
NUMBER_OF_COMMENT = 10000
NUMBER_OF_EVENT_CATEGORY = 1000000

BATCH = 100


def create_user():
    count = 0
    for i in range(NUMBER_OF_USER):
        objs = []
        for id in range(BATCH):
            count = count + 1
            hash_key = 'key'
            objs.append(User(
                username='user' + str(count),
                fullname='Vu Thi Thien Anh - ' + str(count),
                hashed_password=hashlib.sha256('1' + hash_key).hexdigest(),
                hash_key=hash_key
            ))
        try:
            User.objects.bulk_create(objs)
            print "Created " + str(count) + " users."
        except:
            pass


def create_event():
    count = 0
    for i in range(NUMBER_OF_EVENT):
        objs = []
        for id in range(BATCH):
            count = count + 1
            objs.append(Event(
                title='title',
                start=datetime.datetime.utcnow(),
                end=datetime.datetime.utcnow(),
                location='location'
            ))
        try:
            Event.objects.bulk_create(objs)
            print "Created " + str(count) + " events."
        except:
            pass


def create_category():
    count = 0
    for i in range(3):
        try:
            Category.objects.create(name='Cat' + str(i + 1))
            count = count + 1
            print "Created " + str(count) + " categories."
        except:
            pass


def create_like():
    count = 0
    objs = []
    for user_id in range(NUMBER_OF_USER*BATCH):
        for event_id in range(NUMBER_OF_EVENT*BATCH):
            count = count + 1
            objs.append(Like(
                user_id=user_id+1,
                event_id=event_id+1
            ))
            if count % BATCH == 0:
                try:
                    Like.objects.bulk_create(objs)
                    print "Created " + str(count) + " likes."
                    objs = []
                except:
                    pass
            if count == NUMBER_OF_LIKE:
                return


def create_comment():
    count = 0
    for i in range(NUMBER_OF_COMMENT):
        objs = []
        for id in range(BATCH):
            count = count + 1
            user = random.randint(0, NUMBER_OF_USER - 1)
            event = random.randint(0, NUMBER_OF_EVENT - 1)
            objs.append(Comment(
                user_id=user+1,
                event_id=event+1,
                comment="comment",
            ))
        try:
            Comment.objects.bulk_create(objs)
            print "Created " + str(count) + " comments."
        except:
            pass


def create_participant():
    count = 0
    objs = []
    for user_id in range(NUMBER_OF_USER*BATCH):
        for event_id in range(NUMBER_OF_EVENT*BATCH):
            count = count + 1
            objs.append(Participant(
                user_id=user_id+1,
                event_id=event_id+1
            ))
            if count % BATCH == 0:
                try:
                    Participant.objects.bulk_create(objs)
                    print "Created " + str(count) + " participants."
                    objs = []
                except:
                    pass
            if count == NUMBER_OF_PARTICIPANT:
                return


def create_event_category():
    count = 0
    objs = []
    for event_id in range(NUMBER_OF_EVENT * BATCH):
        for category_id in range(3):
            count = count + 1
            objs.append(EventCategory(
                event_id=event_id+1,
                category_id=category_id+1,
            ))
            if count % BATCH == 0:
                try:
                    EventCategory.objects.bulk_create(objs)
                    print "Created " + str(count) + " event-category objects."
                    objs = []
                except:
                    pass
            if count == NUMBER_OF_EVENT_CATEGORY:
                return


if __name__ == '__main__':
    create_user()
    create_event()
    create_category()
    create_like()
    create_comment()
    create_participant()
    create_event_category()
