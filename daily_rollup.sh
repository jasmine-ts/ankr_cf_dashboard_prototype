#!/bin/bash

offset_days_var='4'
historical_days_var='1'

# 24H request counts from all countries:
python3 GQL_CSV_main.py \
--offset_days "${offset_days_var}" \
--historical_days "${historical_days_var}" \
--dataset 'httpRequestsAdaptiveGroups' \
--raw_data_cols 'count' 'dimensions.clientCountryName' \
--renamed_data_cols 'Count' 'clientCountryName' \
--query_name 'clientCountryName_24Hcounts' \
--query_textfile 'clientCountryName_query.txt' \
--opt_filter "none" \
--payload_flag 'no_filter'

# 24H top referers, all blockchains:
python3 GQL_CSV_main.py \
--offset_days "${offset_days_var}" \
--historical_days "${historical_days_var}" \
--dataset 'httpRequestsAdaptiveGroups' \
--raw_data_cols 'count' 'dimensions.clientRefererHost' \
--renamed_data_cols 'Count' 'Referer' \
--query_name 'clientRefererHost_allChains_24Hcounts' \
--query_textfile 'clientRefererHost_allChains.txt' \
--opt_filter "none" \
--payload_flag 'no_filter'

# 24H top referers, Arbitrum:
python3 GQL_CSV_main.py \
--offset_days "${offset_days_var}" \
--historical_days "${historical_days_var}" \
--dataset 'httpRequestsAdaptiveGroups' \
--raw_data_cols 'count' 'dimensions.clientRefererHost' \
--renamed_data_cols 'Count' 'Referer' \
--query_name 'clientRefererHost_arbitrum_24Hcounts' \
--query_textfile 'clientRefererHost_blockchain_query.txt' \
--opt_filter "%arbitrum%" \
--payload_flag 'blockchain_filter'

# 24H top referers, Avalanche:
python3 GQL_CSV_main.py \
--offset_days "${offset_days_var}" \
--historical_days "${historical_days_var}" \
--dataset 'httpRequestsAdaptiveGroups' \
--raw_data_cols 'count' 'dimensions.clientRefererHost' \
--renamed_data_cols 'Count' 'Referer' \
--query_name 'clientRefererHost_avalanche_24Hcounts' \
--query_textfile 'clientRefererHost_blockchain_query.txt' \
--opt_filter "%avalanche%" \
--payload_flag 'blockchain_filter'

# 24H top referers, BSC:
python3 GQL_CSV_main.py \
--offset_days "${offset_days_var}" \
--historical_days "${historical_days_var}" \
--dataset 'httpRequestsAdaptiveGroups' \
--raw_data_cols 'count' 'dimensions.clientRefererHost' \
--renamed_data_cols 'Count' 'Referer' \
--query_name 'clientRefererHost_bsc_24Hcounts' \
--query_textfile 'clientRefererHost_blockchain_query.txt' \
--opt_filter "%bsc%" \
--payload_flag 'blockchain_filter'

# 24H top referers, Fantom:
python3 GQL_CSV_main.py \
--offset_days "${offset_days_var}" \
--historical_days "${historical_days_var}" \
--dataset 'httpRequestsAdaptiveGroups' \
--raw_data_cols 'count' 'dimensions.clientRefererHost' \
--renamed_data_cols 'Count' 'Referer' \
--query_name 'clientRefererHost_fantom_24Hcounts' \
--query_textfile 'clientRefererHost_blockchain_query.txt' \
--opt_filter "%fantom%" \
--payload_flag 'blockchain_filter'

# 24H top referers, Polygon:
python3 GQL_CSV_main.py \
--offset_days "${offset_days_var}" \
--historical_days "${historical_days_var}" \
--dataset 'httpRequestsAdaptiveGroups' \
--raw_data_cols 'count' 'dimensions.clientRefererHost' \
--renamed_data_cols 'Count' 'Referer' \
--query_name 'clientRefererHost_polygon_24Hcounts' \
--query_textfile 'clientRefererHost_blockchain_query.txt' \
--opt_filter "%polygon%" \
--payload_flag 'blockchain_filter'


# 24H top referers, Solana:
python3 GQL_CSV_main.py \
--offset_days "${offset_days_var}" \
--historical_days "${historical_days_var}" \
--dataset 'httpRequestsAdaptiveGroups' \
--raw_data_cols 'count' 'dimensions.clientRefererHost' \
--renamed_data_cols 'Count' 'Referer' \
--query_name 'clientRefererHost_solana_24Hcounts' \
--query_textfile 'clientRefererHost_blockchain_query.txt' \
--opt_filter "%solana%" \
--payload_flag 'blockchain_filter'


echo "CSV files created."

combine() {
    python3 combine_CSVs.py
}

# Pipe output of combine_CSVs.py into a file
combine > 'wb_name.txt'

# Define file format string variable
file_format='.xlsx'

# Get contents of wb_name.txt and place in wb_date variable
wb_date=$(<wb_name.txt)

# Store full workbook name string in variable wb_name
wb_name="${wb_date}${file_format}"

echo "CSVs combined into a single Excel workbook."

# Upload combined Excel spreadsheet to Google Drive folder
python3 upload_spreadsheet.py $wb_name

echo "Combined workbook uploaded to Google Drive folder."

delete_individual_CSVs() {
    cd ./24H_CSVs
    find . -type f -delete
}

# Delete individual CSV files from the 24H_CSVs folder
delete_individual_CSVs