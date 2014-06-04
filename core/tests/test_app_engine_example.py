from google.appengine.ext import ndb

from ndbtestcase import AppEngineTestCase


class Thing(ndb.Model):
    stuff = ndb.StringProperty()


class ExampleTestCase(AppEngineTestCase):
    """Example App Engine testcase"""

    def setUp(self):
        thing = Thing(stuff="One")
        thing.put()

    def test_thing_one(self):
        thing = Thing(stuff="Two")
        thing.put()
        self.assertEquals(Thing.query().count(), 2)

    def test_thing_two(self):
        thing = Thing(stuff="Three")
        thing.put()
        self.assertEquals(Thing.query().count(), 2)

    def tearDown(self):
        pass
