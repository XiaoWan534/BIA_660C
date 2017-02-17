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

        if [col_name for col_name in self.header if self.header.count(col_name) > 1]:
            raise Exception('Dumplicated Column Name Found!')

        self.data = [[value.strip() for value in row] for row in self.data]

        # ============ Task 2 (type modification for comparision) ============












        self.data = [OrderedDict(zip(self.header, row)) for row in self.data]



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
                        raise TypeError('Something wrong with the tuple list input.')

                else:
                    return [[value for value in row.itervalues()][item[1]] for row in rowz]
            else:
                if isinstance(item[1], (int, slice)):
                    return [[value for value in row.itervalues()][item[1]] for row in self.data[item[0]]]
                elif isinstance(item[1], str):
                    return [row[item[1]] for row in self.data[item[0]]]
                else:
                    raise TypeError('Something wrong with the tuple input.')

        elif isinstance(item, str):
            return [row[item] for row in self.data]

        elif isinstance(item, list):
            if all([isinstance(column_name, str) for column_name in item]):
                return [[row[column_name] for column_name in item] for row in self.data]
            # ============ Task 2 (to support lists of booleans) ============
            elif all([isinstance(index, bool) for row_called in item]):
                return [row for index, row in enumerate(self.data) if item[index]]
            else:
                raise TypeError('Something wrong with the list input.')


    def get_rows_where_column_has_value(self, column_name, value, index_only=False):
        if index_only:
            return [index for index, row_value in enumerate(self[column_name]) if row_value==value]
        else:
            return [row for row in self.data if row[column_name]==value]


    # ============ Task 1 ============
    def sort_by(self, column_name, reverse=False):
        if isinstance(column_name, str):
            return sorted(self.data, key=lambda row: row[column_name], reverse=reverse)

        # ============ Task 1 extra ============
        elif isinstance(column_name, list):
            if isinstance(reverse, list):
                for index, name in enumerate(column_name):
                    reverse_index=len(column_name)-index-1
                    self.data = sorted(self.data, key=lambda row: row[column_name[reverse_index]], reverse=reverse[reverse_index])
                return self.data
            else:
                return Exception('Argument Enter Error!')
        else:
            return Exception('Argument Enter Error!')


# ============ Task 2 (define Series object work with all comparison operators) ============










df = DataFrame.from_csv('SalesJan2009.csv')

# test Task 1
sort1 = df.sort_by('Product', True)
sort2 = df.sort_by(['Product','Payment_Type'], [True, False])

# test Task 2
df[df['Price'] > 1400]


2+2