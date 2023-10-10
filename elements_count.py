import os

# Path containing the files .txt
emails='gestores_email'
office='herramientas_office'
browsers='navegadores'
source = f'./labels'
counted_elements = {}
# We loop through all the files in the path
for filename in os.listdir(source):
    if filename.endswith('.txt'):
        pathfile = os.path.join(source, filename)
        
        # we open the file and read the first column by every line
        with open(pathfile, 'r') as file:
            for line in file:
                # Split the lines in columns (it is separate for spaces)
                column = line.strip().split()[0]
                if column in counted_elements:
                    counted_elements[column] += 1
                else:
                    counted_elements[column] = 1
names_elements= ['Buttons','Cells','Checkbox','DropDownList', 'HamburguerLIst', 'Icon','ListBoxes', 
        'ProgressBar', 'RadioButton', 'SearchBox','Submenu', 'TextFields', 'Toggles']

# Print results
for element, quantity in counted_elements.items():      
    print(f"{names_elements[int(element)]}: {quantity}")