# Your name: Josh Richman
# Your student id: 80041347
# Your email: richmajo@umich.edu
# List who you have worked with on this homework:

import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn, path

def load_rest_data(db):
    """
    This function accepts the file name of a database as a parameter and returns a nested
    dictionary. Each outer key of the dictionary is the name of each restaurant in the database, 
    and each inner key is a dictionary, where the key:value pairs should be the category, 
    building, and rating for the restaurant.
    """
    cur, conn, path = open_database(db)
    restdic = {}
    cur.execute("SELECT name, category_id, building_id, rating FROM restaurants")
    rests = cur.fetchall()
    for rest in rests:
        hold = {}
        cur.execute("SELECT category FROM categories WHERE id = (?)", (rest[1],))
        cat = cur.fetchone()
        cur.execute("SELECT building FROM buildings WHERE id = (?)", (rest[2],))
        build = cur.fetchone()
        hold['category'] = cat[0]
        hold['building'] = build[0]
        hold['rating'] = rest[3]
        restdic[rest[0]] = hold
    return restdic
    pass

def plot_rest_categories(db):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the count of number of restaurants in each category.
    """
    cur, conn, path = open_database(db)
    catdic = {}
    cur.execute("SELECT id, category FROM categories")
    cats = cur.fetchall()
    cur.execute("SELECT category_id FROM restaurants")
    rests = cur.fetchall()
    for rest in rests:
        catdic[cats[rest[0]-1][1]] = catdic.get(cats[rest[0]-1][1], 0) + 1
    catdicsorted = sorted(catdic.items(), key=lambda x:x[1], reverse=False)
    x=[]
    y=[]
    for it in catdicsorted:
        y.append(it[0])
        x.append(it[1])
        
    plt.barh(y=y,width=x)
    plt.title('Number of Restaurants Per Category')
    plt.xlabel('Number of Restaurants')
    plt.ylabel('Category')
    plt.tick_params(axis='x',width=1)
    plt.savefig(path + "/plot_rest_categories.png", bbox_inches='tight')
    plt.clf()
    return catdic
    pass

def find_rest_in_building(building_num, db):
    '''
    This function accepts the building number and the filename of the database as parameters and returns a list of 
    restaurant names. You need to find all the restaurant names which are in the specific building. The restaurants 
    should be sorted by their rating from highest to lowest.
    '''
    cur, conn, path = open_database(db)
    rests = []
    cur.execute("SELECT id FROM buildings WHERE building = (?)", (building_num,))
    build_id = cur.fetchone()
    cur.execute("SELECT name, rating FROM restaurants WHERE building_id = (?)", build_id)
    for build in cur:
        rests.append(build)
    restr = sorted(rests, key=lambda x:x[1], reverse=True)
    lis = []
    for rest in restr:
        lis.append(rest[0])
    return lis
    pass

#EXTRA CREDIT
def get_highest_rating(db): #Do this through DB as well
    """
    This function return a list of two tuples. The first tuple contains the highest-rated restaurant category 
    and the average rating of the restaurants in that category, and the second tuple contains the building number 
    which has the highest rating of restaurants and its average rating.

    This function should also plot two barcharts in one figure. The first bar chart displays the categories 
    along the y-axis and their ratings along the x-axis in descending order (by rating).
    The second bar chart displays the buildings along the y-axis and their ratings along the x-axis 
    in descending order (by rating).
    """
    cur, conn, path = open_database(db)
    rests = []
    
    cur.execute("SELECT * FROM categories")
    cats = cur.fetchall()
    catdic = {}
    catdic2 = {}
    cur.execute("SELECT * FROM buildings")
    builds = cur.fetchall()
    builddic = {}
    builddic2 = {}
    cur.execute("SELECT * FROM restaurants")
    rests = cur.fetchall()
    
    for rest in rests:
        catdic[cats[rest[2]-1][1]] = catdic.get(cats[rest[2]-1][1], 0) + rest[4]
        catdic2[cats[rest[2]-1][1]] = catdic2.get(cats[rest[2]-1][1], 0) + 1
        builddic[builds[rest[3]-1][1]] = builddic.get(builds[rest[3]-1][1], 0) + rest[4]
        builddic2[builds[rest[3]-1][1]] = builddic2.get(builds[rest[3]-1][1], 0) + 1
    avgCat = {}
    avgBuild = {}
    for key in catdic:
        avgCat[key] = catdic[key] / catdic2[key]
    for key in builddic:
        avgBuild[key] = builddic[key] / builddic2[key]
    sortcat = sorted(avgCat.items(), key=lambda x:x[1], reverse=False)
    sortbuild = sorted(avgBuild.items(), key=lambda x:x[1], reverse=False)

    x=[]
    y=[]
    x2=[]
    y2=[]
    for it in sortcat:
        y.append(it[0])
        x.append(it[1])
    for it in sortbuild:
        y2.append(str(it[0]))
        x2.append(it[1])
        
    plt.barh(y=y,width=x)
    plt.title('Average Rating Per Category')
    plt.xlabel('Rating')
    plt.ylabel('Category')
    plt.savefig(path + "/get_highest_category_rating.png", bbox_inches='tight')
    plt.clf()
    plt.barh(y=y2,width=x2)
    plt.title('Average Rating Per Building')
    plt.xlabel('Rating')
    plt.ylabel('Building')
    plt.savefig(path + "/get_highest_building_rating.png", bbox_inches='tight')
    plt.clf()
    
    return([sortcat[len(sortcat)-1],sortbuild[len(sortbuild)-1]])
    pass

#Try calling your functions here
def main():
    pass

class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.highest_rating = [('Deli', 4.6), (1335, 4.8)]

    def test_load_rest_data(self):
        rest_data = load_rest_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, dict)
        self.assertEqual(rest_data['M-36 Coffee Roasters Cafe'], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_plot_rest_categories(self):
        cat_data = plot_rest_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_find_rest_in_building(self):
        restaurant_list = find_rest_in_building(1140, 'South_U_Restaurants.db')
        self.assertIsInstance(restaurant_list, list)
        self.assertEqual(len(restaurant_list), 3)
        self.assertEqual(restaurant_list[0], 'BTB Burrito')

    def test_get_highest_rating(self):
        highest_rating = get_highest_rating('South_U_Restaurants.db')
        self.assertEqual(highest_rating, self.highest_rating)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
