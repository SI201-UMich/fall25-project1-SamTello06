import unittest
import os
import csv

def load_results(f):
    # takes in csv file and returns nested dict
    # outer keys are first row of the csv file
    # values are a list of each value in the column

    # open the file
    base_path = os.path.abspath(os.path.dirname(__file__))
    full_path = os.path.join(base_path, f)

    with open(full_path) as fh:
        r = csv.reader(fh)
        rows = list(r)

    header = rows[0]
    d = {}
    for category in header:
        d[category] = []
    for row in rows[1:]:
        for i, col in enumerate(header):
            d[col].append(row[i])
    return d

def frequent_category_per_state(d):
    # takes in nested dict from load_csv
    # returns a dict where keys are states and values are 
    # the most frequent category in that state

    # creates a dict with states and categories and their counts
    state_cat = {}
    for i in range(len(d['State'])):
        state = d['State'][i]
        category = d['Category'][i]
        if state not in state_cat:
            state_cat[state] = {}
        if category not in state_cat[state]:
            state_cat[state][category] = 0
        state_cat[state][category] += 1

    # finds the category with the largest count in each state 
    # and returns a dict with state and frequent category
    result = {}
    for state in state_cat:
        max_count = 0
        max_cat = ''
        for category in state_cat[state]:
            count = state_cat[state][category]
            if count > max_count:
                max_count = count
                max_cat = category
        result[state] = max_cat
    return result


def avg_sales_per_category(d):
    # takes in nested dict from load_csv
    # returns a dict where keys are categories and values are 
    # the average sales for that category

    # creates a dict with categories and their total sales and counts
    cat_sales = {}
    for i in range(len(d['Category'])):
        category = d['Category'][i]
        sales = float(d['Sales'][i])
        if category not in cat_sales:
            cat_sales[category] = {'total_sales': 0, 'count': 0}
        cat_sales[category]['total_sales'] += sales
        cat_sales[category]['count'] += 1

    # calculates the average sales for each category
    result = {}
    for category in cat_sales:
        total_sales = cat_sales[category]['total_sales']
        count = cat_sales[category]['count']
        avg_sales = total_sales / count
        result[category] = avg_sales
    return result

def write_results(d, f):
    #takes in dict and writes to txt file
    #it will be called twice, once for each of the above functions
    with open(f, 'a') as fh:
        for key in d:
            fh.write(f"{key}: {d[key]}\n")
    
    
#unit tests (2 general cases and 2 edge cases per function)
class TestProject1(unittest.TestCase):
    def setUp(self):
        self.superstore_dict = load_results('SampleSuperstore.csv')
        self.empty_dict = {'State': [], 'Category': [], 'Sales': []}
    


def main():
    #writes out a header for output file that says "Frequent Category per State"
    with open('output.txt', 'w') as fh:
        fh.write("Frequent Category per State\n")
        fh.write("---------------------------\n")

    #calls function and writes data to output.txt
    write_results(frequent_category_per_state(load_results('SampleSuperstore.csv')), 'output.txt')

    
    #writes out a header for output file that says "Average Sales per Category"
    with open('output.txt', 'a') as fh:
        fh.write("\nAverage Sales per Category\n")
        fh.write("--------------------------\n")

    #calls function and writes data to output.txt
    write_results(avg_sales_per_category(load_results('SampleSuperstore.csv')), 'output.txt')


    #call tests
    unittest.main(verbosity=2)

main()