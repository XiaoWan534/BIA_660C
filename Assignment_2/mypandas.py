import csv
from collections import OrderedDict

class DataFrame(object):

    @classmethod
    def from_csv(cls, file_path, delimiting_character=',', quote_character='"'):
        with open(file_path, 'rU') as infile:
            reader = csv.reader(infile, delimiter=delimiting_character, quotechar=quote_character)
            data = []
            for row in reader:
                data.append(row)
            return cls(list_of_lists=data)



    def __init__(self, list_of_lists, header=True):

        if header:
            self.header = list_of_lists[0]
            self.data = list_of_lists[1:]
        else:
            self.data = list_of_lists
            generated_header = []
            for index, column in enumerate(self.data[0]):
                generated_header.append('column' + str(index + 1))
            self.header = generated_header

        # =========== Task 1 =============
        # To check if all column names are unique
        if [col_name for col_name in self.header if self.header.count(col_name) > 1]:
            raise Exception('Dumplicated column name found!')

        # =========== Task 2 =============
        # To strip any leading and trailing whitespaces from strings in the data
        self.data = [[value.strip() for value in row] for row in self.data]

        ordered_dict_rows = []
        for row in self.data:
            ordered_dict_data = []
            for index, row_value in enumerate(row):
                ordered_dict_data.append((self.header[index], row_value))

            ordered_dict_row = OrderedDict(ordered_dict_data)
            ordered_dict_rows.append(ordered_dict_row)
        self.data = ordered_dict_rows



    def __getitem__(self, item):

        if isinstance(item, (int, slice)):
            return self.data[item]

        elif isinstance(item, tuple):
            if isinstance(item[0], list) or isinstance(item[1], list):

                if isinstance(item[0], list):
                    rowz = [row for index, row in enumerate(self.data) if index in item[0]]
                else:
                    rowz = self.data[item[0]]

                if isinstance(item[1], list):
                    if all([isinstance(thing, int) for thing in item[1]]):
                        return [[column_value for index, column_value in enumerate([value for value in row.itervalues()]) if index in item[1]] for row in rowz]
                    elif all([isinstance(thing, str) for thing in item[1]]):
                        return [[row[column_name] for column_name in item[1]] for row in rowz]
                    else:
                        raise TypeError('What the hell is this?')

                else:
                    return [[value for value in row.itervalues()][item[1]] for row in rowz]
            else:
                if isinstance(item[1], (int, slice)):
                    return [[value for value in row.itervalues()][item[1]] for row in self.data[item[0]]]
                elif isinstance(item[1], str):
                    return [row[item[1]] for row in self.data[item[0]]]
                else:
                    raise TypeError('I don\'t know how to handle this...')

        elif isinstance(item, str):
            return [row[item] for row in self.data]

        elif isinstance(item, list):
            return [[row[column_name] for column_name in item] for row in self.data]

    def get_rows_where_column_has_value(self, column_name, value, index_only=False):
        if index_only:
            return [index for index, row_value in enumerate(self[column_name]) if row_value==value]
        else:
            return [row for row in self.data if row[column_name]==value]





df = DataFrame.from_csv('SalesJan2009.csv')


# Test for Task 2
test2 = df[3]
print(test2['City'])

2+2