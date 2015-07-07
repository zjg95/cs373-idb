#!/usr/bin/env python3

# -------
# imports
# -------

import json
import requests
from django.test import TestCase
from . import models
class GOT_Tests (TestCase):

    # Person(first_name, last_name, titles, status, bio)
    def test_person_1(self):

        person = models.Person(first_name='Eddard',
                               last_name='Stark',
                               titles='Lord of Winterfell',
                               status='Dead',
                               bio='Neds bio')
        first_name = person.first_name
        last_name = person.last_name
        titles = person.titles
        status = person.status
        bio = person.bio

        self.assertEqual(first_name, 'Eddard')
        self.assertEqual(last_name,  'Stark')
        self.assertEqual(titles,     'Lord of Winterfell')
        self.assertEqual(status, 	 'Dead')
        self.assertEqual(bio,        'Neds bio')

    def test_region_1(self):

        region = models.Region(name='The North',
                               capital_name=models.Castle(self, name='whatever'),
                               ruling_house=models.House(self, name='that one house'),
                               ruling_lord=models.Person(self, first_name="evil guy", last_name="prob"),
                               description='may the lord bless your soul')
        name = region.name
        capital = region.capital_name
        house = region.ruling_house
        lord = region.ruling_lord
        bio = region.description

        self.assertEqual(name, 'The North')
        self.assertEqual(capital,  models.Castle(self, name='whatever'))
        self.assertEqual(house,     models.House(self, name='that one house'))
        self.assertEqual(lord, 	 models.Person(self, first_name="evil guy", last_name="prob"))
        self.assertEqual(bio,        'may the lord bless your soul')

    def test_castles_1(self):

        castle = models.Castle(name='The North',
                               region_name=models.Region(self, name='whatever'),
                               ruling_house=models.House(self, name='that one house'),
                               ruling_lord=models.Person(self, first_name="evil guy", last_name="prob"),
                               description='may the lord bless your soul')
        name = castle.name
        capital = castle.region_name
        house = castle.ruling_house
        lord = castle.ruling_lord
        bio = castle.description

        self.assertEqual(name, 'The North')
        self.assertEqual(capital,  models.Region(self, name='whatever'))
        self.assertEqual(house,     models.House(self, name='that one house'))
        self.assertEqual(lord, 	 models.Person(self, first_name="evil guy", last_name="prob"))
        self.assertEqual(bio,        'may the lord bless your soul')

class GOT_API_Tests (TestCase):
    url = "http://127.0.0.1:8000"

    def test_api_get_person (self):
        """
        Doing an http get on person 'Ned Stark'.
        Expecting a response with a json object
        containing Ned Starks data members
        """
        response = requests.get(self.url + '/content/api/people/')
        self.assertEqual(response.status_code, 200)
        actual = response.json()  # convert response to json obj
        expected = [{"id":2,"first_name":"Robert","last_name":"Baratheon","status":"Dead","bio":"He loves women"},{"id":3,"first_name":"Tywin","last_name":"Lannister","status":"Dead","bio":"Tywin is (was) pretty scary"},{"id":1,"first_name":"Ned","last_name":"Stark","status":"Dead","bio":"Ned is cool"}]
        self.assertEqual(actual, expected)

    def test_api_get_castle (self):
        """
        Doing an http get on person 'Ned Stark'.
        Expecting a response with a json object
        containing Ned Starks data members
        """
        response = requests.get(self.url + '/content/api/castles/')
        self.assertEqual(response.status_code, 200)
        actual = response.json()  # convert response to json obj
        expected = [{"id":2,"name":"Casterly Rock","region_name":2,"ruling_lord":3,"description":"The seat of house Lannister"},{"id":3,"name":"Storm's End","region_name":3,"ruling_lord":2,"description":"The seat of house Baratheon"},{"id":1,"name":"Winterfell","region_name":1,"ruling_lord":1,"description":"The seat of house Stark"}]
        self.assertEqual(actual, expected)

    def test_api_get_regions (self):
        """
        Doing an http get on person 'Ned Stark'.
        Expecting a response with a json object
        containing Ned Starks data members
        """
        response = requests.get(self.url + '/content/api/regions/')
        self.assertEqual(response.status_code, 200)
        actual = response.json()  # convert response to json obj
        expected = [{"id":3,"name":"Stormlands","capital_name":3,"ruling_lord":2,"description":"The Baratheon lands."},{"id":1,"name":"The North","capital_name":1,"ruling_lord":1,"description":"A big fancy place"},{"id":2,"name":"Westerlands","capital_name":2,"ruling_lord":3,"description":"The Lannister lands"}]
        self.assertEqual(actual, expected)

