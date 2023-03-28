import numpy as np
import random
# from Person import Person
# ages = {'0-4': 258, '5-9': 357, '10-14': 448, '15-19': 383, '20-24': 237,
#         '25-29': 319, '30-34': 315, '35-39': 340, '40-44': 409, '45-49': 425,
#         '50-54': 482, '55-59': 451, '60-64': 365, '65-69': 345, '70-74': 351,
#         '75-79': 252, '80-84': 210, '85+': 205}
# genders = {'Female': 3165.0, 'Male': 2989.0}
#
# ethnicities = {'Asian': 553.0, 'Black': 128.0, 'Mixed': 317.0,
#                'White': 4952.0, 'Other': 204.0}
#
# religions = {'none': 2547.0, 'Christian': 2611.0, 'Buddhist': 41.0,
#              'Hindu': 107.0, 'Jewish': 68.0, 'Muslim': 261.0, 'Sikh': 20.0,
#              'other': 36.0, 'unknown': 464.0}
#
# # p = Person(1, 24, 'Male', 'White', 'Muslim')
# # q = Person(2, 20, 'Female', 'Asian', 'Sikh')
# # r = Person(3, 55, 'Male', 'Asian', 'Hindu')
#
#
# print(len(ages) * len(genders) * len(ethnicities) * len(religions))
#
#
# maritaldf = pd.read_csv(os.path.join(path, 'NOMIS', 'Census_2011_LSOA', 'individual', 'marital_status.csv'),
#                     usecols= lambda x: x not in ['date', 'geography', 'Rural Urban'])
# maritaldf.columns = rename_columns(maritaldf, 'Marital Status')
# maritaldf.columns = ['geography code', 'All', 'Single', 'Married', 'civil partnership', 'Separated', 'Divorced', 'Widowed']
# maritaldf = maritaldf[maritaldf['geography code']=='E01028580']
# ms_samples =  get_weighted_samples(maritaldf).tolist()
# persondf['maritalstatus'] = persondf['age'].apply(lambda x: ms_samples.pop(0) if x > 18 else 'single')
#
# healthdf = pd.read_csv(os.path.join(path, 'NOMIS', 'Census_2011_LSOA', 'individual', 'general_health.csv'),
#                     usecols= lambda x: x not in ['date', 'geography', 'Rural Urban'])
# healthdf.columns = rename_columns(healthdf, 'General Health')
# healthdf = healthdf[healthdf['geography code']=='E01028580']
# persondf['health'] = get_weighted_samples(healthdf, 'health')
#
# # qualificationdf = pd.read_csv(os.path.join(path, 'NOMIS', 'Census_2011_LSOA', 'individual', 'highest_qualification.csv'),
# #                     usecols= lambda x: x not in ['date', 'geography', 'Rural Urban'])
# # qualificationdf.columns = rename_columns(qualificationdf, 'Qualification')
# # qualificationdf = qualificationdf[qualificationdf['geography code']=='E01028580']
# # persondf['qualification'] = get_weighted_samples(qualificationdf, total, 'qualification')
# #
# # industrydf = pd.read_csv(os.path.join(path, 'NOMIS', 'Census_2011_LSOA', 'individual', 'industry.csv'),
# #                     usecols= lambda x: x not in ['date', 'geography', 'Rural Urban'])
# # industrydf.columns = rename_columns(industrydf, 'Industry')
# # industrydf = industrydf[industrydf['geography code']=='E01028580']
# # persondf['industry'] = get_weighted_samples(industrydf, total, 'industry')
# # economicdf = pd.read_csv(os.path.join(path, 'NOMIS', 'Census_2011_LSOA', 'individual', 'economic_activity.csv'),
# #                     usecols= lambda x: x not in ['date', 'geography', 'Rural Urban'])
# # economicdf.columns = rename_columns(economicdf.columns, level=1)
# # economicdf = economicdf[economicdf['geography code']=='E01028580']
# #
# # nssecdf = pd.read_csv(os.path.join(path, 'NOMIS', 'Census_2011_LSOA', 'individual', 'NS_SEC.csv'),
# #                     usecols= lambda x: x not in ['date', 'geography', 'Rural Urban'])
# # nssecdf.columns = rename_columns(nssecdf.columns)
# # nssecdf = nssecdf[nssecdf['geography code']=='E01028580']
#
# # def remove_columns(df):
# #     result = []
# #     groups = df.columns[2:]
# #     for group in groups:
# #         if group.count(':') < 3:
# #             result.append(group)
# #     return result
# #
# # def rename_columns(df, table):
# #         groups = df.columns
# #         groups = [sub.replace(table + ":", '').strip().split(';')[0] for sub in groups]
# #         return groups
#
# def getkey(dictionary, val):
#     for key, value in dictionary.items():
#         if value == val:
#             return key
#     return None
#
# def print_df(df, header): #level=1 has main category; #level=2 has a subcategory
#     for index, row in df.iterrows():
#         for col in df.columns:
#             print(getkey(header, col), row[col])
#
# def get_header(df, level=1): #level=1 has main category; #level=2 has a subcategory
#     header = {}
#     if level==1:
#         value = 0
#         for index, column in enumerate(df.columns):
#             if index == 0:  # geography code
#                 header[column] = column
#             elif index == 1:
#                 header[column] = 'total'
#             else:
#                 header[column] = str(value)
#                 value += 1
#     # elif level==2:
#     return header
#
#
# list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
# for i in range(85):
#         print("'" + str(i) + 'M'+ "'")

