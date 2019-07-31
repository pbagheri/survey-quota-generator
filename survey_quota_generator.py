# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 11:52:08 2018

@author: Payam
"""

#import numpy as np
import pandas as pd
import re
import time
from os import path

dir_path = path.dirname(path.abspath(__file__))
#dir_path = path.dirname( __file__ )
print(dir_path)

# Functions #########################
 
def ordinator(x):
# This function takes in a number (0 to 9) and creates an ordinal string based on the number.
    xs = str(x)
    last_dig = int(xs[-1])
    if last_dig == 1:
        ordin = 'st'
    elif last_dig == 2:
        ordin = 'nd'
    elif last_dig == 3:
        ordin = 'rd'
    else:
        ordin = 'th'
    return ordin

# This function creates a Cartesian product of two dataframes
def cross(df1, df2, **kwargs):
    """
    Make a cross join (cartesian product) between two dataframes by using a constant temporary key.
    Also sets a MultiIndex which is the cartesian product of the indices of the input dataframes.
    See: https://github.com/pydata/pandas/issues/5401
    :param df1 dataframe 1
    :param df1 dataframe 2
    :param kwargs keyword arguments that will be passed to pd.merge()
    :return cross join of df1 and df2
    """
    df1['_tmpkey'] = 1
    df2['_tmpkey'] = 1

    res = pd.merge(df1, df2, on='_tmpkey', **kwargs).drop('_tmpkey', axis=1)
    res.index = pd.MultiIndex.from_product((df1.index, df2.index))

    df1.drop('_tmpkey', axis=1, inplace=True)
    df2.drop('_tmpkey', axis=1, inplace=True)

    return res

  
def in_check(intype, text, klist, pat = False):
# This function provides resilience for the input-taking process
# intype: the type of the desired input ('str', 'int', 'float')
# text: the question text as a string
# klist: a list of accept values (for strings) or a list like [min, max] to indicated the range of accepted values
# pat: a key whihc should be put to True if a check against a pattern is desired for the input string
    if intype == 'str': 
        if pat == False:
            inp = input(text)
            while inp not in klist:
                print('Please try again!')
                inp = input(text)            
            else:
                res = inp
                return res
        else:
            inp = input(text)
            while not re.match(klist,inp) :
                print('Please try again!')
                inp = input(text)            
            else:
                res = inp
                return res
            
    elif intype == 'int':
        cond = 1
        c = 0
        while (cond or inp < min(klist) or inp > max(klist)):
            if c == 1:
               print('Please try again!') 
            try:
                inp = int(input(text))
                cond = 0
                c = 1
            except ValueError:
                print('Please try again!')
                c = 2
        else:
            res = inp
            return res
                    
    elif intype == 'float':
        cond = 1
        c = 0
        while (cond or inp < min(klist) or inp > max(klist)):
            if c == 1:
               print('Please try again!') 
            try:
                inp = float(input(text))
                cond = 0
                c = 1
            except ValueError:
                print('Please try again!')
                c = 2
        else:
            res = inp
            return res

        
# Input data #######################################
can_prov = ["Newfoundland and Labrador","Prince Edward Island","Nova Scotia","New Brunswick","Quebec","Ontario","Manitoba","Saskatchewan","Alberta","British Columbia","Yukon","Northwest Territories","Nunavut"]
can_reg = ["Atlantic","Atlantic","Atlantic","Atlantic","Quebec","Ontario","West","West","West","West","West","West","West"]
can_prov_pop = [530128,148649,949501,756780,8326089,13982984,1318128,1150632,4252879,4751612,37492,44469,37082]
french_ratio = [0.006, 0.041, 0.038, 0.316, 0.93, 0.044, 0.038, 0.019, 0.022, 0.016, 0.048, 0.029, 0.014]
regions_canada_en = ['Atlantic', 'Ontario', 'West']

region_can = pd.DataFrame({'province':can_prov,	'region':can_reg, 'population': can_prov_pop, 'french_ratio':french_ratio}) 

us_state = ["Illinois", "Indiana", "Iowa", "Kansas", "Michigan", "Minnesota", "Missouri", "Nebraska", "North Dakota", "Ohio", "South Dakota", "Wisconsin", "Connecticut", "Maine", "Massachusetts", "New Hampshire", "New Jersey", "New York", "Pennsylvania", "Rhode Island", "Vermont", "Alabama", "Arkansas", "Delaware", "District of Columbia", "Florida", "Georgia", "Kentucky", "Louisiana", "Maryland", "Mississippi", "North Carolina", "Oklahoma", "South Carolina", "Tennessee", "Texas", "Virginia", "West Virginia", "Puerto Rico", "Alaska", "Arizona", "California", "Colorado", "Hawaii", "Idaho", "Montana", "Nevada", "New Mexico", "Oregon", "Utah", "Washington", "Wyoming"]
us_reg = ["Midwest", "Midwest", "Midwest", "Midwest", "Midwest", "Midwest", "Midwest", "Midwest", "Midwest", "Midwest", "Midwest", "Midwest", "North-East", "North-East", "North-East", "North-East", "North-East", "North-East", "North-East", "North-East", "North-East", "South", "South", "South", "South", "South", "South", "South", "South", "South", "South", "South", "South", "South", "South", "South", "South", "South", "South", "West", "West", "West", "West", "West", "West", "West", "West", "West", "West", "West", "West", "West"]
us_state_pop = [12802023, 6666818, 3145711, 2913123, 9962311, 5576606, 6113532, 1920076, 755393, 11658609, 869666, 5795483, 3588184, 1335907, 6859819, 1342795, 9005644, 19849399, 12805537, 1059639, 623657, 4874747, 3004279, 961939, 693972, 20984400, 10429379, 4454189, 4684333, 6052177, 2984100, 10273419, 3930864, 5024369, 6715984, 28304596, 8470020, 1815857, 3337177, 739795, 7016270, 39536653, 5607154, 1427538, 1716943, 1050493, 2998039, 2088070, 4142776, 3101833, 7405743, 579315]

region_us = pd.DataFrame({'state':us_state,	'region':us_reg, 'population': us_state_pop})

year = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84]
us_year_pop = [3985407, 3985407, 3985407, 3985407, 3985407, 4085959, 4085959, 4085959, 4085959, 4085959, 4123646, 4123646, 4123646, 4123646, 4123646, 4225999, 4225999, 4225999, 4225999, 4225999, 4476205, 4476205, 4476205, 4476205, 4476205, 4578176, 4578176, 4578176, 4578176, 4578176, 4357271, 4357271, 4357271, 4357271, 4357271, 4154781, 4154781, 4154781, 4154781, 4154781, 3939250, 3939250, 3939250, 3939250, 3939250, 4189524, 4189524, 4189524, 4189524, 4189524, 4367811, 4367811, 4367811, 4367811, 4367811, 4396021, 4396021, 4396021, 4396021, 4396021, 3896607, 3896607, 3896607, 3896607, 3896607, 3364016, 3364016, 3364016, 3364016, 3364016, 2362049, 2362049, 2362049, 2362049, 2362049, 1673579, 1673579, 1673579, 1673579, 1673579, 1173127, 1173127, 1173127, 1173127, 1173127]
can_year_pop = [392096, 392359, 392203, 392871, 391182, 392663, 397671, 400545, 401416, 392618, 382639, 376385, 378146, 373296, 375559, 383259, 398528, 405243, 426149, 453316, 477435, 489793, 493113, 500853, 507870, 513986, 518524, 502232, 489514, 492868, 503133, 507492, 506931, 507541, 505075, 509183, 501541, 488874, 479150, 477387, 476394, 475004, 462550, 462660, 468774, 489398, 485457, 481656, 477395, 481343, 507236, 541036, 556299, 559700, 547047, 552885, 542074, 528672, 521737, 507877, 491548, 484039, 462819, 439886, 421789, 411964, 401360, 390978, 387962, 383459, 327091, 300511, 288116, 272790, 250539, 236443, 218630, 206479, 193485, 179788, 171547, 159939, 148080, 141404, 132453]

census = pd.DataFrame({'age':year, 'population_us':us_year_pop, 'population_can': can_year_pop}) 
####################################################

print('\n','*******************************')

final_result = pd.DataFrame()
# take total and flex as input
total = in_check('int', 'What is the total number of respondents? ', [1,100000])
flex = in_check('float', 'What is the flex value? e.g. enter 1.05 for 5% flex: ', [1,2])

# take male ratio as input:
gen_over = in_check('str','Do you need to override the default male/female ratio 0f 50/50? (y/n): ',['y','n'])
if gen_over == 'y':
    male_ratio = in_check('float', 'What is the ratio of male respondents? (a number between 0 and 1): ', [0,1])
    rats = [male_ratio, (1-male_ratio)]
    gens = ['male', 'female']
    gender = pd.DataFrame({'gender_ratio': rats, 'gender': gens})
elif gen_over == 'n':
    male_ratio = 0.5
    rats = [male_ratio, (1-male_ratio)]
    gens = ['male', 'female']
    gender = pd.DataFrame({'gender_ratio': rats, 'gender': gens})

   
print('\n','*******************************')

country = in_check('str','What is the country of the survey? type can or us: ', ['can', 'us'])

if country == 'can':
    num_age_brackets = in_check('int','How many age brackets are there in this survey? ',[1,100])
    age = pd.DataFrame()
    for c in range(num_age_brackets):
        upper = 1000
        lower = 1000
        warn = 0
        while upper <= lower:
            if warn == 1:
                print('Please try again')
            agelims = in_check('str', 'Enter the ' + str(c+1)+ ordinator(c+1) + ' age bracket: LowerLimit,UpperLimit ','\d+[-|\s|,]\d+', pat = True) 
            sep = re.search('[-|\s|,]',agelims).group(0)
            comma = agelims.find(sep)
            lower = int(agelims[:comma].strip())
            upper = int(agelims[comma + 1:].strip()) 
            pop = census['population_can'][lower : upper + 1].sum()
            age = age.append(pd.Series([lower, upper, pop]), ignore_index=True)
            warn = 1
    age.columns = ['lower', 'upper', 'pop']
    age['age_ratio'] = age['pop']/age['pop'].sum()
    
    lang = in_check('int','What are the languages of the survey? (Enter 1 for English, 2 for French, and 3 for French & English): ',[1,3])
    if lang == 1:
        region = pd.DataFrame()        
        for i in regions_canada_en:
            ans = in_check('str','Is ' + i + ' included in the survey regions? (y/n) ', ['y','n'])
            if (ans == 'y' or ans == 'Y' or ans == 'yes' or ans == 'Yes'):
                reg = i
                reg_pop = region_can['population'][region_can.region == reg].sum()
                region = region.append(pd.Series([reg, reg_pop]), ignore_index=True)
        region.columns = ['reg', 'population']
        region['region_ratio'] = region['population']/region['population'].sum()
        print('\n','*******************************')
        for c in range(len(region)):
            print('Quota for ' + region['reg'].iloc[c] + ': ', int(round(region['region_ratio'].iloc[c]*total*flex)))
            final_result = final_result.append(pd.Series(['Quota for ' + region['reg'].iloc[c] + ': ', int(round(region['region_ratio'].iloc[c]*total*flex))]), ignore_index=True)
        langs = ['English']
        rats = [1]
        language = pd.DataFrame({'lang':langs, 'language_ratio':rats})    
        
        
    if lang == 2:
        print('\n','*******************************')
        print('Quota for Quebec: ', int(round(total*flex)))
        final_result = final_result.append(pd.Series(['Quota for Quebec: ', int(round(total*flex))]), ignore_index=True)
        langs = ['French']
        rats = [1]
        language = pd.DataFrame({'lang':langs, 'language_ratio':rats})
   
    if lang == 3:
        region = pd.DataFrame()
        lang_over = in_check('str', 'Do you need to override the census French/English speaker ratio? (y/n): ', ['y','n'])
        if lang_over == 'y':
            fr_ratio = in_check('float', 'What is the ratio of French speaking respondents? (a number between 0 and 1): ', [0,1])
            for i in regions_canada_en:
                ans_en = in_check('str', 'Is ' + i + ' included in the English survey regions? (y/n) ', ['y','n'])
                if ans_en == 'y':
                    reg_en = i
                    reg_pop_en = sum([x*(1-fr_ratio) for x in region_can['population'][region_can.region == reg_en]])
                    region = region.append(pd.Series([reg_en, reg_pop_en]), ignore_index=True)
            reg_pop_fr = float(region_can['population'][region_can.region == 'Quebec']*fr_ratio)
            region = region.append(pd.Series(['Quebec', reg_pop_fr]), ignore_index=True)
            region.columns = ['reg', 'population']
            region['region_ratio'] = region['population']/region['population'].sum()
            region['region_ratio'][region.reg != 'Quebec'] = (1-fr_ratio)*region['region_ratio'][region.reg != 'Quebec']/region['region_ratio'][region.reg != 'Quebec'].sum()
            region['region_ratio'][region.reg == 'Quebec'] = fr_ratio
            print('\n','*******************************')
            print('Quota for Quebec/French: ', int(round(fr_ratio*total*flex)))
            final_result = final_result.append(pd.Series(['Quota for Quebec/French: ', int(round(fr_ratio*total*flex))]), ignore_index=True)
            print('Quota for English: ', int(round((1-fr_ratio)*total*flex)))
            final_result = final_result.append(pd.Series(['Quota for English: ', int(round((1-fr_ratio)*total*flex))]), ignore_index=True)
            sum_en_ratios = region['region_ratio'][region.reg != 'Quebec'].sum()
            for c in range(len(region)):
                if region['reg'].iloc[c] != 'Quebec':
                    print('Quota for ' + region['reg'].iloc[c] + ': ', int(round((1-fr_ratio)*region['region_ratio'].iloc[c]*total*flex/sum_en_ratios)))                
                    final_result = final_result.append(pd.Series(['Quota for ' + region['reg'].iloc[c] + ': ', int(round((1-fr_ratio)*region['region_ratio'].iloc[c]*total*flex/sum_en_ratios))]), ignore_index=True)
            
            rats = [float(fr_ratio), float(1-fr_ratio)]
            langs = ['French', 'English']
            language = pd.DataFrame({'lang':langs, 'language_ratio':rats})
            
        elif lang_over == 'n':
            for i in regions_canada_en:
                ans_en = in_check('str', 'Is ' + i + ' included in the English survey regions? (y/n) ', ['y','n'])
                if ans_en == 'y':
                    reg_en = i
                    reg_pop = region_can['population'][region_can.region == reg_en].sum()
                    region = region.append(pd.Series([reg_en, reg_pop]), ignore_index=True)
            reg_pop_fr = float(region_can['population'][region_can.region == 'Quebec'])
            region = region.append(pd.Series(['Quebec', reg_pop_fr]), ignore_index=True)
            region.columns = ['reg', 'population']
            region['region_ratio'] = region['population']/region['population'].sum()
            print('\n','*******************************')
            print('Quota for Quebec/French: ', int(round(region['region_ratio'][region.reg == 'Quebec']*total*flex)))
            final_result = final_result.append(pd.Series(['Quota for Quebec/French: ', int(round(region['region_ratio'][region.reg == 'Quebec']*total*flex))]), ignore_index=True)
            print('Quota for English: ', int(round((1-region['region_ratio'][region.reg == 'Quebec'])*total*flex)))
            final_result = final_result.append(pd.Series(['Quota for English: ', int(round((1-region['region_ratio'][region.reg == 'Quebec'])*total*flex))]), ignore_index=True)
            for r in region.reg:
                if r != 'Quebec': 
                    print('Quota for ' + r + ': ', int(round(region['region_ratio'][region.reg == r]*total*flex)))
                    final_result = final_result.append(pd.Series(['Quota for ' + r + ': ', int(round(region['region_ratio'][region.reg == r]*total*flex))]), ignore_index=True)
            fr_ratio = region.region_ratio[region.reg == 'Quebec']
            rats = [float(fr_ratio), float(1-fr_ratio)]
            langs = ['French', 'English']
            language = pd.DataFrame({'lang':langs, 'language_ratio':rats})
            

elif country == 'us':
    num_age_brackets = in_check('int','How many age brackets are there in this survey? ',[1,100])
    #age_tot = 0
    age = pd.DataFrame()
    for c in range(num_age_brackets):
        upper = 1000
        lower = 1000
        warn = 0
        while upper <= lower:
            if warn == 1:
                print('Please try again')
            agelims = in_check('str', 'Enter the ' + str(c+1)+ ordinator(c+1) + ' age bracket: LowerLimit,UpperLimit ','\d+[-|\s|,]\d+', pat = True) 
            sep = re.search('[-|\s|,]',agelims).group(0)
            comma = agelims.find(sep)
            lower = int(agelims[:comma].strip())
            upper = int(agelims[comma + 1:].strip()) 
            pop = census['population_us'][lower : upper + 1].sum()
            age = age.append(pd.Series([lower, upper, pop]), ignore_index=True)
            warn = 1
    age.columns = ['lower', 'upper', 'pop']
    age['age_ratio'] = age['pop']/(age['pop'].sum())
    
    region = pd.DataFrame()
    for i in region_us.region.unique():
        ans = in_check('str', 'Is ' + i + ' included in the survey regions? (y/n) ', ['y','n'])
        if ans == 'y':
            reg = i        
            reg_pop = region_us['population'][region_us.region == reg].sum()
            region = region.append(pd.Series([reg, reg_pop]), ignore_index=True)

    region.columns = ['reg', 'population']
    region['region_ratio'] = region['population']/region['population'].sum()
    print('\n','*******************************')
    for r in region.reg:
        print('Quota for ' + r + ': ', int(round(region['region_ratio'][region.reg == r]*total*flex)))
        final_result = final_result.append(pd.Series(['Quota for ' + r + ': ', int(round(region['region_ratio'][region.reg == r]*total*flex))]), ignore_index=True)
    langs = ['English']
    rats = [1]
    language = pd.DataFrame({'lang':langs, 'language_ratio':rats})
    
print('\n','*******************************')
for c in range(num_age_brackets):
    print('Quota for age-range "' + str(age['lower'].iloc[c]) + ' to ' + str(age['upper'].iloc[c]) + '": ', int(round(age['age_ratio'].iloc[c]*total*flex)))
    final_result = final_result.append(pd.Series(['Quota for age-range "' + str(age['lower'].iloc[c]) + ' to ' + str(age['upper'].iloc[c]) + '": ', int(round(age['age_ratio'].iloc[c]*total*flex))]), ignore_index=True)
    
print('\n','*******************************')    
print('Quota for males: ', int(round(male_ratio*total*flex)))
final_result = final_result.append(pd.Series(['Quota for males: ', int(round(male_ratio*total*flex))]), ignore_index=True)
print('Quota for females: ', int(round((1-male_ratio)*total*flex)))  
final_result = final_result.append(pd.Series(['Quota for females: ', int(round((1-male_ratio)*total*flex))]), ignore_index=True)

print('\n','*******************************')

region['id'] = region['reg']
age['id'] = age.apply(lambda x: str(int(x.lower)) + '-' + str(int(x.upper)), axis=1)
language['id'] = language['lang']
gender['id'] = gender['gender']

df_dic = {'region': region, 'age':age, 'language': language, 'gender': gender}
nes_dic = {1: 'region', 2:'age', 3: 'language', 4: 'gender'}

nest = in_check('str', 'Do you need to nest a set of variables? (y/n): ', ['y', 'n'])
while nest == 'y':
    num = in_check('int','How many variable would you like to nest under each other? ', [1,4])
    nest_list = list()
    name_ratios = list()
    for i in range(num):
        nes_n = in_check('int', 'What is the ' + str(i+1) + ordinator(i+1) + ' variable? (region:1, age:2, language:3, gender:4): ', [1,4])
        nes = nes_dic[nes_n]
        nest_list.append(nes)
        ratio = nes + '_ratio'
        name_ratios.append(ratio)
    comb_ratio = ''
    df_cross = pd.DataFrame([1])
    df_ratios = pd.DataFrame([1])
    for j in range(num):    
        comb_ratio = name_ratios[j] + '_' + comb_ratio# + '_ratio'
        df_temp = df_dic[nest_list[j]].copy()
        df_temp.rename(columns={'id':'id' + str(j)}, inplace=True)
        df_cross = cross(df_temp,df_cross)
        df_cross.reset_index(drop=True, inplace=True)
    
    df_cross['nest_ratio'] = 1
    for n in name_ratios:
        df_cross['nest_ratio'] = df_cross['nest_ratio']*df_cross[n]
    df_cross.reset_index(drop=True, inplace=True)
     
    print('\n','*******************************')
    df_cross['fin_id'] = ''
    for i in range(num):
        idi = 'id' + str(i)
        if i == 0:
            df_cross['fin_id'] = df_cross[idi] + ', '
        elif (i > 0 and i < num-1):
            df_cross['fin_id'] = df_cross['fin_id'] + df_cross[idi] + ', '
        else:
            df_cross['fin_id'] = df_cross['fin_id'] + df_cross[idi]
            
    for c in df_cross.index:
        print(df_cross['fin_id'].iloc[c] + ': ', int(round(df_cross['nest_ratio'].iloc[c]*total*flex)))
        final_result = final_result.append(pd.Series([df_cross['fin_id'].iloc[c] + ': ', int(round(df_cross['nest_ratio'].iloc[c]*total*flex))]), ignore_index=True)
    print('\n','*******************************')
    nest = in_check('str', 'Do you need to nest another set of variables? (y/n): ', ['y','n'])   

final_result.to_csv(dir_path + '\\quotas.csv', index=False, header=False)

#time.sleep(500)
print('\n') 
ans = input('Hit enter to exit: ')

 
