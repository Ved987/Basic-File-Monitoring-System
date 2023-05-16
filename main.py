import re
import os
import pandas as pd
from glob import glob
from datetime import datetime

#Enter the FIle Directory where the important files to be monitored are stored
all_files = pd.DataFrame(glob('C:/Users/Vedanshu/PycharmProject/Information Security/Important Files/*'), columns=['Name']) 
Data = pd.DataFrame(columns=['Name', 'Size', 'Last Modified', 'Date Created'])

#Enter the FIle Directory where the Data File is stored which compares changes
Check_Data = pd.read_excel('C:/Users/Vedanshu/PycharmProject/Information Security/Data File.xlsx')

# Importing attributes related to files present in the folder.
Data['Name'] = all_files['Name'].apply(lambda x: re.findall(r'Important file [0-9]{1}', x)[0])
for index, row in all_files.iterrows():
    File = row['Name']
    Data['Size'].iloc[index] = os.path.getsize(File)
    Data['Last Modified'].iloc[index] = datetime.fromtimestamp(os.path.getmtime(File)).strftime('%Y-%m-%d %H:%M:%S')
    Data['Date Created'].iloc[index] = datetime.fromtimestamp(os.path.getctime(File)).strftime('%Y-%m-%d %H:%M:%S')
print(Data)

flag = 0
# Runs Comparision tests on the attributes of the FIles.
for index, row in Data.iterrows():
    if row['Name'] != Check_Data['Name'].iloc[index]:
        print("Changes made to File in Name" + row['Name'])
        flag = 1
    elif row['Size'] != Check_Data['Size'].iloc[index]:
        print("Changes made to File in Size: " + str(row['Size']))
        flag = 1
    elif row['Last Modified'] != Check_Data['Last Modified'].iloc[index]:
        print("Changes made to File in Modification Date: " + str(row['Last Modified']))
        flag = 1
    elif row['Date Created'] != Check_Data['Date Created'].iloc[index]:
        print("Changes made to File in Date of Creation: " + str(row['Date Created']))
        flag = 1


if flag == 1:
    user_in = input("Were these Changes made by user (Y/N)")
    if user_in == 'Y':
        Data.to_excel('Data File.xlsx')
        print("Authorized Updates Made")
    else:
        print("Backup Restored")
        # Deletes the files in which unauthorised changes were made.
        os.remove('C:/Users/Vedanshu/PycharmProject/Information Security/Important Files')
        # Restores the Important files by importing/renaming the backup file as the Important Files folder
        os.rename('C:/Users/Vedanshu/PycharmProject/Information Security/Important Backup','C:/Users/Vedanshu/PycharmProject/Information Security/Important Files')
else:
    print("No Changes were made")