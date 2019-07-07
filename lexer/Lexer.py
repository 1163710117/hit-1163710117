# -*- coding: utf-8 -*-
import re

import DFA


class Lexer():
    def __init__(self):
        self.dfa = DFA.DFA()
        self.keywords = ['char', 'int', 'float', 'boolean', 'record', 'if', 'then', 'else', 'do', 'while',
                         'proc', 'call', 'return', 'string']

    def word_analyze(self, s1, t, line_num):
        ret_token_str = str(line_num) + '\t' + t + "\t"
        if s1 in [1, 2, 4, 5, 29]:
            ret_token_str += "<CONST," + t + ">"
        elif s1 == 3:
            ret_token_str += "error: unfinished HEX"

        elif s1 == 6:
            if t in self.keywords:
                ret_token_str += "<" + t + ", _ >"
            else:
                ret_token_str += "<IDN," + t + ">"
        elif s1 in [11, 12, 13, 14, 15, 16, 17, 22]:
            ret_token_str += "<" + t + ", _ >"
        elif s1 in [25, 26]:
            ret_token_str = str(line_num) + '\t' + "/**/\t" + "<NOTE," + t + ">"
        elif s1 in [18, 21, 33]:
            ret_token_str += "<CONST," + t + ">"
        elif s1 == 30:
            ret_token_str += 'wrong OCT or HEX: ' + t
        else:
            ret_token_str += 'error: ' + t
        return ret_token_str

    def analyze(self, word, func="word_anylyze"):
        '''
        :param word: 待分析内容
        :return: token序列
        '''
        # 构造token属性值
        func = getattr(self, func)

        token = ''
        s = 0
        i = 0
        line_idx = 1
        tokens = []
        while i<len(word):
            c = word[i]
            s = self.dfa.move(s, c)
            if re.match('\n', c):
                line_idx += 1
            if re.match('\s', c) == None:
                token += c
            elif s in [23, 24, 26]:
                if s == 26 and re.match('\n', c) == None:
                    token += c
                else:
                    token += c
            if i < len(word)-1:
                c_next = word[i + 1]
                s_next = self.dfa.move(s, c_next)
                if s != 0 and s_next == 0:
                    tokens.append(func(s, token, line_idx))
                    token = ''
                    s = 0
            else:
                tokens.append(func(s, token, line_idx))
            i = i+1
        return tokens

    def lex(self, content):
        tokens = self.analyze(content, func="word_analyze")
        return tokens