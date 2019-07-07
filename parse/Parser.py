# -*- coding: utf-8 -*-

class Parser():
    def __init__(self):
        self.indent = "  "

    def getNextToken(self, index):
        while True:
            row = self.tokens[index]
            row_number = row.split("\t")[0]
            des = row.split("\t")[2]
            if not des[0] == "<":
                type = "error"
                value = des
                return row_number, type, value
            des = des[1:len(des) - 1]
            des = des.split(",")
            type = des[0]
            value = des[1]
            if type == 'NOTE':
                self.tokens.remove(self.tokens[index])
            else:
                break

        return row_number, type, value
    def analyze(self, tokens):
        self.tokens = tokens
        index = 0
        grade = 0
        row_number, type, value = self.getNextToken(index)
        if type in ('proc', 'record', 'char', 'int', 'float', 'boolean', 'string'):
            index, result = self.P_func(grade, index)
            return result
        else:
            errors = 'error: <' + type + ',' + value + '>' + '\t' + row_number
            return errors

    def P_func(self, grade, index):
        row_number, type, value = self.getNextToken(index)
        head_str = ''
        for i in range(grade):
            head_str += self.indent
        result = head_str + 'P (' + row_number + ')' + '\n'
        index1, result1 = self.D_func(grade+1, index)
        index2, result2 = self.S_func(grade+1, index1)
        result += result1 + result2
        return index2, result

    def D_func(self, grade, index):
        row_number, type, value = self.getNextToken(index)
        head_str = ''
        for i in range(grade):
            head_str += self.indent
        result = head_str + 'D (' + row_number + ')' + '\n'
        head_str = head_str + self.indent
        if type == 'proc':
            index += 1
            result2 = head_str + 'proc (' + row_number + ')' + '\n'
            result += result2
            index, result2 = self.X_func(grade+1, index)
            result += result2
            index, result2 = self.C_func(grade+1, index)
            result += result2

            row_number, type, value = self.getNextToken(index)
            if type == 'IDN':
                index += 1
                result2 = head_str + 'id: ' + value + ' (' + row_number + ')' + '\n'
                result += result2
            else:
                index += 1
                self.Error_des(row_number, 'IDN', type)
                errors = head_str + 'error: <' + type + ',' + value + '>' + '\t' + row_number
                result += errors
                return index, result

            row_number, type, value = self.getNextToken(index)
            if type == '(':
                index += 1
                result2 = head_str + '( (' + row_number + ')' + '\n'
                result += result2
            else:
                index += 1
                self.Error_des(row_number, '(', type)
                errors = head_str + 'error: <' + type + ',' + value + '>' + '\t' + row_number
                result += errors
                return index, result

            row_number, type, value = self.getNextToken(index)
            if type == ')':
                index += 1
                result2 = head_str + ') (' + row_number + ')' + '\n'
                result += result2

            elif type in ('char', 'int', 'float', 'boolean', 'string'):
                while True:
                    index += 1
                    row_number, type, value = self.getNextToken(index)
                    if type == ')':
                        index += 1
                        result2 = head_str + ') (' + row_number + ')' + '\n'
                        result += result2
                        break
            else:
                index += 1
                self.Error_des(row_number, 'char, int, float, boolean, string', type)
                errors = head_str + 'error: <' + type + ',' + value + '>' + '\t' + row_number
                result += errors
                return index, result

            row_number, type, value = self.getNextToken(index)
            if type == '{':
                index += 1
                result2 = head_str + '{ (' + row_number + ')' + '\n'
                result += result2
            else:
                index += 1
                self.Error_des(row_number, '{', type)
                errors = head_str + 'error: <' + type + ',' + value + '>' + '\t' + row_number
                result += errors
                return index, result

            index, result2 = self.D_func(grade + 1, index)
            result += result2
            index, result2 = self.S_func(grade+1, index)
            result += result2
            row_number, type, value = self.getNextToken(index)
            if type == '}':
                index += 1
                result2 = head_str + '} (' + row_number + ')' + '\n'
                result += result2
            else:
                index += 1
                self.Error_des(row_number, '}', type)
                errors = head_str + 'error: <' + type + ',' + value + '>' + '\t' + row_number
                result += errors
                return index, result
            index, result2 = self.D1_func(grade+1, index)
            result += result2

            return index, result

        elif type in ('record', 'char', 'int', 'float', 'boolean', 'string'):
            index, result2 = self.T_func(grade+1, index)
            result += result2

            row_number, type, value = self.getNextToken(index)
            if type == 'IDN':
                index += 1
                result2 = head_str + 'id: ' + value + '(' + row_number + ')' + '\n'
                result += result2
            else:
                index += 1
                self.Error_des(row_number, 'IDN', type)
                errors = head_str + 'error: <' + type + ',' + value + '>' + '\t' + row_number
                result += errors
                return index, result

            row_number, type, value = self.getNextToken(index)
            if type == ';':
                index += 1
                result2 = head_str + '; (' + row_number + ')' + '\n'
                result += result2
            else:
                index += 1
                self.Error_des(row_number, ':', type)
                errors = head_str + 'error: <' + type + ',' + value + '>' + '\t' + row_number
                result += errors
                return index, result
            index, result2 = self.D1_func(grade+1, index)
            result += result2

            return index, result

        else:
            index += 1
            self.Error_des(row_number, 'proc, char, int, float, boolean, string', type)
            errors = head_str + 'error: <' + type + ',' + value + '>' + '\t' + row_number
            return index, errors

    def D1_func(self, grade, index):
        '''
        接收错误字符时返回空字符，即将错误字符当成结束符
        :param grade:
        :param index:
        :return:
        '''
        head_str = ''
        result = ''
        for i in range(grade):
            head_str += self.indent
        row_number, type, value = self.getNextToken(index)
        result += head_str + 'D\' (' + row_number + ')' + '\n'
        head_str += self.indent

        if type in ('proc', 'record', 'char', 'int', 'float', 'boolean', 'string'):
            index, result2 = self.D_func(grade+1, index)
            result += result2
            index, result2 = self.D1_func(grade+1, index)
            result += result2

            return index, result
        else:
            return index, ''

    def T_func(self, grade, index):
        head_str = ''
        result = ''
        for i in range(grade):
            head_str += self.indent
        row_number, type, value = self.getNextToken(index)
        result2 = head_str + 'T (' + row_number + ')' + '\n'
        result += result2
        head_str += self.indent

        if type in ('char', 'int', 'float', 'boolean', 'string'):
            index, result2 = self.X_func(grade+1, index)
            result += result2
            index, result2 = self.C_func(grade+1, index)
            result += result2

            return index, result
        elif type == 'record':
            index += 1
            result2 = head_str + 'record (' + row_number + ')' + '\n'
            result += result2

            row_number, type, value = self.getNextToken(index)
            if type == ':':
                index += 1
                result2 = head_str + ': (' + row_number + ')' + '\n'
                result += result2
            else:
                index += 1
                self.Error_des(row_number, ':', type)
                errors = head_str + 'error: <' + type + ',' + value + '>' + '\t' + row_number
                result += errors
                return index, result

            row_number, type, value = self.getNextToken(index)
            if type == '{':
                index += 1
                result2 = head_str + '{ (' + row_number + ')' + '\n'
                result += result2
            else:
                index += 1
                self.Error_des(row_number, '{', type)
                errors = head_str + 'error: <' + type + ',' + value + '>' + '\t' + row_number
                result += errors
                return index, result

            index, result2 = self.D_func(grade+1, index)
            result += result2

            row_number, type, value = self.getNextToken(index)
            if type == '}':
                index += 1
                result2 = head_str + '} (' + row_number + ')' + '\n'
                result += result2
            else:
                index += 1
                self.Error_des(row_number, '}', type)
                errors = head_str + 'error: <' + type + ',' + value + '>' + '\t' + row_number
                result += errors
                return index, result

            return index, result

        else:
            index += 1
            self.Error_des(row_number, 'char, int, float, boolean, string, record', type)
            errors = head_str + 'error: <' + type + ',' + value + '>' + '\t' + row_number
            result += errors
            return index, result

    def X_func(self, grade, index):
        head_str = ''
        result = ''
        for i in range(grade):
            head_str += self.indent
        row_number, type, value = self.getNextToken(index)
        result2 = head_str + 'X (' + row_number + ')' + '\n'
        result += result2
        head_str += self.indent
        if type in ('char', 'int', 'float', 'boolean', 'string'):
            index += 1
            result2 = head_str + type + ' (' + row_number + ')' + '\n'
            result += result2
            return index, result
        else:
            index += 1
            self.Error_des(row_number, 'char, int, float, boolean, string', type)
            errors = head_str + 'error: <' + type + ',' + value + '>' + '\t' + row_number
            result += errors
            return index, result

    def C_func(self, grade, index):
        head_str = ''
        result = ''
        for i in range(grade):
            head_str += self.indent
        row_number, type, value = self.getNextToken(index)
        result2 = head_str + 'C (' + row_number + ')' + '\n'
        result += result2
        head_str += self.indent

        if type == '[':
            index += 1
            result2 = head_str + '[ (' + row_number + ')' + '\n'
            result += result2

            row_number, type, value = self.getNextToken(index)
            if type == 'CONST' and isinstance(eval(value), int) and eval(value) > 0:
                index += 1
                result2 = head_str + 'num: '+ value + '(' + row_number + ')' + '\n'
                result += result2
            else:
                index += 1
                self.Error_des(row_number, 'CONST', type)
                errors = head_str + 'error: <' + type + ',' + value + '>' + '\t' + row_number
                result += errors
                return index, result

            row_number, type, value = self.getNextToken(index)
            if type == ']':
                index += 1
                result2 = head_str + '] (' + row_number + ')' + '\n'
                result += result2
            else:
                index += 1
                self.Error_des(row_number, ']', type)
                errors = head_str + 'error: <' + type + ',' + value + '>' + '\t' + row_number
                result += errors
                return index, result

            index, result2 = self.C_func(grade+1, index)
            result += result2

            return index, result
        elif type == 'IDN':
            return index, ''
        else:
            index += 1
            self.Error_des(row_number, '[, IDN', type)
            errors = head_str + 'error: <' + type + ',' + value + '>' + '\t' + row_number
            result += errors
            return index, result

    def S_func(self, grade, index):
        '''
        当接收错误符号时返回空字符，即把错误字符当成终结符
        :param grade:
        :param index:
        :return:
        '''
        head_str = ''
        result = ''
        for i in range(grade):
            head_str += self.indent
        row_number, type, value = self.getNextToken(index)
        result2 = head_str + 'S (' + row_number + ')' + '\n'
        result += result2
        head_str += self.indent

        if type == 'IDN':
            index += 1
            result2 = head_str + 'id: ' + value + '(' + row_number + ')' + '\n'
            result += result2
            index, result2 = self.S1_func(grade+1, index)
            result += result2
            return index, result
        elif type == 'if':
            index += 1
            result2 = head_str + 'if (' + row_number + ')' + '\n'
            result += result2
            index, result2 = self.B_func(grade + 1, index)
            result += result2

            row_number, type, value = self.getNextToken(index)
            if type == 'then':
                index += 1
                result2 = head_str + 'then (' + row_number + ')' + '\n'
                result += result2
                index, result2 = self.S_func(grade + 1, index)
                result += result2
                index, result2 = self.S21_func(grade+1, index)
                result += result2
                return index, result
            else:
                index += 1
                self.Error_des(row_number, 'then', type)
                errors = head_str + 'error: <' + type + ',' + value + '>' + '\t' + row_number
                result += errors
                return index, result
        elif type == 'while':
            index += 1
            result2 = head_str + 'while (' + row_number + ')' + '\n'
            result += result2

            index, result2 = self.B_func(grade + 1, index)
            result += result2
            row_number, type, value = self.getNextToken(index)
            if type == 'do':
                index += 1
                result2 = head_str + 'do (' + row_number + ')' + '\n'
                result += result2
                index, result2 = self.S_func(grade + 1, index)
                result += result2
                return index, result
        elif type == 'call':
            index += 1
            result2 = head_str + type + ' (' + row_number + ')' + '\n'
            result += result2

            row_number, type, value = self.getNextToken(index)
            if type == 'IDN':
                index += 1
                result2 = head_str + type + ': ' + value + '(' + row_number + ')' + '\n'
                result += result2
            else:
                index += 1
                self.Error_des(row_number, 'IDN', type)
                errors = head_str + 'error: <' + type + ',' + value + '>' + '\t' + row_number
                result += errors
                return index, result

            row_number, type, value = self.getNextToken(index)
            if type == '(':
                index += 1
                result2 = head_str + type  + ' (' + row_number + ')' + '\n'
                result += result2
            else:
                index += 1
                self.Error_des(row_number, '(', type)
                errors = head_str + 'error: <' + type + ',' + value + '>' + '\t' + row_number
                result += errors
                return index, result

            index, result2 = self.Elist_func(grade+1, index)
            result += result2

            row_number, type, value = self.getNextToken(index)
            if type == ')':
                index += 1
                result2 = head_str + type + ' (' + row_number + ')' + '\n'
                result += result2
            else:
                index += 1
                self.Error_des(row_number, ')', type)
                errors = head_str + 'error: <' + type + ',' + value + '>' + '\t' + row_number
                result += errors
                return index, result
            return index, result
        else:
            return index, ''

    def S1_func(self, grade, index):
        head_str = ''
        result = ''
        for i in range(grade):
            head_str += self.indent
        row_number, type, value = self.getNextToken(index)
        result2 = head_str + 'S\' (' + row_number + ')' + '\n'
        result += result2
        head_str += self.indent

        if type == '=':
            index += 1
            result2 = head_str + '= (' + row_number + ')' + '\n'
            result += result2
            index, result2 = self.E_func(grade+1, index)
            result += result2

            row_number, type, value = self.getNextToken(index)
            if type == ';':
                index += 1
                result2 = head_str + '; (' + row_number + ')' + '\n'
                result += result2
            else:
                index += 1
                self.Error_des(row_number, ':', type)
                errors = head_str + 'error: <' + type + ',' + value + '>' + '\t' + row_number
                result += errors
                return index, result
            index, result2 = self.S_func(grade+1, index)
            result += result2
            return index, result
        elif type == '[':
            index += 1
            result2 = head_str + '[ (' + row_number + ')' + '\n'
            result += result2

            index, result2 = self.E_func(grade+1, index)
            result += result2

            row_number, type, value = self.getNextToken(index)
            if type == ']':
                index += 1
                result2 = head_str + '] (' + row_number + ')' + '\n'
                result += result2
            else:
                index += 1
                self.Error_des(row_number, ']', type)
                errors = head_str + 'error: <' + type + ',' + value + '>' + '\t' + row_number
                result += errors
                return index, result
            index, result2 = self.L1_func(grade+1, index)
            result += result2

            row_number, type, value = self.getNextToken(index)
            if type == '=':
                index += 1
                result2 = head_str + '= (' + row_number + ')' + '\n'
                result += result2
            else:
                index += 1
                self.Error_des(row_number, '=', type)
                errors = head_str + 'error: <' + type + ',' + value + '>' + '\t' + row_number
                result += errors
                return index, result
            index, result2 = self.E_func(grade+1, index)
            result += result2

            row_number, type, value = self.getNextToken(index)
            if type == ';':
                index += 1
                result2 = head_str + '; (' + row_number + ')' + '\n'
                result += result2
            else:
                index += 1
                self.Error_des(row_number, ':', type)
                errors = head_str + 'error: <' + type + ',' + value + '>' + '\t' + row_number
                result += errors
                return index, result
            index, result2 = self.S_func(grade + 1, index)
            result += result2
            return index, result

        else:
            index += 1
            self.Error_des(row_number, '=, [', type)
            errors = head_str + 'error: <' + type + ',' + value + '>' + '\t' + row_number
            result += errors
            return index, result

    def S21_func(self, grade, index):
        '''
        错误字符当做终结符
        :param grade:
        :param index:
        :return:
        '''
        head_str = ''
        result = ''
        for i in range(grade):
            head_str += self.indent
        row_number, type, value = self.getNextToken(index)

        result2 = head_str + '\'S\' (' + row_number + ')' + '\n'
        result += result2
        head_str += self.indent

        if type == 'else':
            index += 1
            result2 = head_str + 'else (' + row_number + ')' + '\n'
            result += result2
            index, result2 = self.S_func(grade+1, index)
            result += result2
            return index, result
        else:
            return index, ''

    def E_func(self, grade, index):
        head_str = ''
        result = ''
        for i in range(grade):
            head_str += self.indent
        row_number, type, value = self.getNextToken(index)
        result2 = head_str + 'E (' + row_number + ')' + '\n'
        result += result2
        head_str += self.indent

        if type == '-':
            index += 1
            result2 = head_str + '- (' + row_number + ')' + '\n'
            result += result2

            index, result2 = self.E_func(grade + 1, index)
            result += result2
            index, result2 = self.E1_func(grade + 1, index)
            result += result2
            return index, result
        elif type == '(':
            index += 1
            result2 = head_str + '( (' + row_number + ')' + '\n'
            result += result2

            index, result2 = self.E_func(grade + 1, index)
            result += result2

            row_number, type, value = self.getNextToken(index)
            if type == ')':
                index += 1
                result2 = head_str + ') (' + row_number + ')' + '\n'
                result += result2
            else:
                index += 1
                self.Error_des(row_number, ')', type)
                errors = head_str + 'error: <' + type + ',' + value + '>' + '\t' + row_number
                result += errors
                return index, result

            index, result2 = self.E1_func(grade + 1, index)
            result += result2
            return index, result
        elif type == 'CONST':
            index += 1
            result2 = head_str + 'const: ' + value + '(' + row_number + ')' + '\n'
            result += result2
            index, result2 = self.E1_func(grade+1, index)
            result += result2
            return index, result
        elif type == 'IDN':
            index += 1
            result2 = head_str + 'id: ' + value + '(' + row_number + ')' + '\n'
            result += result2
            index, result2 = self.E2_func(grade+1, index)
            result += result2
            return index, result
        else:
            index += 1
            self.Error_des(row_number, '-, (, CONST, IDN', type)
            errors = head_str + 'error: <' + type + ',' + value + '>' + '\t' + row_number
            result += errors
            return index, result

    def E2_func(self, grade, index):
        head_str = ''
        result = ''
        for i in range(grade):
            head_str += self.indent
        row_number, type, value = self.getNextToken(index)
        result2 = head_str + 'E\'\' (' + row_number + ')' + '\n'
        result += result2
        head_str += self.indent

        if type == '+':
            index += 1
            result2 = head_str + '+ (' + row_number + ')' + '\n'
            result += result2
            index, result2 = self.E_func(grade+1, index)
            result += result2
            index, result2 = self.E1_func(grade+1, index)
            result += result2
            return index, result
        elif type == '*':
            index += 1
            result2 = head_str + '* (' + row_number + ')' + '\n'
            result += result2
            index, result2 = self.E_func(grade + 1, index)
            result += result2
            index, result2 = self.E1_func(grade + 1, index)
            result += result2
            return index, result
        elif type == '-':
            index += 1
            result2 = head_str + '- (' + row_number + ')' + '\n'
            result += result2
            index, result2 = self.E_func(grade + 1, index)
            result += result2
            index, result2 = self.E1_func(grade + 1, index)
            result += result2
            return index, result
        elif type == '[':
            index += 1
            result2 = head_str + '[ (' + row_number + ')' + '\n'
            result += result2
            index, result2 = self.E_func(grade + 1, index)

            row_number, type, value = self.getNextToken(index)
            if type == ']':
                index += 1
                result2 = head_str + '[ (' + row_number + ')' + '\n'
                result += result2
            else:
                index += 1
                self.Error_des(row_number, ']', type)
                errors = head_str + 'error: <' + type + ',' + value + '>' + '\t' + row_number
                result += errors
                return index, result
            index, result2 = self.L1_func(grade+1, index)
            result += result2
            index, result2 = self.E1_func(grade+1, index)
            result += result2
            return index, result
        else:
            return index, ''

    def E1_func(self, grade, index):
        head_str = ''
        result = ''
        for i in range(grade):
            head_str += self.indent
        row_number, type, value = self.getNextToken(index)
        result2 = head_str + 'E\' (' + row_number + ')' + '\n'
        result += result2
        head_str += self.indent

        if type == '+':
            index += 1
            result2 = head_str + '+ (' + row_number + ')' + '\n'
            result += result2
            index, result2 = self.E_func(grade+1, index)
            result += result2
            index, result2 = self.E1_func(grade+1, index)
            result += result2
            return index, result
        elif type == '*':
            index += 1
            result2 = head_str + '* (' + row_number + ')' + '\n'
            result += result2
            index, result2 = self.E_func(grade + 1, index)
            result += result2
            index, result2 = self.E1_func(grade + 1, index)
            result += result2
            return index, result
        else:
            return index, ''

    def L_func(self, grade, index):
        head_str = ''
        result = ''
        for i in range(grade):
            head_str += self.indent
        row_number, type, value = self.getNextToken(index)
        result2 = head_str + 'L (' + row_number + ')' + '\n'
        result += result2
        head_str += self.indent

        if type == 'IDN':
            index += 1
            result2 = head_str + 'id: ' + value + '(' + row_number + ')' + '\n'
            result += result2

            row_number, type, value = self.getNextToken(index)
            if type == '[':
                index += 1
                result2 = head_str + '[ (' + row_number + ')' + '\n'
                result += result2
            else:
                index += 1
                self.Error_des(row_number, '[', type)
                errors = head_str + 'error: <' + type + ',' + value + '>' + '\t' + row_number
                result += errors
                return index, result
            index, result2 = self.E_func(grade+1, index)
            result += result2

            row_number, type, value = self.getNextToken(index)
            if type == ']':
                index += 1
                result2 = head_str + '] (' + row_number + ')' + '\n'
                result += result2
            else:
                index += 1
                self.Error_des(row_number, ']', type)
                errors = head_str + 'error: <' + type + ',' + value + '>' + '\t' + row_number
                result += errors
                return index, result
            index, result2 = self.L1_func(grade+1, index)
            result += result2
            return index, result
        else:
            index += 1
            self.Error_des(row_number, 'IDN', type)
            errors = head_str + 'error: <' + type + ',' + value + '>' + '\t' + row_number
            result += errors
            return index, result

    def L1_func(self, grade, index):
        '''
        当接收错误符号时返回空字符，即把错误字符当成终结符
        :param grade:
        :param index:
        :return:
        '''
        head_str = ''
        result = ''
        for i in range(grade):
            head_str += self.indent
        row_number, type, value = self.getNextToken(index)
        result2 = head_str + 'L\' (' + row_number + ')' + '\n'
        result += result2
        head_str += self.indent

        if type == '[':
            index += 1
            result2 = head_str + '[ (' + row_number + ')' + '\n'
            result += result2

            index, result2 = self.E_func(grade+1, index)
            result += result2

            row_number, type, value = self.getNextToken(index)
            if type == ']':
                index += 1
                result2 = head_str + '] (' + row_number + ')' + '\n'
                result += result2
            else:
                index += 1
                self.Error_des(row_number, ']', type)
                errors = head_str + 'error: <' + type + ',' + value + '>' + '\t' + row_number
                result += errors
                return index, result
            index, result2 = self.L1_func(grade+1, index)
            result += result2
            return index, result
        else:
            return index, ''

    def B_func(self, grade, index):
        head_str = ''
        result = ''
        for i in range(grade):
            head_str += self.indent
        row_number, type, value = self.getNextToken(index)
        result2 = head_str + 'B (' + row_number + ')' + '\n'
        result += result2
        head_str += self.indent

        if type == '!':
            index += 1
            result2 = head_str + '! (' + row_number + ')' + '\n'
            result += result2
            index, result2 = self.B_func(grade + 1, index)
            result += result2
            index, result2 = self.B1_func(grade+1, index)
            result += result2
            return index, result
        elif type == '(':
            index += 1
            result2 = head_str + '( (' + row_number + ')' + '\n'
            result += result2
            index, result2 = self.B_func(grade+1, index)
            result += result2

            row_number, type, value = self.getNextToken(index)
            if type == ')':
                index += 1
                result2 = head_str + ') (' + row_number + ')' + '\n'
                result += result2
            else:
                index += 1
                self.Error_des(row_number, ')', type)
                errors = head_str + 'error: <' + type + ',' + value + '>' + '\t' + row_number
                result += errors
                return index, result
            index, result2 = self.B1_func(grade+1, index)
            result += result2
            return index, result
        elif type in ('-', '(', 'IDN', 'CONST'):
            index, result2 = self.E_func(grade+1, index)
            result += result2
            row_number, type, value = self.getNextToken(index)
            if type in ('<', '<=', '==', '!=', '>', '>='):
                index += 1
                result2 = head_str + type + ' (' + row_number + ')' + '\n'
                result += result2
            else:
                index += 1
                self.Error_des(row_number, '<, <=, ==, !=, >, >=', type)
                errors = head_str + 'error: <' + type + ',' + value + '>' + '\t' + row_number
                result += errors
                return index, result
            index, result2 = self.E_func(grade+1, index)
            result += result2
            index, result2 = self.B1_func(grade+1, index)
            result += result2
            return index, result
        elif type == 'CONST' and value == '"true"':
            index += 1
            result2 = head_str + type + ': ' + value + '(' + row_number + ')' + '\n'
            result += result2
            index, result2 = self.B1_func(grade+1, index)
            result += result2
            return index, result
        elif type == 'CONST' and value == '"false"':
            index += 1
            result2 = head_str + type + ': ' + value + '(' + row_number + ')' + '\n'
            result += result2
            index, result2 = self.B1_func(grade+1, index)
        else:
            index += 1
            self.Error_des(row_number, '!, (, -, IDN, CONST', type)
            errors = head_str + 'error: <' + type + ',' + value + '>' + '\t' + row_number
            result += errors
            return index, result

    def B1_func(self, grade, index):
        '''
        错误字符当终结符
        :param grade:
        :param index:
        :return:
        '''
        head_str = ''
        result = ''
        for i in range(grade):
            head_str += self.indent
        row_number, type, value = self.getNextToken(index)
        result2 = head_str + 'B\' (' + row_number + ')' + '\n'
        result += result2
        head_str += self.indent

        if type == '||':
            index += 1
            result2 = head_str + type + ' (' + row_number + ')' + '\n'
            result += result2
            index, result2 = self.B_func(grade+1, index)
            result += result2
            index, result2 = self.B1_func(grade+1, index)
            result += result2
            return index, result
        elif type == '&&':
            index += 1
            result2 = head_str + type + ' (' + row_number + ')' + '\n'
            result += result2
            index, result2 = self.B_func(grade + 1, index)
            result += result2
            index, result2 = self.B1_func(grade + 1, index)
            result += result2
            return index, result
        else:
            return index, ''

    def Elist_func(self, grade, index):
        head_str = ''
        result = ''
        for i in range(grade):
            head_str += self.indent
        row_number, type, value = self.getNextToken(index)
        result2 = head_str + 'Elist (' + row_number + ')' + '\n'
        result += result2
        head_str += self.indent

        if type in ('-', '(', 'IDN', 'CONST'):
            index, result2 = self.E_func(grade + 1, index)
            result += result2
            index, result2 = self.Elist1_func(grade + 1, index)
            result += result2
            return index, result
        else:
            return index, ''

    def Elist1_func(self, grade, index):
        '''
        把错误字符当终结符
        :param grade:
        :param index:
        :return:
        '''
        head_str = ''
        result = ''
        for i in range(grade):
            head_str += self.indent
        row_number, type, value = self.getNextToken(index)
        result2 = head_str + 'Elist\' (' + row_number + ')' + '\n'
        result += result2
        head_str += self.indent

        if type == ',':
            index += 1
            result2 = head_str + type + ' (' + row_number + ')' + '\n'
            result += result2
            index, result2 = self.E_func(grade+1, index)
            result += result2
            index, result2 = self.Elist1_func(grade+1, index)
            result += result2
            return index, result

        else:
            return index, ''

    def Error_des(self, row_number, expect_value, real_value):
        des = "此处期望'" + expect_value + "'，但实际出现'" + real_value + "'，处理方法：文法读取终止"
        error_des = "Error at Line [" + str(row_number) + "]: [" + des + "]"
        print(error_des)
