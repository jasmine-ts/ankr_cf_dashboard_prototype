import pandas as pd
import os
import glob

def main():
    path = './24H_CSVs'
    all_files = sorted(glob.glob(os.path.join(path, "*.csv")))

    filenames = []

    date_start, date_fin = all_files[0].find('_24Hcounts'), all_files[0].find('.csv')
    workbook_name = all_files[0][date_start+11 : date_fin]

    for s in all_files:

        # Extract some filename info to serve as a (condensed) Excel tab name
        fn_start, fn_fin = s.find('./24H_CSVs/'), s.find('_24Hcounts')
        
        filename = s[fn_start+11 : fn_fin]
        filenames.append(filename)


    writer = pd.ExcelWriter(workbook_name + '.xlsx', engine='xlsxwriter')
    workbook = writer.book
    header_format = workbook.add_format({'bold': True, 'align': 'center', 'border': 1}) # Formatting option to be used later

    # Create a Pandas dataframe from each input CSV file
    df_from_each_file = (pd.read_csv(f) for f in all_files)

    # Iterate through all the dataframes and add to the combined Excel workbook
    for idx, df in enumerate(df_from_each_file):

        df.to_excel(writer, sheet_name=filenames[idx].format(idx), index=False)
        worksheet = writer.sheets[filenames[idx]]

        # Change the header text of the worksheet Index column
        worksheet.write(0, 0, 'Index', header_format)

        # Find the length of the longest string in each column and set width accordingly
        for idx, col in enumerate(df):
            series = df[col]
            max_len = max((
                series.astype(str).map(len).max(),  # len of largest item
                len(str(series.name))  # len of column name/header
                )) + 1  # adding a little extra space
            worksheet.set_column(idx, idx, max_len)  # set column width
        
    writer.save()

    print(workbook_name) # Used to pipe the workbook name into bash script variable

if __name__ == "__main__":
    main()