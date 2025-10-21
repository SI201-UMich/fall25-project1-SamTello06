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
    #takes into account the 'Quantity' column
    state_cat = {}
    for i in range(len(d['State'])):
        state = d['State'][i]
        category = d['Category'][i]
        quant = int(d['Quantity'][i])
        if state not in state_cat:
            state_cat[state] = {}
        if category not in state_cat[state]:
            state_cat[state][category] = quant
        else:
            state_cat[state][category] += quant

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


def highest_avg_sale_subcategory_per_region(d):
    # takes in nested dict from load_csv
    # returns a dict where keys are region and values are 
    # the subcategory with the highest average sale in that region

    # creates a nested dict with regions and subcategories 
    # and their total sales and counts
    region_subcat = {}
    for i in range(len(d['Region'])):
        region = d['Region'][i]
        subcat = d['Sub-Category'][i]
        sale = float(d['Sales'][i])

        if region not in region_subcat:
            region_subcat[region] = {}
        if subcat not in region_subcat[region]:
            region_subcat[region][subcat] = {'total_sales': 0, 'count': 0}

        region_subcat[region][subcat]['total_sales'] += sale
        region_subcat[region][subcat]['count'] += 1


    # finds the subcategory with the largest avg in each region 
    # and returns a dict with region and subcategory
    result = {}
    for reg in region_subcat:
        max_avg = 0
        max_subcat = ''
        for subcat in region_subcat[reg]:
            total_sales = region_subcat[reg][subcat]['total_sales']
            count = region_subcat[reg][subcat]['count']
            avg_sale = total_sales / count
            if avg_sale > max_avg:
                max_avg = avg_sale
                max_subcat = subcat
        result[reg] = max_subcat
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
        # Main dataset for general tests
        self.data = {
            'State': ['California', 'California', 'Texas', 'Texas', 'Florida', 'Florida'],
            'Category': ['Furniture', 'Office Supplies', 'Furniture', 'Office Supplies', 'Technology', 'Furniture'],
            'Quantity': ['3', '10', '2', '5', '4', '1'],
            'Region': ['West', 'West', 'Central', 'Central', 'South', 'South'],
            'Sub-Category': ['Chairs', 'Paper', 'Tables', 'Phones', 'Machines', 'Chairs'],
            'Sales': ['300', '120', '250', '500', '1000', '200']
        }

        # Empty data for edge tests
        self.empty_dict = {
            'State': [], 'Category': [], 'Quantity': [],
            'Region': [], 'Sub-Category': [], 'Sales': []
        }

    #  frequent_category_per_state 
    def test_frequent_category_per_state_general_case1(self):

        result = frequent_category_per_state(self.data)
       
        self.assertEqual(result['California'], 'Office Supplies')
        self.assertEqual(result['Texas'], 'Office Supplies')
        self.assertEqual(result['Florida'], 'Technology')

    def test_frequent_category_per_state_general_case2(self):
        data_tie = {
            'State': ['Nevada', 'Nevada'],
            'Category': ['Furniture', 'Technology'],
            'Quantity': ['5', '5'],
            'Region': ['West', 'West'],
            'Sub-Category': ['Chairs', 'Phones'],
            'Sales': ['200', '300']
        }
        result = frequent_category_per_state(data_tie)
        self.assertIn(result['Nevada'], ['Furniture', 'Technology'])

    def test_frequent_category_per_state_edge_case1(self):
        result = frequent_category_per_state(self.empty_dict)
        self.assertEqual(result, {})

    def test_frequent_category_per_state_edge_case2(self):
        single_entry = {
            'State': ['Oregon'], 'Category': ['Furniture'], 'Quantity': ['1'],
            'Region': ['West'], 'Sub-Category': ['Chairs'], 'Sales': ['50']
        }
        result = frequent_category_per_state(single_entry)
        self.assertEqual(result, {'Oregon': 'Furniture'})

    #  highest_avg_sale_subcategory_per_region 
    def test_highest_avg_sale_subcategory_per_region_general_case1(self):
        result = highest_avg_sale_subcategory_per_region(self.data)
        

        self.assertEqual(result['West'], 'Chairs')
        self.assertEqual(result['Central'], 'Phones')
        self.assertEqual(result['South'], 'Machines')

    def test_highest_avg_sale_subcategory_per_region_general_case2(self):
        data_multi = {
            'Region': ['East', 'East', 'East', 'East'],
            'Sub-Category': ['Phones', 'Phones', 'Tables', 'Tables'],
            'Sales': ['100', '300', '200', '200'],
            'State': [], 'Category': [], 'Quantity': []
        }
        result = highest_avg_sale_subcategory_per_region(data_multi)

        self.assertIn(result['East'], ['Phones', 'Tables'])

    def test_highest_avg_sale_subcategory_per_region_edge_case1(self):

        result = highest_avg_sale_subcategory_per_region(self.empty_dict)
        self.assertEqual(result, {})

    def test_highest_avg_sale_subcategory_per_region_edge_case2(self):

        single_entry = {
            'Region': ['Midwest'], 'Sub-Category': ['Copiers'], 'Sales': ['900'],
            'State': [], 'Category': [], 'Quantity': []
        }
        result = highest_avg_sale_subcategory_per_region(single_entry)
        self.assertEqual(result, {'Midwest': 'Copiers'})


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
    write_results(highest_avg_sale_subcategory_per_region(load_results('SampleSuperstore.csv')), 'output.txt')


    #call tests
    unittest.main(verbosity=2)

main()