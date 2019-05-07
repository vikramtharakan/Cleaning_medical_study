#!/usr/bin/env python
# coding: utf-8

# ## Gather

# In[3]:


import pandas as pd


# In[4]:


patients = pd.read_csv('patients.csv')
treatments = pd.read_csv('treatments.csv')
adverse_reactions = pd.read_csv('adverse_reactions.csv')


# ## Assess

# In[5]:


patients


# In[6]:


treatments


# In[7]:


adverse_reactions


# In[8]:


patients.info()


# In[9]:


treatments.info()


# In[10]:


adverse_reactions.info()


# In[11]:


all_columns = pd.Series(list(patients) + list(treatments) + list(adverse_reactions))
all_columns[all_columns.duplicated()]


# In[12]:


list(patients)


# In[13]:


patients[patients['address'].isnull()]


# In[14]:


patients.describe()


# In[15]:


treatments.describe()


# In[16]:


patients.sample(5)


# In[17]:


patients.surname.value_counts()


# In[18]:


patients.address.value_counts()


# In[19]:


patients[patients.address.duplicated()]


# In[20]:


patients.weight.sort_values()


# In[21]:


weight_lbs = patients[patients.surname == 'Zaitseva'].weight * 2.20462
height_in = patients[patients.surname == 'Zaitseva'].height
bmi_check = 703 * weight_lbs / (height_in * height_in)
bmi_check


# In[22]:


patients[patients.surname == 'Zaitseva'].bmi


# In[23]:


sum(treatments.auralin.isnull())


# In[24]:


sum(treatments.novodra.isnull())


# #### Quality
# ##### `patients` table
# - Zip code is a float not a string
# - Zip code has four digits sometimes
# - Tim Neudorf height is 27 in instead of 72 in
# - Full state names sometimes, abbreviations other times
# - Dsvid Gustafsson
# - Missing demographic information (address - contact columns) ***(can't clean)***
# - Erroneous datatypes (assigned sex, state, zip_code, and birthdate columns)
# - Multiple phone number formats
# - Default John Doe data
# - Multiple records for Jakobsen, Gersten, Taylor
# - kgs instead of lbs for Zaitseva weight
# 
# ##### `treatments` table
# - Missing HbA1c changes
# - The letter 'u' in starting and ending doses for Auralin and Novodra
# - Lowercase given names and surnames
# - Missing records (280 instead of 350)
# - Erroneous datatypes (auralin and novodra columns)
# - Inaccurate HbA1c changes (leading 4s mistaken as 9s)
# - Nulls represented as dashes (-) in auralin and novodra columns
# 
# ##### `adverse_reactions` table
# - Lowercase given names and surnames

# #### Tidiness
# - Contact column in `patients` table should be split into phone number and email
# - Three variables in two columns in `treatments` table (treatment, start dose and end dose)
# - Adverse reaction should be part of the `treatments` table
# - Given name and surname columns in `patients` table duplicated in `treatments` and `adverse_reactions` tables

# ## Clean

# In[25]:


patients_clean = patients.copy()
treatments_clean = treatments.copy()
adverse_reactions_clean = adverse_reactions.copy()


# ### Missing Data

# #### `treatments`: Missing records (280 instead of 350)

# ##### Define
# *Fill in missing `treatments` values from `treatments_cut.csv` by joining tables together. 
# 
# Note: the missing `treatments` records are stored in a file named `treatments_cut.csv`, which you can see in this Jupyter Notebook's dashboard (click the **jupyter** logo in the top lefthand corner of this Notebook). Hint: [documentation page](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.concat.html) for the function used in the solution.*

# ##### Code

# In[26]:


# Your cleaning code here
cut_df = pd.read_csv('treatments_cut.csv')
treatments_clean = pd.concat([treatments_clean, cut_df], ignore_index=True)


# ##### Test

# In[27]:


# Your testing code here
print('size of old treatments dataframe: ' + str(treatments.shape[0]))
print('size of new treatments_clean dataframe: ' + str(treatments_clean.shape[0]))


# #### `treatments`: Missing HbA1c changes and Inaccurate HbA1c changes (leading 4s mistaken as 9s)
# *Note: the "Inaccurate HbA1c changes (leading 4s mistaken as 9s)" observation, which is an accuracy issue and not a completeness issue, is included in this header because it is also fixed by the cleaning operation that fixes the missing "Missing HbA1c changes" observation. Multiple observations in one **Define, Code, and Test** header occurs multiple times in this notebook.*

# ##### Define
# * Check if `hba1c_start` - `hba1c_end` is positive 
# * Check that `hba1c_start` - `hba1c_end` = hba1c_change. If not, change `hba1c_change` value to this difference

# ##### Code

# In[28]:


treatments_clean.head()


# In[29]:


# Your cleaning code here
for i in range(treatments_clean.shape[0]):
    if (treatments_clean['hba1c_start'][i] - treatments_clean['hba1c_end'][i] != treatments_clean['hba1c_change'][i]):
        treatments_clean['hba1c_change'][i] = treatments_clean['hba1c_start'][i] - treatments_clean['hba1c_end'][i]
        


# In[30]:


treatments_clean.head()


# ##### Test

# In[31]:


# Your testing code here
print('Number of NaN\'s in `hba1c_change`: '+ str(treatments_clean['hba1c_change'].isnull().sum()))
                                                


# ### Tidiness

# #### Contact column in `patients` table contains two variables: phone number and email

# ##### Define
# *Your definition here. Hint 1: use regular expressions with pandas' [`str.extract` method](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.str.extract.html). Here is an amazing [regex tutorial](https://regexone.com/). Hint 2: [various phone number regex patterns](https://stackoverflow.com/questions/16699007/regular-expression-to-match-standard-10-digit-phone-number). Hint 3: [email address regex pattern](http://emailregex.com/), which you might need to modify to distinguish the email from the phone number.*

# ##### Code

# In[32]:


patients_clean.head(8)
# Your cleaning code here


# In[33]:


# Creates a datafram 'phone_num' that has the parsed segments of the phone number
# from the contact information
phone_num = patients_clean['contact'].str.extract('\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*', expand = True)
#phone_num


# In[34]:


# Creates a list of the phone numbers. Ignores '+1' as all numbers are from the US 
phone_list = []
for i in range(len(phone_num)):
    number = ''
    for j in range(5):
        if (type(phone_num[j][i]) == str and j>0):
            number = number + phone_num[j][i]
    phone_list.append(number)
#phone_list


# In[35]:


#Add phone numbers to the data frame under column name "phone_numbers"
patients_clean['phone_number'] = phone_list


# In[36]:


# Now parse the contact information for the email
patients_clean['email'] = patients_clean['contact'].str.extract('([a-zA-Z][a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+[a-zA-Z])', expand=True)


# In[37]:


patients_clean = patients_clean.drop('contact', axis=1)


# ##### Test

# In[38]:


patients_clean.head()


# In[39]:


patients_clean.info()


# In[40]:


# Your testing code here
patients_clean.phone_number.sample(10) #blank spots are contacts with no phone numbers


# In[41]:


patients_clean.email.sample(10)


# #### Three variables in two columns in `treatments` table (treatment, start dose and end dose)

# ##### Define
# *We want to split up the auralin and novodra columns into 3 different columns. One called treatment that lists the type of drug, one for the start dose, and one for the end dose. Also, remove the u as this unit can be added to the column description.*
# 
# >Hint: use pandas' [melt function](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.melt.html) and [`str.split()` method](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.str.split.html). Here is an excellent [`melt` tutorial](https://deparkes.co.uk/2016/10/28/reshape-pandas-data-with-melt/).

# ##### Code

# In[42]:


# Your cleaning code here
treatments_clean.head()


# In[43]:


# Separate into treatment and start_end_dose columns (second column to be divided further)
melt = pd.melt(treatments_clean, id_vars=["given_name",'surname','hba1c_start','hba1c_end', 'hba1c_change'], value_vars=['auralin','novodra'], var_name='treatment', value_name='start_end_dose')
melt.head()


# In[44]:


# Get rid of duplicate entries, i.e. start_end_dose == '-'
melt_1 = melt[melt['start_end_dose'] != '-']
melt_1.head()


# In[45]:


#Separate start_end_dose into two columns, turn to ints.
start = []
end = []
for i in range(len(melt_1)):
    s,d,e = melt_1.iloc[i,6].split()
    start.append(s[:-1])
    end.append(e[:-1])

melt_1['start_dose'] = start;
melt_1['end_dose'] = end;
melt_1.tail()


# In[46]:


treatments_clean = melt_1.drop('start_end_dose', axis=1)


# In[47]:


# Your testing code here
treatments_clean.tail()


# #### Adverse reaction should be part of the `treatments` table

# ##### Define
# *Combine adverse reaction table with treatments table using a join on the treatments table. Join on given and surname.*
# 
# >Hint: [tutorial](https://chrisalbon.com/python/pandas_join_merge_dataframe.html) for the function used in the solution.

# ##### Code

# In[48]:


# Your cleaning code here
treatments_clean = pd.merge(treatments_clean, adverse_reactions_clean, on=['given_name','surname'], how='left')


# ##### Test

# In[49]:


# Your testing code here
print(len(treatments_clean))
treatments_clean.head(15)


# #### Given name and surname columns in `patients` table duplicated in `treatments` and `adverse_reactions` tables  and Lowercase given names and surnames

# ##### Define
# *Don't need to worry about adverse_reactions table as this has been added to treatments table. We need to merge the patient_id's from the patients table into the treatments table, and then we can delete the given and surname. Do this by creating another dataframe with the given name (lower), surname (lower), and id from the patients table, and then merge this with the treatments table on given and surname. Once merged, we can delete these name columns*
# >Hint: [tutorial](https://chrisalbon.com/python/pandas_join_merge_dataframe.html) for one function used in the solution and [tutorial](http://erikrood.com/Python_References/dropping_rows_cols_pandas.html) for another function used in the solution.

# ##### Code

# In[50]:


# Your cleaning code here
df_id = patients_clean[['given_name','surname','patient_id']]
df_id['given_name'] = df_id.given_name.str.lower()
df_id['surname'] = df_id.surname.str.lower()
df_id.head()


# In[51]:


treatments_clean = pd.merge(treatments_clean, df_id, on = ['given_name','surname'], how = 'left')
treatments_clean.head()


# In[52]:


treatments_clean = treatments_clean.drop(['given_name','surname'], axis =1)


# ##### Test

# In[53]:


# Your testing code here
treatments_clean


# In[54]:


# Only duplicated column is patient_id
all_cols = pd.Series(list(patients_clean) + list(treatments_clean))
all_cols[all_cols.duplicated()]


# ### Quality

# #### Zip code is a float not a string and Zip code has four digits sometimes

# ##### Define
# 1) Zip codes need to be a string not an int
# 
# 2) Zip codes all must be 5 digits long. Pad the 4 int zip codes with a 0 in the front. Do this while ignoring nan values
# 
# *. Hint: see the "Data Cleaning Process" page.*

# ##### Code

# In[55]:


patients_clean.zip_code = patients_clean.zip_code.astype(str)


# In[56]:


# Turns zip code into string and then makes sure all valid zip codes are 5 characters long
zip_codes = patients_clean.zip_code.astype(str)
for i in range(len(zip_codes)):
    if zip_codes[i] != 'nan':
        zip_codes[i] = zip_codes[i][:-2]
for i in range(len(zip_codes)):
    if len(zip_codes[i]) < 5:
        if zip_codes[i] != 'nan':
            zip_codes[i] = '0' + zip_codes[i]


# In[57]:


patients_clean.zip_code = zip_codes


# ##### Test

# In[58]:


# Your testing code here
patients_clean.zip_code.sample(20)


# #### Tim Neudorf height is 27 in instead of 72 in

# ##### Define
# *Simple slip up in entry, as it is unlikely this man is 27 inches tall. Fix individual entry using df.loc*

# ##### Code

# In[59]:


# Your cleaning code here
patients_clean[patients_clean.surname == 'Neudorf'].height #row is 4
patients_clean.loc[4,'height'] = 72


# ##### Test

# In[60]:


# Your testing code here
patients_clean[patients_clean.surname == 'Neudorf'].height


# #### Full state names sometimes, abbreviations other times

# ##### Define
# 1) Find which states aren't abbreviated.
# 
# 2) Make a dictionary of these longer state names with their abbreviated state names
# 
# 3) Loop through the states name column and if the entry matches the longer name, assign the shorter name to that value
# 
# *Hint: [tutorial](https://chrisalbon.com/python/pandas_apply_operations_to_dataframes.html) for method used in solution.*

# ##### Code

# In[61]:


# Your cleaning code here
patients_clean.state.value_counts()


# In[62]:


# We see that the only states that aren't abreviated are California (CA), New York (NY), 
# Illinois (IL), Florida (FL), and Nebraska (NE). Just have to change these.
bad_states = {'California': 'CA', 'New York': 'NY', 'Illinois': 'IL', 'Florida': 'FL', 'Nebraska': 'NE'}
for i in range(len(patients_clean.state)):
    if patients_clean.state[i] in bad_states:
        patients_clean.state[i] = bad_states[patients_clean.state[i]]


# ##### Test

# In[63]:


# Your testing code here
patients_clean.state.value_counts() # And now we see no full state name


# #### Dsvid Gustafsson

# ##### Define
# *Typo using 's' instead of 'a'. Fix using single replacement on location (loc)*

# ##### Code

# In[64]:


# Your cleaning code here
patients_clean[patients_clean.surname == 'Gustafsson'] # row is 8, use given_name = Dsvid
patients_clean.loc[8,'given_name'] = 'David'


# ##### Test

# In[65]:


# Your testing code here
patients_clean[patients_clean.surname == 'Gustafsson']


# #### Erroneous datatypes (assigned sex, state, zip_code, and birthdate columns) and Erroneous datatypes (auralin and novodra columns) and The letter 'u' in starting and ending doses for Auralin and Novodra

# ##### Define
# *For sex and zip_code use astype() function and change to categories, and for birthdate use this function to change to datetime. Zip code is already fixed so we can ignore that. Letter 'u' in auralin and novodra has already been removed so we can ignore that, simply turn these strings to ints*
# 
# >Hint: [documentation page](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.astype.html) for one method used in solution, [documentation page](http://pandas.pydata.org/pandas-docs/version/0.20/generated/pandas.to_datetime.html) for one function used in the solution, and [documentation page](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.str.strip.html) for another method used in the solution.

# ##### Code

# In[66]:


# Your cleaning code here
patients_clean.head(2)


# In[67]:


patients_clean.assigned_sex = patients_clean.assigned_sex.astype('category')
patients_clean.state = patients_clean.state.astype('category')


# In[68]:


patients_clean.birthdate = pd.to_datetime(patients_clean.birthdate)


# In[69]:


treatments_clean.start_dose = treatments_clean.start_dose.astype('int')
treatments_clean.end_dose = treatments_clean.end_dose.astype('int')


# ##### Test

# In[70]:


# Your testing code here
patients_clean.info()


# In[71]:


treatments_clean.info()


# #### Multiple phone number formats

# ##### Define
# *This problem was fixed in the initial phone number changes. We removed the +1 from all numbers, all all patients were US residents* 
# 
# Hint: helpful [Stack Overflow answer](https://stackoverflow.com/a/123681).

# #### Default John Doe data

# ##### Define
# *(Recall that it is assumed that the data that this John Doe data displaced is not recoverable). Thus we can simply remove all 'John Doe' data from the patients data frame*

# ##### Code

# In[96]:


#Ignore 'Doe' surname
patients_clean = patients_clean[patients_clean['surname'] != 'Doe']


# ##### Test

# In[97]:


# Your testing code here
patients_clean[patients_clean['surname'] == 'Doe']


# #### Multiple records for Jakobsen, Gersten, Taylor

# ##### Define
# *Set patients table to only include the first instance of each of these names. For all cases, the difference lies in that the given name in the duplicate is a nickname for the actual given name. Delete this nickname entries*

# ##### Code

# In[185]:


# Your cleaning code here
patients_clean = patients_clean[~((patients_clean.address.duplicated()) & patients_clean.address.notnull())]


# ##### Test

# In[186]:


patients_clean[patients_clean['surname'] == 'Taylor']


# In[187]:


patients_clean[patients_clean['surname'] == 'Jakobsen']


# In[188]:


patients_clean[patients_clean['surname'] == 'Gersten']


# #### kgs instead of lbs for Zaitseva weight

# ##### Define
# *Find the location for Zaitseva's weight and multiply this weight by the conversion factor*

# ##### Code

# In[189]:


# Your cleaning code here
patients_clean[patients_clean['surname'] == 'Zaitseva'] #Multiply 48.8 by 2.20462


# In[194]:


patients_clean.loc[210,'weight'] = patients_clean.loc[210,'weight']*2.20462


# ##### Test

# In[195]:


# Your testing code here
patients_clean.loc[210,'weight']

