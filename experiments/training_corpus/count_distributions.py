import pandas as pd
import re

def mean_and_std_dev_words_in_cell(file_path):
    # Read the spreadsheet into a pandas DataFrame
    df = pd.read_csv(file_path)  # Update this line based on your spreadsheet format (e.g., pd.read_csv for CSV files)

    # Function to count words in a cell
    def count_words(cell):
        words = re.findall(r'\b\w+\b', str(cell))
        return len(words)

    # Apply the count_words function to each cell in the DataFrame
    df['Word Count'] = df["excerpt"].map(count_words)

    # Calculate mean and standard deviation of word count
    mean_word_count = df['Word Count'].mean()
    std_dev_word_count = df['Word Count'].std()

    return mean_word_count, std_dev_word_count


mean_result, std_dev_result = mean_and_std_dev_words_in_cell("description.csv")
print(f'Mean number of words in the spreadsheet cells: {mean_result:.2f}')
print(f'Standard deviation of word count: {std_dev_result:.2f}')
