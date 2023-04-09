import openpyxl
def values(temp): 
# Open the spreadsheet
    workbook = openpyxl.load_workbook("POA.xlsx")
  
# Get the first sheet
    sheet = workbook.worksheets[0]
# Create a list to store the values
    head = []
    if(temp%50!=0):
        if(temp%50>25):
            temp=temp-temp%50+50
        else:
            temp-=temp%50
  
# Iterate over the rows in the sheet
    for row in sheet:
    # Get the value of the first cell
    # in the row (the "Name" cell)
        name = row[0].value
    # Add the value to the list
        if(name==temp):
            for col in range(5):
                head.append(row[col].value)
# Print the list of names
    return(head)