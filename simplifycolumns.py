import random
import numpy as np
import geopandas as gpd
import pandas as pd
import os

path = os.path.join(os.path.dirname(os.getcwd()))

# Read cross tables
# sex_by_age = pd.read_csv(os.path.join(path, 'NOMIS', 'Census_2011_MSOA', 'crosstables', 'sex_by_age.csv'))
# # sex_by_age = sex_by_age[sex_by_age['geography code'] == 'E02005949']
# sex_by_age = sex_by_age.drop(columns=[col for col in sex_by_age.columns if 'A' in col])
#
# sex_by_age_5yrs = pd.DataFrame()
# sex_by_age_5yrs['geography code'] = sex_by_age['geography code']
# sex_by_age_5yrs['total'] = sex_by_age['total']
#
#
# sex_by_age_5yrs['0-4 M'] = sex_by_age[['0M', '1M', '2M', '3M', '4M']].sum(axis=1)
# sex_by_age_5yrs['5-7 M'] = sex_by_age[['5M', '6M', '7M']].sum(axis=1)
# sex_by_age_5yrs['8-9 M'] = sex_by_age[['8M', '9M']].sum(axis=1)
# sex_by_age_5yrs['10-14 M'] = sex_by_age[['10M', '11M', '12M', '13M', '14M']].sum(axis=1)
# sex_by_age_5yrs['15 M'] = sex_by_age[['15M']].sum(axis=1)
# sex_by_age_5yrs['16-17 M'] = sex_by_age[['16M', '17M']].sum(axis=1)
# sex_by_age_5yrs['18-19 M'] = sex_by_age[['18M', '19M']].sum(axis=1)
# sex_by_age_5yrs['20-24 M'] = sex_by_age[['20M', '21M', '22M', '23M', '24M']].sum(axis=1)
# sex_by_age_5yrs['25-29 M'] = sex_by_age[['25M', '26M', '27M', '28M', '29M']].sum(axis=1)
# sex_by_age_5yrs['30-34 M'] = sex_by_age[['30M', '31M', '32M', '33M', '34M']].sum(axis=1)
# sex_by_age_5yrs['35-39 M'] = sex_by_age[['35M', '36M', '37M', '38M', '39M']].sum(axis=1)
# sex_by_age_5yrs['40-44 M'] = sex_by_age[['40M', '41M', '42M', '43M', '44M']].sum(axis=1)
# sex_by_age_5yrs['45-49 M'] = sex_by_age[['45M', '46M', '47M', '48M', '49M']].sum(axis=1)
# sex_by_age_5yrs['50-54 M'] = sex_by_age[['50M', '51M', '52M', '53M', '54M']].sum(axis=1)
# sex_by_age_5yrs['55-59 M'] = sex_by_age[['55M', '56M', '57M', '58M', '59M']].sum(axis=1)
# sex_by_age_5yrs['60-64 M'] = sex_by_age[['60M', '61M', '62M', '63M', '64M']].sum(axis=1)
# sex_by_age_5yrs['65-69 M'] = sex_by_age[['65M', '66M', '67M', '68M', '69M']].sum(axis=1)
# sex_by_age_5yrs['70-74 M'] = sex_by_age[['70M', '71M', '72M', '73M', '74M']].sum(axis=1)
# sex_by_age_5yrs['75-79 M'] = sex_by_age[['75M', '76M', '77M', '78M', '79M']].sum(axis=1)
# sex_by_age_5yrs['80-84 M'] = sex_by_age[['80M', '81M', '82M', '83M', '84M']].sum(axis=1)
# sex_by_age_5yrs['85+ M'] = sex_by_age[['85M']].sum(axis=1)
#
# sex_by_age_5yrs['0-4 F'] = sex_by_age[['0F', '1F', '2F', '3F', '4F']].sum(axis=1)
# sex_by_age_5yrs['5-7 F'] = sex_by_age[['5F', '6F', '7F']].sum(axis=1)
# sex_by_age_5yrs['8-9 F'] = sex_by_age[['8F', '9F']].sum(axis=1)
# sex_by_age_5yrs['10-14 F'] = sex_by_age[['10F', '11F', '12F', '13F', '14F']].sum(axis=1)
# sex_by_age_5yrs['15 F'] = sex_by_age[['15F']].sum(axis=1)
# sex_by_age_5yrs['16-17 F'] = sex_by_age[['16F', '17F']].sum(axis=1)
# sex_by_age_5yrs['18-19 F'] = sex_by_age[['18F', '19F']].sum(axis=1)
# sex_by_age_5yrs['20-24 F'] = sex_by_age[['20F', '21F', '22F', '23F', '24F']].sum(axis=1)
# sex_by_age_5yrs['25-29 F'] = sex_by_age[['25F', '26F', '27F', '28F', '29F']].sum(axis=1)
# sex_by_age_5yrs['30-34 F'] = sex_by_age[['30F', '31F', '32F', '33F', '34F']].sum(axis=1)
# sex_by_age_5yrs['35-39 F'] = sex_by_age[['35F', '36F', '37F', '38F', '39F']].sum(axis=1)
# sex_by_age_5yrs['40-44 F'] = sex_by_age[['40F', '41F', '42F', '43F', '44F']].sum(axis=1)
# sex_by_age_5yrs['45-49 F'] = sex_by_age[['45F', '46F', '47F', '48F', '49F']].sum(axis=1)
# sex_by_age_5yrs['50-54 F'] = sex_by_age[['50F', '51F', '52F', '53F', '54F']].sum(axis=1)
# sex_by_age_5yrs['55-59 F'] = sex_by_age[['55F', '56F', '57F', '58F', '59F']].sum(axis=1)
# sex_by_age_5yrs['60-64 F'] = sex_by_age[['60F', '61F', '62F', '63F', '64F']].sum(axis=1)
# sex_by_age_5yrs['65-69 F'] = sex_by_age[['65F', '66F', '67F', '68F', '69F']].sum(axis=1)
# sex_by_age_5yrs['70-74 F'] = sex_by_age[['70F', '71F', '72F', '73F', '74F']].sum(axis=1)
# sex_by_age_5yrs['75-79 F'] = sex_by_age[['75F', '76F', '77F', '78F', '79F']].sum(axis=1)
# sex_by_age_5yrs['80-84 F'] = sex_by_age[['80F', '81F', '82F', '83F', '84F']].sum(axis=1)
# sex_by_age_5yrs['85+ F'] = sex_by_age[['85F']].sum(axis=1)
# sex_by_age_5yrs.to_csv(os.path.join(path, 'NOMIS', 'Census_2011_MSOA', 'crosstables', 'sex_by_age_5yrs.csv'), index=False)

# ethnic_by_sex_by_age = pd.read_csv(os.path.join(path, 'NOMIS', 'Census_2011_MSOA', 'crosstables', 'ethnic_by_sex_by_age.csv'))
# ethnic_by_sex_by_age = ethnic_by_sex_by_age.rename(columns = {'Sex: All persons; Age: All categories: Age; Ethnic Group: All categories: Ethnic group; measures: Value':'total'})
# ethnic_by_sex_by_age = ethnic_by_sex_by_age.drop(columns=[col for col in ethnic_by_sex_by_age.columns if 'All' in col])
# ethnic_by_sex_by_age = ethnic_by_sex_by_age.drop(columns=[col for col in ethnic_by_sex_by_age.columns if 'Total' in col])
# ethnic_by_sex_by_age = ethnic_by_sex_by_age.drop(columns=['date', 'geography'])
#
# columns = list(ethnic_by_sex_by_age.columns)[2:]
# updated_columns = ['geography code', 'total']
# for column in columns:
#     genders = column.split(";")[0].replace('Sex: Females', 'F').replace('Sex: Males', 'M')
#     ages = column.split(";")[1].replace(' Age: Age ', '').replace(' and over', '+'). replace(' to ', '-')
#     ethnic = column.split(";")[2].replace(' Ethnic Group: ', '')
#     ethnic = ethnic.replace('White: English/Welsh/Scottish/Northern Irish/British', 'W0')
#     ethnic = ethnic.replace('White: Irish', 'W1')
#     ethnic = ethnic.replace('White: Gypsy or Irish Traveller', 'W2')
#     ethnic = ethnic.replace('White: Other White', 'W3')
#     ethnic = ethnic.replace('Mixed/multiple ethnic group: White and Black Caribbean', 'M0')
#     ethnic = ethnic.replace('Mixed/multiple ethnic group: White and Black African', 'M1')
#     ethnic = ethnic.replace('Mixed/multiple ethnic group: White and Asian', 'M2')
#     ethnic = ethnic.replace('Mixed/multiple ethnic group: Other Mixed', 'M3')
#     ethnic = ethnic.replace('Asian/Asian British: Indian', 'A0')
#     ethnic = ethnic.replace('Asian/Asian British: Pakistani', 'A1')
#     ethnic = ethnic.replace('Asian/Asian British: Bangladeshi', 'A2')
#     ethnic = ethnic.replace('Asian/Asian British: Chinese', 'A3')
#     ethnic = ethnic.replace('Asian/Asian British: Other Asian', 'A4')
#     ethnic = ethnic.replace('Black/African/Caribbean/Black British: African', 'B0')
#     ethnic = ethnic.replace('Black/African/Caribbean/Black British: Caribbean', 'B1')
#     ethnic = ethnic.replace('Black/African/Caribbean/Black British: Other Black', 'B2')
#     ethnic = ethnic.replace('Other ethnic group: Arab', 'O0')
#     ethnic = ethnic.replace('Other ethnic group: Any other ethnic group', 'O1')
#     updated_columns.append(genders + ' ' +  ages +  ' ' + ethnic)
#
# ethnic_by_sex_by_age.columns = updated_columns
# ethnic_by_sex_by_age.to_csv(os.path.join(path, 'NOMIS', 'Census_2011_MSOA', 'crosstables', 'ethnic_by_sex_by_age2.csv'), index=False)

# religion_by_sex_by_age = pd.read_csv(os.path.join(path, 'NOMIS', 'Census_2011_MSOA', 'crosstables', 'religion_by_sex_by_age.csv'))
# religion_by_sex_by_age = religion_by_sex_by_age.rename(columns = {'Sex: All persons; Age: All categories: Age; Religion: All categories: Religion; measures: Value':'total'})
# religion_by_sex_by_age = religion_by_sex_by_age.drop(columns=[col for col in religion_by_sex_by_age.columns if 'All' in col])
# religion_by_sex_by_age = religion_by_sex_by_age.drop(columns=[col for col in religion_by_sex_by_age.columns if 'Total' in col])
# religion_by_sex_by_age = religion_by_sex_by_age.drop(columns=['date', 'geography'])
# columns = list(religion_by_sex_by_age.columns)[2:]
# updated_columns = ['geography code', 'total']
# for column in columns:
#     genders = column.split(";")[0].replace('Sex: Females', 'F').replace('Sex: Males', 'M')
#     ages = column.split(";")[1].replace(' Age: Age ', '').replace(' and over', '+'). replace(' to ', '-')
#     religion = column.split(";")[2]
#     religion = religion.replace(' Religion: Christian', 'C')
#     religion = religion.replace(' Religion: Buddhist', 'B')
#     religion = religion.replace(' Religion: Hindu', 'H')
#     religion = religion.replace(' Religion: Jewish', 'J')
#     religion = religion.replace(' Religion: Muslim', 'M')
#     religion = religion.replace(' Religion: Sikh', 'S')
#     religion = religion.replace(' Religion: Other religion', 'OR')
#     religion = religion.replace(' Religion: No religion', 'NR')
#     religion = religion.replace(' Religion: Religion not stated', 'NS')
#     updated_columns.append(genders + ' ' +  ages +  ' ' + religion)
#
# religion_by_sex_by_age.columns = updated_columns
# religion_by_sex_by_age.to_csv(os.path.join(path, 'NOMIS', 'Census_2011_MSOA', 'crosstables', 'religion_by_sex_by_age2.csv'), index=False)


# marital_by_sex_by_age = pd.read_csv(os.path.join(path, 'NOMIS', 'Census_2011_MSOA', 'crosstables', 'marital_by_sex_by_age.csv'))
# marital_by_sex_by_age = marital_by_sex_by_age.rename(columns = {'Sex: All persons; Age: All categories: Age; Marital Status: All categories: Marital and civil partnership status; measures: Value':'total'})
# marital_by_sex_by_age = marital_by_sex_by_age.drop(columns=[col for col in marital_by_sex_by_age.columns if 'All' in col])
# marital_by_sex_by_age = marital_by_sex_by_age.drop(columns=['date', 'geography'])
#
# columns = list(marital_by_sex_by_age.columns)[2:]
# updated_columns = ['geography code', 'total']
# for column in columns:
#     genders = column.split(";")[0].replace('Sex: Females', 'F').replace('Sex: Males', 'M')
#     ages = column.split(";")[1].replace(' Age: Age ', '').replace(' and over', '+'). replace(' to ', '-').replace(' and under', '*')
#     status = column.split(";")[2].replace(' Marital Status: ', '')
#     status = status.replace('Single (never married or never registered a same-sex civil partnership)','Single')
#     status = status.replace('In a registered same-sex civil partnership', 'Partner')
#     status = status.replace('Separated (but still legally married or still legally in a same-sex civil partnership)', 'Seperated')
#     status = status.replace('Divorced or formerly in a same-sex civil partnership which is now legally dissolved', 'Divorced')
#     status = status.replace('Widowed or surviving partner from a same-sex civil partnership', 'Widowed')
#     updated_columns.append(genders + ' ' +  ages +  ' ' + status)
#
# marital_by_sex_by_age.columns = updated_columns
# marital_by_sex_by_age.to_csv(os.path.join(path, 'NOMIS', 'Census_2011_MSOA', 'crosstables', 'marital_by_sex_by_age2.csv'), index=False)