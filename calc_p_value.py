import data_acq

def main():
    county_list = get_population().keys()
    tsa_list = get_region2county().keys()

    # Hypothesis 5 (z test)
    date_param = '06-04~07-15'
    x, y = [], []
    for county in county_list:
        tran_data = get_cases(county, date_range=date_param, number_form='transmission', mv_avg_days=42)
        tran_rate = round(tran_data[0], 1)
        density = get_density(county)
        x.append(density)
        y.append(tran_rate)

    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    print(slope, intercept, r_value, p_value, std_err)

    '''
    with open('density_trans.csv', 'a+', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_MINIMAL)
        for row in csv_data:
            spamwriter.writerow(row)
    '''
    return
    # Hypothesis 4 (z test)
    date_param = '04-21~09-11'
    count = 0
    dic = {}
    for county in county_list:
        x = get_testings(county, date_range=date_param)
        y = get_cases(county, date_range=date_param, number_form='transmission', mv_avg_days=7)
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        if p_value >= 0.05:
            count += 1
        lv = round((1 - abs(p_value)) * 100) // 5 * 5
        if lv not in dic:
            dic[lv] = 0
        dic[lv] += 1
    print(count, len(dic))
    return
    # Hypothesis 3 (T paired test)
    bf_restrict = get_cases('NUECES', date_range='04-01~04-30', number_form='infection')
    af_restrict = get_cases('NUECES', date_range='05-01~05-30', number_form='infection')
    print(len(bf_restrict), len(af_restrict))
    t_value, p_value = stats.ttest_rel(bf_restrict, af_restrict)
    print(t_value, p_value)
    return

    for tsa in tsa_list:
        print('\n {}'.format(tsa))
        # Hypothesis 1 (z-test)
        date_param = '04-12~09-21'
        x = get_hospitalization(tsa=tsa, gain=100, date_range=date_param, accu_format=True)
        y = get_fatality(tsa=tsa, date_range=date_param)
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        print(slope, intercept, r_value, p_value, std_err)
        #print(p_value, p_value<0.05)

        # Hypothesis 2 (z-test)
        date_param = '04-23~09-21'
        x = get_icu(tsa=tsa, gain=100, date_range=date_param, accu_format=True)
        y = get_fatality(tsa=tsa, date_range=date_param)
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        print(slope, intercept, r_value, p_value, std_err)
        #print(p_value, p_value<0.05)

if __name__ == '__main__':
    main()

