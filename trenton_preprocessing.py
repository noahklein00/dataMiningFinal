import pandas as pd
import noahProcess as np

INPUT_DATA_FILE_NAME = "Pokemon.csv"
OUTPUT_DATA_FILE_NAME = "trenton_pokemon.csv"

def main():
	# Load csv data in pandas
	df = pd.read_csv(INPUT_DATA_FILE_NAME)

	# Replace missing "Type1" values
	df = replace_missing_type1_values(df)

	# Replace missing "Type2" values with "none"
	df = replace_missing_type2_values(df)

	# Check the sum for "Total" and correct if needed
	df = check_and_correct_total_sum(df)

	# Make all "Legendary" values uniform "true", "false", or "unknown"
	df = make_legendary_uniform(df)

	df = np.processGeneration(df)
	df = np.removeDuplicates(df)
	df = np.removeWorthlessAttributes(df)

	# Output the updated dataframe to a new csv
	df.to_csv(OUTPUT_DATA_FILE_NAME, index=False)


def replace_missing_type1_values(df):

	# Replace missing "Type1" values with "none"
	df["Type1"].fillna("none", inplace = True)

	# Replace "?" values with "none"
	df.update(df["Type1"].replace("?", "none"))

	# Make all "Type2" values lowercase
	df["Type1"] = df["Type1"].str.lower()

	return df


def replace_missing_type2_values(df):

	# Replace missing "Type2" values with "none"
	df["Type2"].fillna("none", inplace = True)

	# Replace "?" values with "none"
	df.update(df["Type2"].replace("?", "none"))

	# Make all "Type2" values lowercase
	df["Type2"] = df["Type2"].str.lower()

	return df


def check_and_correct_total_sum(df):

	# Check that the sum of "HP", "Attack", "Defense", "SpAtk", "SpDef", and "Speed"
	# add up to the same number as "Total". If there is a discrepancy, replace
	# the "Total" value with the calculated sum
	for index, row in df.iterrows():

		# The recorded value for "Total" in the dataframe
		total_recorded = row["Total"]
		if total_recorded != "?":
			total_recorded = int(total_recorded)

		# Each column that needs to be summed for total
		composition_columns = ["HP", "Attack", "Defense", "SpAtk", "SpDef", "Speed"]

		# Calculate the actual sum of each of the composition columns
		total_sum = 0
		for column_name in composition_columns:
			if row[column_name] != "?":
				total_sum += int(row[column_name])

		# Check if the sum matches the recorded value
		if total_recorded != total_sum:
			# Replace the incorrect values with the calculated sum
			df.at[index, "Total"] = total_sum

	return df


def make_legendary_uniform(df):

	# Convert all "Legendary" values to lower case
	df["Legendary"] = df["Legendary"].str.lower()

	# Check each row's "Legendary" value, change to "false" or "true" as needed
	for index, row in df.iterrows():

		# The recorded value for "Legendary"
		legendary_recorded = row["Legendary"]

		# Correct values of "f" to "false", "t" to "true" and "?" to "unknown"
		if legendary_recorded == "f":
			df.at[index, "Legendary"] = "false"
		elif legendary_recorded == "t":
			df.at[index, "Legendary"] = "true"
		elif legendary_recorded == "?":
			df.at[index, "Legendary"] = "unknown"

	return df


if __name__ == "__main__":
	main()