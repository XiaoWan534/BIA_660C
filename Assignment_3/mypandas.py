import csv
from collections import OrderedDict, defaultdict

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
        def type_modify(row):
            for i in range(len(row)):
                # transform data to proper format as time, string, number
                try:
                    row[i] = datetime.datetime.strptime(row[i], '%m/%d/%y %H:%M')
                except:
                    try:
                        row[i] = row[i].strip()
                    except:
                        try:
                            row[i] = float(row[i].replace(',', ''))
                        except:
                            pass
            return row

        # assure data is in proper format before return
        self.data = [type_modify(row) for row in self.data]

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
            # return a series so that comparison is applicable, and then we cen get a boolean string fo next step
            return Series([row[item] for row in self.data])

        elif isinstance(item, list):
            if all([isinstance(column_name, str) for column_name in item]):
                return [[row[column_name] for column_name in item] for row in self.data]

            # ============ Task 2 (to support lists of booleans) ============
            elif all([isinstance(index, bool) for index in item]):
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
            self.data = sorted(self.data, key=lambda row: row[column_name], reverse=reverse)
            return self

        # ============ Task 1 extra ============
        elif isinstance(column_name, list):
            if isinstance(reverse, list):
                for index, name in enumerate(column_name):
                    reverse_index=len(column_name)-index-1
                    self.data = sorted(self.data, key=lambda row: row[column_name[reverse_index]], reverse=reverse[reverse_index])
                return self
            else:
                raise Exception('Argument Enter Error!')
        else:
            raise Exception('Argument Enter Error!')


    # ============ Task 3 ============
    def group_by(self, key_col, f_col, f):
        d = defaultdict(list)
        if isinstance(f_col, str):

            if isinstance(key_col, str):
                group = [key_col, f_col]
                for index, row_value in enumerate(self[key_col]):
                    d[row_value].append(row_f for index_f, row_f in enumerate(self[f_col]) if index_f == index)
                for key in d.keys():
                    group.append(key,f(d[key]))
                return DataFrame(group, header=True)

            elif isinstance(key_col, list):
                if all([isinstance(col_name, str) for col_name in key_col]):
                    for key_row in set(self[col_group[0]].data):
                        return None
        else:
            raise TypeError('Something wrong with the second argument.')


# ============ Task 2 (define Series object work with all comparison operators) ============
class Series(list):
    def __eq__(self, item):
        comparison = []
        for value in self:
            comparison.append(value == item)
        return comparison

    def __lt__(self, item):
        comparison = []
        for value in self:
            comparison.append(value < item)
        return comparison

    def __gt__(self, item):
        comparison = []
        for value in self:
            comparison.append(value > item)
        return comparison

    def __ge__(self, item):
        comparison = []
        for value in self:
            comparison.append(value >= item)
        return comparison

    def __le__(self, item):
        comparison = []
        for value in self:
            comparison.append(value <= item)
        return comparison


def avg(list_of_values):
    return sum(list_of_values)/float(len(list_of_values))




df = DataFrame.from_csv('SalesJan2009.csv')

# test Task 1
sort1 = df.sort_by('Product', True)
sort2 = df.sort_by(['Product','Payment_Type'], [True, False])

print(sort1['Product'])

# test Task 2
b_ix = df['Price'] > 1400
bool_ix = df[df['Price'] > 1400]


# test Task 3
group1 = df.group_by('Payment_Type', 'Price', avg)
#group2 = df.group_by(['City', 'Payment_Type'], 'Price', avg)

2+2