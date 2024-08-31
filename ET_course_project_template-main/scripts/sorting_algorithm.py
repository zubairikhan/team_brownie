import pandas as pd
import os


# Function to parse the filenames
def parse_filename(filename):
    parts = filename.split('_')
    qualified = parts[0]
    picture = 'pic' in parts
    name = parts[-1].split('.')[0]
    sort_type = parts[2].strip()
    return qualified, picture, name, sort_type, filename


def sample_frame(df):
    qualified_with_picture = df[(df['Qualified'] == 'qualified') & (df['Picture'] == True)]
    qualified_without_picture = df[(df['Qualified'] == 'qualified') & (df['Picture'] == False)]
    unqualified_with_picture = df[(df['Qualified'] == 'unqualified') & (df['Picture'] == True)]
    unqualified_without_picture = df[(df['Qualified'] == 'unqualified') & (df['Picture'] == False)]

    qualified_with_picture = qualified_with_picture.sample(3)
    qualified_without_picture = qualified_without_picture[~qualified_without_picture['Name'].isin(qualified_with_picture['Name'].to_list())]

    unqualified_with_picture = unqualified_with_picture.sample(3)
    unqualified_without_picture = unqualified_without_picture[~unqualified_without_picture['Name'].isin(unqualified_with_picture['Name'].to_list())]

    # Create a combination with required criteria
    valid_subset = pd.concat([
        qualified_with_picture,
        qualified_without_picture,
        unqualified_with_picture,
        unqualified_without_picture
    ])
    return valid_subset

# Main script
if __name__ == "__main__":
    # Load files
    files = os.listdir("./eye-tracking/resumes")

    # Create dataframe
    data = [parse_filename(file) for file in files]
    df = pd.DataFrame(data, columns=['Qualified', 'Picture', 'Name', 'Sorting Method', 'Filename'])

    # Define names and nationalities
    names = ['tian', 'viktor', 'kare', 'hannah', 'maria', 'hans', 'leila',
             'lea', 'rahul', 'aisha', 'emilia', 'david']

    name_to_nationality = {
        'emilia': 'Hispanic/Latina (studied in Switzerland)',
        'lea': 'White (Denmark)',
        'hannah': 'Spanish/Latina/Hispanic (studied in Germany)',
        'tian': 'Chinese',
        'david': 'Black (South Africa)',
        'viktor': 'White (Russian)',
        'rahul': 'Indian',
        'hans': 'White (Germany)',
        'kare': 'White (Norway)',
        'aisha': 'Black (American)',
        'leila': 'Arabic (from UAE)',
        'maria': 'Italian'
    }

    # Add nationality to dataframe
    df['Nationality'] = df['Name'].apply(lambda x: name_to_nationality[x])

    # Define rules
    rules = lambda df: [
        set(df['Name'].unique()) == set(names),
        df['Qualified'].value_counts()['qualified'] == 6,
        df['Picture'].value_counts()[True] == 6,
    ]

    # Generate and save subsets
    all_frames = []
    for i in range(15):
        subset = sample_frame(df)
        all_frames.append(subset)

        subset['correct_type'] = subset['Qualified'].apply(lambda x: "y" if x == "qualified" else "n")
        subset.rename(columns={"Filename": "image_file"}, inplace=True)

        subset[['correct_type', 'image_file']].to_csv(f"{i}_participant.csv", index=False)

        if not all(rules(subset)):
            print(f"Bad sorting for subset {i}")
        else:
            print(f"Subset {i} generated successfully")

    print("All subsets generated and saved.")
