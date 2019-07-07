#coding=utf-8

class Semantic():

    def __init__(self):
        self.indent = "  "
        self.symbol_table = []
        self.symbol_name = []
        self.error_table = []
        self.offset = 0

    def getNextParse(self, index):
        if index < self.length:
            parse_one = self.parse_array[index]
            print
            i = 0
            for symbol in parse_one:
                if not symbol == ' ':
                    break
                i = i + 1
            # grade = i/2
            print("行： " + parse_one[i:])
            return parse_one[i:]
        else:
            return ''

    def analyze(self, parse_result):
        result = ''
        self.parse_array = parse_result.split("\n")
        self.length = len(self.parse_array)
        index = 0
        value = self.getNextParse(index)
        index = index + 1
        if value[0] == 'P':
            index = self.P_func(index)
        else:
            result = 'error'
        symbol_result = self.deal_symbol()
        error_result = self.deal_error()
        return symbol_result + error_result

    def deal_symbol(self):
        symbol_result = '符号表:\nName\tType\tOffset\n'
        for row in self.symbol_table:
            symbol_result = symbol_result + row[0] + '\t' + row[1] + '\t' + row[2] + '\n'
        return symbol_result

    def deal_error(self):
        error_result = 'Error:\n'
        for row in self.error_table:
            error_result = error_result + 'Error at line ' + row[0] + ': ' + row[1] + '\n'
        return error_result

    def P_func(self, index):
        self.offset = 0
        index = index + 1
        index, d_width = self.D_func(index)
        index = index + 1
        index = self.S_func(index)

        return index

    def D_func(self, index):
        value = self.getNextParse(index)

        if value[0:4] == 'proc':
            index = index + 2
            index, x_type, x_width = self.X_func(index)
            index = index + 1
            index, c_type, c_width = self.C_func(index)
            id_info = self.getNextParse(index)
            id_value = id_info.split('(')[0]
            id_value = id_value[4:]
            index = index + 4
            index, d_width = self.D_func(index)
            index = index + 1
            index = self.D1_func(index)
            if id_value in self.symbol_name:
                id_line = id_info.split('(')[1]
                id_line = id_line.split(')')[0]
                self.error_table.append((id_line, '重复的函数声明'))
                return index, 0
            else:
                self.symbol_table.append((id_value, 'proc', self.offset))
                self.offset = self.offset + 8
                return index, 8
        else:
            index, t_type, t_width = self.T_func(index)
            index = index + 1
            id_info = self.getNextParse(index)
            id_value = id_info.split('(')[0]
            id_value = id_value[4:]
            index = index + 1
            if id_value in self.symbol_name:
                id_line = id_info.split('(')[1]
                id_line = id_line.split(')')[0]
                self.error_table.append((id_line, '重复的变量声明'))
                t_width = 0
            else:
                self.symbol_table.append((id_value, t_type, self.offset))
                self.offset = self.offset + t_width
            index = index + 1
            index = self.D1_func(index)
            return index, t_width

    def D1_func(self, index):
        '''
        接收错误字符时返回空字符，即将错误字符当成结束符
        :param grade:
        :param index:
        :return:
        '''
        value = self.getNextParse(index)
        if value[0] == 'D':
            index = index + 1
            index, d_width = self.D_func(index)
            index = index + 1
            index = self.D1_func(index)
            return index
        else:
            return index

    def T_func(self, index):
        value = self.getNextParse(index)
        if value[0] == 'X':
            index = index + 1
            index, x_type, x_width = self.X_func(index)
            t = x_type
            w = x_width
            index = index + 1
            index, c_type, c_width = self.C_func(index, t, w)
            return index, c_type, c_width
        else:
            index = index + 4
            index, d_width = self.D_func(index)
            index = index + 1
            id_info = self.getNextParse(index)
            id_value = id_info.split('(')[0]
            id_value = id_value[4:]
            index = index + 2
            t_type = 'record'
            t_width = d_width
            if id_value in self.symbol_name:
                id_line = id_info.split('(')[1]
                id_line = id_line.split(')')[0]
                self.error_table.append((id_line, '重复的变量声明'))
                t_width = 0
            else:
                self.symbol_table.append((id_value, t_type, self.offset))
                self.offset = self.offset + t_width
            return index, t_type, t_width

    def X_func(self, index):
        value = self.getNextParse(index)
        if value[0:4] == 'char':
            x_type = 'char'
            x_width = 1
        elif value[0:3] == 'int':
            x_type = 'int'
            x_width = 4
        elif value[0:5] == 'float':
            x_type = 'float'
            x_width = 4
        elif value[0:7] == 'boolean':
            x_type = 'boolean'
            x_width = 4
        else:
            x_type = 'string'
            x_width = 8
        index = index + 1
        return index, x_type, x_width

    def C_func(self, index, t, w):
        value = self.getNextParse(index)
        if value[0] == '[':
            index = index + 1
            num_val = self.getNextParse(index).split(': ')[1]
            num_val = num_val.split('(')[0]
            index = index + 3
            index, c_type, c_width = self.C_func(index, t, w)
            c_type = 'array(' + num_val + ', ' + c_type + ')'

            if num_val.isdigit() and not num_val[0] == '-':
                c_width = int(num_val)*c_width
            else:
                id_info = self.getNextParse(index-1)
                id_line = id_info.split('(')[1]
                id_line = id_line.split(')')[0]
                self.error_table.append(id_line, '数组声明是方框内不为正整数')
                c_width = 0
            return index, c_type, c_width
        else:
            c_type = t
            c_width = w
            return index, c_type, c_width

    def S_func(self, index):
        '''
        当接收错误符号时返回空字符，即把错误字符当成终结符
        :param grade:
        :param index:
        :return:
        '''
        return index