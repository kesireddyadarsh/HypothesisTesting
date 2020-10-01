#import re
import csv
import xlrd
import numpy as np
from datetime import datetime
from scipy import stats
import statistics

_fatality_map = None
_case_map = None
_hsptlztn_map = None
_icu_map = None
_population_map = None
_grp_map = None
_testing_map = None
_fips_map = None
_density_map = None
_travel_map = None
_metro_map = None
_adj_map = None

def ztest(a, b):
    diff = [i-j for i,j in zip(a, b)]
    std = statistics.stdev(diff)
    mean = sum(diff)/len(diff)
    se = std / len(diff)**(1/2)
    z_value = (mean-0) / se
    p_value = stats.norm.cdf(z_value)
    return p_value

'''
Moving average / Moving mean
@x_array: the original array
@unit: period of time. eg. 7 days 
'''
def moving_avg(x_array, unit):
    return np.convolve(x_array, np.ones(unit), 'valid') / unit

'''
@county: for getting one single county
@tsa: for getting a whole TSA area which contains several counties
@date_range: eg. "04-13~09-21"
@accu_format: accumulated number or daily number
'''
def get_fatality(county=None, tsa=None, date_range=None, accu_format=False):
    global _fatality_map
    if _fatality_map == None:
        target_file = "raw/Texas COVID-19 Fatality Count Data by County.xlsx"
        wb = xlrd.open_workbook(target_file)
        sht = wb.sheet_by_index(0)
        title_row = 2
        county1_row, county254_row = 3, 3+254
        date_col1 = 1
        _fatality_map = {
            'date_from': sht.cell_value(2, date_col1), # Fatalities 03-07
            'total_days': sht.ncols - 2,
        }

        for i in range(county1_row, county254_row):
            county_text = sht.cell_value(i, 0).upper().strip()
            _fatality_map[county_text] = []
            for j in range(date_col1, sht.ncols):
                try:
                    text = sht.cell_value(i, j)
                    v = round(float(text), 2)
                except ValueError as e:
                    text = temp_text
                    v = round(float(text), 2)
                temp_text = text
                _fatality_map[county_text].append(v)

    if county != None:
        county = county.upper()
        res_list = _fatality_map[county]
    elif tsa != None:
        tsa = tsa.upper()
        county_list = get_region2county(tsa)

        all_county_list = []
        for rec in county_list:
            one_county = _fatality_map[rec]
            all_county_list.append(one_county)
        res_list = [sum(i) for i in zip(*all_county_list)]

    # in numpy format
    res_array = np.array(res_list)
    if accu_format == False:
        res_array = np.diff(res_array)

    if date_range != None:
        t1, t2 = date_range.split('~')
        fixed_str = '2020-{}'.format(_fatality_map['date_from'][-5:])
        data_t1 = datetime.strptime(fixed_str, '%Y-%m-%d')
        data_total_days = _fatality_map['total_days']
        user_t1 = datetime.strptime('2020-'+t1, '%Y-%m-%d')
        user_t2 = datetime.strptime('2020-'+t2, '%Y-%m-%d')
        expected_days = (user_t2 - user_t1).days + 1
        if expected_days > data_total_days:
            raise Exception('data_range {} error: {} days (min: {})'.format(date_range, expected_days, data_total_days))
        start_idx = (user_t1 - data_t1).days
        end_idx = (user_t2 - data_t1).days + 1
        return res_array[start_idx:end_idx]

    return res_array

'''
@county: for getting one single county
@date_range: eg. "04-13~09-21"
@accu_format: accumulated number or daily number
@number_form: case ->  numbers of cases 
              infection -> infection rate 
              transmission -> trasmission rate
@mv_avg_days: moving average days              
'''
def get_cases(county, date_range=None, accu_format=False, number_form='infection', mv_avg_days=7):
    global _case_map
    county = county.upper()
    if _case_map == None:
        target_file = "raw/Texas COVID-19 Case Count Data by County.xlsx"
        wb = xlrd.open_workbook(target_file)
        sht = wb.sheet_by_index(0)
        title_row = 2
        county1_row, county254_row = 3, 3+254
        date_col1 = 1
        _case_map = {
            'date_from': sht.cell_value(2, date_col1), # Caess 03-04
            'total_days': sht.ncols - 2,
        }

        for i in range(county1_row, county254_row):
            county_text = sht.cell_value(i, 0).upper().strip()
            _case_map[county_text] = []
            for j in range(date_col1, sht.ncols):
                try:
                    text = sht.cell_value(i, j)
                    v = round(float(text), 2)
                except ValueError as e:
                    text = temp_text
                    v = round(float(text), 2)
                temp_text = text
                _case_map[county_text].append(v)

    # number_form
    if number_form == 'case':
        res_list = list(_case_map[county])
    if number_form ==  'infection':
        pop = get_population(county) 
        res_list = [round(v / pop * 10**6, 2) for v in _case_map[county]]
    elif number_form == 'transmission':
        pop = get_population(county) 
        res_list = [round(v / pop * 10**6, 2) for v in _case_map[county]]
        res_list = moving_avg(res_list, mv_avg_days)

    # in numpy format
    res_array = np.array(res_list)
    if accu_format == False:
        res_array = np.diff(res_array)

    if date_range != None:
        t1, t2 = date_range.split('~')
        fixed_str = '2020-{}'.format(_case_map['date_from'][-5:])
        data_t1 = datetime.strptime(fixed_str, '%Y-%m-%d')
        data_total_days = _case_map['total_days']
        user_t1 = datetime.strptime('2020-'+t1, '%Y-%m-%d')
        user_t2 = datetime.strptime('2020-'+t2, '%Y-%m-%d')
        expected_days = (user_t2 - user_t1).days + 1
        if expected_days > data_total_days:
            raise Exception('data_range {} error: {} days (min: {})'.format(date_range, expected_days, data_total_days))
        start_idx = (user_t1 - data_t1).days
        end_idx = (user_t2 - data_t1).days + 1
        return res_array[start_idx:end_idx]

    return res_array


'''
@county: for getting one single county
@date_range: eg. "04-13~09-21"
@accu_format: accumulated number or daily number
'''
def get_testings(county, date_range=None, accu_format=False):
    global _testing_map
    county = county.upper()
    if _testing_map == None:
        target_file = "raw/Cumulative Tests over Time by County_Legacy.xlsx"
        wb = xlrd.open_workbook(target_file)
        sht = wb.sheet_by_index(0)
        title_row = 1
        county1_row, county254_row = 2, 2+254
        date_col1 = 1
        _testing_map = {
            'date_from': sht.cell_value(1, date_col1), # Tests Through Apr 21
            'total_days': sht.ncols - 2,
        }

        for i in range(county1_row, county254_row):
            county_text = sht.cell_value(i, 0).upper().strip()
            _testing_map[county_text] = []
            for j in range(date_col1, sht.ncols):
                try:
                    text = sht.cell_value(i, j)
                    v = round(float(text), 2)
                except ValueError as e:
                    text = temp_text
                    v = round(float(text), 2)
                temp_text = text
                _testing_map[county_text].append(v)

    res_list = _testing_map[county]

    # in numpy format
    res_array = np.array(res_list)
    if accu_format == False:
        res_array = np.diff(res_array)

    if date_range != None:
        t1, t2 = date_range.split('~')
        _, _, month, day = _testing_map['date_from'].split(' ') # Tests Through Apr 21
        fixed_str = '2020-{}-{}'.format(month, day)
        data_t1 = datetime.strptime(fixed_str, '%Y-%B-%d') # 2020-Apr-21
        data_total_days = _testing_map['total_days']
        user_t1 = datetime.strptime('2020-'+t1, '%Y-%m-%d')
        user_t2 = datetime.strptime('2020-'+t2, '%Y-%m-%d')
        expected_days = (user_t2 - user_t1).days + 1
        if expected_days > data_total_days:
            raise Exception('data_range {} error: {} days (min: {})'.format(date_range, expected_days, data_total_days))
        start_idx = (user_t1 - data_t1).days
        end_idx = (user_t2 - data_t1).days + 1
        return res_array[start_idx:end_idx]

    return res_array
'''
@tsa: TSA area
@gain: for amplifying your cell values, eg. 0.15 -> 15 (%) when gain = 100
@date_range: eg. "04-13~09-21"
@accu_format: accumulated number or daily number
'''
def get_hospitalization(tsa, gain=1, date_range=None, accu_format=False):
    global _hsptlztn_map
    if _hsptlztn_map == None:
        target_file = "raw/Combined Hospital Data over Time by TSA Region.xlsx"
        wb = xlrd.open_workbook(target_file)
        sht = wb.sheet_by_index(0)
        title_row = 2
        area1_row, area22_row = 3, 3+22
        date_col1 = 2 #TSA ID	TSA AREA	2020-04-12	2020-04-12
        _hsptlztn_map = {
            'date_from': sht.cell_value(2, date_col1), # 2020-04-12
            'total_days': sht.ncols - 2,
        }
        for i in range(area1_row, area22_row):
            tsa_text = sht.cell_value(i, 1).upper().strip()
            _hsptlztn_map[tsa_text] = []
            for j in range(date_col1, sht.ncols):
                try:
                    text = sht.cell_value(i, j)
                    v = round(float(text) * gain, 2)
                except ValueError as e:
                    text = temp_text
                    v = round(float(text) * gain, 2)
                temp_text = text
                _hsptlztn_map[tsa_text].append(v)

    # in numpy format
    tsa = tsa.upper()
    res_array = np.array(_hsptlztn_map[tsa])
    if accu_format == False:
        res_array = np.diff(res_array)

    if date_range != None:
        t1, t2 = date_range.split('~')
        data_t1 = datetime.strptime(_hsptlztn_map['date_from'], '%Y-%m-%d')
        data_total_days = _hsptlztn_map['total_days']
        user_t1 = datetime.strptime('2020-'+t1, '%Y-%m-%d')
        user_t2 = datetime.strptime('2020-'+t2, '%Y-%m-%d')
        expected_days = (user_t2 - user_t1).days + 1
        if expected_days > data_total_days:
            raise Exception('data_range {} error: {} days (min: {})'.format(date_range, expected_days, data_total_days))
        start_idx = (user_t1 - data_t1).days
        end_idx = (user_t2 - data_t1).days + 1
        return res_array[start_idx:end_idx]

    return res_array

'''
@tsa: TSA area
@gain: for amplifying your cell values, eg. 0.15 -> 15 (%) when gain = 100
@date_range: eg. "04-13~09-21"
@accu_format: accumulated number or daily number
'''
def get_icu(tsa, gain=1, date_range=None, accu_format=False):
    global _icu_map
    if _icu_map == None:
        target_file = "raw/Combined Hospital Data over Time by TSA Region.xlsx"
        wb = xlrd.open_workbook(target_file)
        sht1 = wb.sheet_by_name('ICU Beds Available')
        sht2 = wb.sheet_by_name('ICU Beds Occupied')
        title_row = 2
        area1_row, area22_row = 3, 3+22
        date_col1 = 2 #TSA ID	TSA AREA	2020-04-12	2020-04-12
        _icu_map = {
            'date_from': sht2.cell_value(2, date_col1), # 2020-04-23
            'total_days': sht2.ncols - 2,
        }
        col_shift = 11 # sht1 starts from 04-12, sht2 starts from 04-23
        for i in range(area1_row, area22_row):
            tsa_text = sht1.cell_value(i, 1).upper().strip()
            _icu_map[tsa_text] = []
            for j in range(date_col1, sht2.ncols):
                try:
                    text1 = sht1.cell_value(i, j+col_shift)
                    text2 = sht2.cell_value(i, j)
                    v1 = int(text1)
                    v2 = int(text2)
                    icu_rate = round(v2/(v1+v2)*gain, 4)
                except (ValueError, ZeroDivisionError) as e:
                    text1 = temp_text1
                    text2 = temp_text2
                    v1 = int(text1)
                    v2 = int(text2)
                    icu_rate = round(v2/(v1+v2)*gain, 4)
                temp_text1 = text1
                temp_text2 = text2
                _icu_map[tsa_text].append(icu_rate)

    # in numpy format
    tsa = tsa.upper()
    res_array = np.array(_icu_map[tsa])
    if accu_format == False:
        res_array = np.diff(res_array)

    if date_range != None:
        t1, t2 = date_range.split('~')
        data_t1 = datetime.strptime(_icu_map['date_from'], '%Y-%m-%d')
        data_total_days = _icu_map['total_days']
        user_t1 = datetime.strptime('2020-'+t1, '%Y-%m-%d')
        user_t2 = datetime.strptime('2020-'+t2, '%Y-%m-%d')
        expected_days = (user_t2 - user_t1).days + 1
        if expected_days > data_total_days:
            raise Exception('data_range {} error: {} days (min: {})'.format(date_range, expected_days, data_total_days))
        start_idx = (user_t1 - data_t1).days
        end_idx = (user_t2 - data_t1).days + 1
        return res_array[start_idx:end_idx]

'''
@tsa: TSA area name
'''
def get_region2county(tsa=None):
    global _grp_map
    if _grp_map == None:
        target_file = 'raw/region2county.tsv'
        with open(target_file, newline='') as csvfile:
            temp = csv.reader(csvfile, delimiter='\t', quotechar='|')
            _grp_map = {}
            for row in temp:
                county, no, tsa_text, _, _ = row
                if county == 'county':
                    continue
                county, tsa_text = county.replace('_', ' '), tsa_text.replace('_', ' ')
                county, tsa_text = county.upper().strip(), tsa_text.upper().strip()
                # no data below these TSA areas in the hospitalization file
                if tsa_text in ['DISTRICT', 'TEXAS', 'YOAKUM', 'BEAUMONT', 'PHARR', 'BROWNWOOD', 'ATLANTA', 'CHILDRESS']:
                    continue
                if tsa_text not in _grp_map:
                    _grp_map[tsa_text] = []
                _grp_map[tsa_text].append(county)

    if tsa == None:
        return _grp_map
    
    tsa = tsa.upper()

    return _grp_map[tsa]

'''
@county: county name
'''
def get_population(county=None): 
    global _population_map
    if _population_map == None:
        _population_map = {}
        population_file = 'raw/2018_txpopest_county.csv'
        with open(population_file, newline='') as csvfile:
            temp = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in temp:
                fips, county_text, c_2010, c_2018, c_2019, *others = row 
                # skip title
                if fips == 'FIPS' or county_text == 'State of Texas':
                    continue
                _population_map[county_text.upper()] = int(c_2019)

    if county == None:
        return _population_map

    county = county.upper()

    return _population_map[county]

'''
@county: county name
'''
def get_fips(county=None): 
    global _fips_map
    if _fips_map == None:
        _fips_map = {}
        target_file = 'raw/2018_txpopest_county.csv'
        with open(target_file, newline='') as csvfile:
            temp = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in temp:
                fips, county_text, c_2010, c_2018, c_2019, *others = row 
                # skip title and the last line
                if fips == 'FIPS' or county_text == 'State of Texas':
                    continue
                _fips_map[county_text.upper()] = '48'+fips

    if county == None:
        return _fips_map

    county = county.upper()

    return _fips_map[county]

'''
Regenerate a file that only contains data in Texas,
because the size of "2020_US_Region_Mobility_Report.csv" is too large.
'''
def filter_travel(): 
    target_file = 'raw/2020_US_Region_Mobility_Report.csv'
    new_csv = 'raw/Mobility_in_Texas.csv'
    new_list = []
    with open(target_file, newline='') as csvfile:
        temp = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in temp:
            country_code, region, state, county_text, metro, iso, fips, date_text, recreation, grocery, park, transit, work, resident = row
            # skip title
            if country_code == 'country_region_code':
                continue
            if state == 'Texas' and county_text.strip() != '':
                new_list.append([date_text, county_text, recreation, grocery, park, transit, work, resident])

    with open(new_csv, 'a+', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['date', 'county_text', 'recreation', 'grocery', 'park', 'transit', 'work', 'resident'])
        for row in new_list:
            spamwriter.writerow(row)

'''
@county: county name
@attr: choices -> 'mean', 'recreation', 'grocery', 'park', 'transit', 'work', 'resident'
@date_range: eg. "04-13~09-21"
'''
def get_travel(county, attr='mean', date_range=None): 
    global _travel_map
    if _travel_map == None:
        _travel_map = {}
        target_file = 'raw/Mobility_in_Texas.csv'
        _travel_map = {
            'date_from': '2020-02-15',
            'total_days': 224,
        }
        with open(target_file, newline='') as csvfile:
            temp = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in temp:
                date_text, county_text, recreation, grocery, park, transit, work, resident = row
                # skip title and the last line
                if date_text == 'date':
                    continue
                county_text = county_text[:-7].upper()
                if county_text not in _travel_map:
                    _travel_map[county_text] = {}
                #  ===== recreation
                if 'recreation' not in _travel_map[county_text]:
                    _travel_map[county_text]['recreation'] = []
                if recreation == '':
                    recreation = 0
                v1 = int(recreation)
                _travel_map[county_text]['recreation'].append(v1)
                #  ===== grocery
                if 'grocery' not in _travel_map[county_text]:
                    _travel_map[county_text]['grocery']= []
                if grocery == '':
                    grocery = 0
                v2 = int(grocery)
                _travel_map[county_text]['grocery'].append(v2)
                #  ===== park
                if 'park' not in _travel_map[county_text]:
                    _travel_map[county_text]['park'] = []
                if park == '':
                    park = 0
                v3 = int(park)
                _travel_map[county_text]['park'].append(v3)
                #  ===== transit
                if 'transit' not in _travel_map[county_text]:
                    _travel_map[county_text]['transit'] = []
                if transit == '':
                    transit = 0
                v4 = int(transit)
                _travel_map[county_text]['transit'].append(v4)
                #  ===== work
                if 'work' not in _travel_map[county_text]:
                    _travel_map[county_text]['work'] = []
                if work == '':
                    work = 0
                v5 = int(work)
                _travel_map[county_text]['work'].append(v5)
                #  ===== resident
                if 'resident' not in _travel_map[county_text]:
                    _travel_map[county_text]['resident'] = []
                if resident == '':
                    resident = 0
                v6 = int(resident)
                _travel_map[county_text]['resident'].append(v6)

                # mean all data from v1 to v6 (except for value 0)
                s = (v1+v2+v3+v4+v5+v6)
                count = 0
                for i in [v1, v2, v3, v4, v5, v6]:
                    if i != 0:
                        count += 1
                if count == 0:
                    mean = 0
                else:
                    mean = round(s / count, 1)
                if 'mean' not in _travel_map[county_text]:
                    _travel_map[county_text]['mean'] = []
                _travel_map[county_text]['mean'].append(mean)

    county = county.upper()
    res_array = list(_travel_map[county][attr])

    if date_range != None:
        t1, t2 = date_range.split('~')
        data_t1 = datetime.strptime(_travel_map['date_from'], '%Y-%m-%d')
        data_total_days = _travel_map['total_days']
        user_t1 = datetime.strptime('2020-'+t1, '%Y-%m-%d')
        user_t2 = datetime.strptime('2020-'+t2, '%Y-%m-%d')
        expected_days = (user_t2 - user_t1).days + 1
        if expected_days > data_total_days:
            raise Exception('data_range {} error: {} days (min: {})'.format(date_range, expected_days, data_total_days))
        start_idx = (user_t1 - data_t1).days
        end_idx = (user_t2 - data_t1).days + 1
        return res_array[start_idx:end_idx]

    return _travel_map[county][attr]


'''
@county: county name
'''
def get_density(county): 
    global _density_map
    if _density_map == None:
        _density_map = {}
        target_file = 'raw/Population Density by Counties in Texas.xlsx'
        wb = xlrd.open_workbook(target_file)
        sht = wb.sheet_by_index(0)

        for i in range(1, sht.nrows):
            density = sht.cell_value(i, 1)[:-6].replace(',', '')
            county_text = sht.cell_value(i, 2).split(',')[0].upper()
            if county_text == 'DE WITT':
                county_text = 'DEWITT'
            _density_map[county_text] = float(density)

    county = county.upper()

    return _density_map[county]

'''
return two kinds of counties in list.
'''
def get_rural_urban_counties(): 
    global _metro_map
    if _metro_map == None:
        _metro_map = []
        r_list, u_list = [], []
        target_file = 'raw/PHR_MSA_County_masterlist.xlsx'
        wb = xlrd.open_workbook(target_file)
        sht = wb.sheet_by_index(0)

        for i in range(1, sht.nrows-2):
            county_text = sht.cell_value(i, 0).strip().upper()
            metro_type = sht.cell_value(i, 7).strip()
            if metro_type == 'Metro':
                u_list.append(county_text)
            else:
                r_list.append(county_text)

        _metro_map = r_list, u_list
        return _metro_map

    county = county.upper()

    return _metro_map 

'''
@county: county namee
'''
def get_adj_counties(county):
    global _adj_map
    if _adj_map == None:
        target_file = 'raw/county_adjacency.txt'
        finding = False
        with open(target_file, newline='') as csvfile:
            temp = csv.reader(csvfile, delimiter='\t', quotechar='|')
            _adj_map = {}
            for r in temp:
                # adj
                if r[0] == '':
                    adj, adj_state = r[2].split(',')
                    adj = adj[:-7].replace('"', '').strip().upper()
                    adj_state = adj_state.replace('"', '').strip()
                    #if state == 'TX' and adj_state == 'TX':
                    if finding == True:
                        if adj_state == 'TX':
                            _adj_map[center].append(adj)
                # center
                else:
                    center, state, adj, adj_state = *r[0].split(','), *r[2].split(',')
                    center = center[:-7].replace('"', '').strip().upper()
                    state = state.replace('"', '').strip()
                    adj = adj.replace('"', '').strip().upper()
                    adj_state = adj_state.replace('"', '').strip()
                    if state == 'TX':
                        finding = True
                        _adj_map[center] = []
                        if adj_state == 'TX':
                            _adj_map[center].append(adj)
                    else:
                        finding = False
    county = county.upper()
    return _adj_map[county]

def main():
    #county_list = get_population().keys()
    #tsa_list = get_region2county().keys()
    adj_counties = get_adj_counties('NUECES')
    print(adj_counties)

if __name__ == '__main__':
    main()

