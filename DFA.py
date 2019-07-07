# -*- coding: utf-8 -*-
import re

#######改改改改改改改改
class DFA():
    d0_9 = "[0-9]"
    d1_9 = "[1-9]"
    d0_7 = "[0-7]"
    d0_9a_f = "[0-9a-f]"

    def __init__(self):
        self.conv_table = {
            0: {'0': 2, '[1-9]': 1, "[a-zA-Z_]": 6, "[=!<>*%+-]": 12,
                "[\(\)\[\];,:{}]": 11, "/": 22, "&": 16, "\|": 14, "\"": 28, "'": 31, "[\s]": 0, ".": 30},
            # NUM tokens
            1: {'[0-9]': 1, "\.": 27, "[eE]": 19},
            2: {'x': 3, '[0-7]': 4, "\.": 27, "[8-9]": 30},
            3: {'[0-9a-f]': 5, "[g-z]": 30},
            4: {'[0-7]': 4, "[8-9]": 30},
            5: {'[0-9a-f]': 5, "[g-z]": 30},
            # IDF tokens
            6: {"[a-zA-Z_0-9]": 6},
            # boundary
            11: {},
            # operation
            12: {"=": 13},
            13: {},
            14: {"\|": 15},
            15: {},
            16: {"&": 17},
            17: {},

            # scientific number
            18: {"[0-9]": 18, "[eE]": 19},
            19: {"[0-9]": 21, "[\+-]": 20},
            20: {"[0-9]": 21},
            21: {"[0-9]": 21},
            27: {"[0-9]": 18},
            # note
            22: {"\*": 23, "/": 26, "=":13},
            23: {"[^\*]": 23, "\*": 24},
            24: {"[^\*/]": 23, "\*": 24, "/": 25},
            25: {},
            26: {"[^\\n]": 26},

            # string const
            28: {"\"": 29, "[^\"\\n]": 28},
            29: {},

            # char const
            31: {"[^'\\n]": 32,},
            32: {"'": 33},
            33: {},
            # error handler
            30: {},

        }
        #######改改改改改改改改
        self.dfa_end_status = [1, 2, 4, 5, 6, 12, 13, 14, 15, 16, 17, 18, 21, 22, 25, 26, 29, 30, 33]

    #######改改改改改改改改
    def get_dfa_table(self):
        states = [str(s) for s in list(self.conv_table.keys())]
        chars = set()
        for s, v in self.conv_table.items():
            for k, vv in v.items():
                chars.add(k)

        chars = list(chars)
        t_content = [['']*len(chars) for i in range(len(states))]

        for s, v in self.conv_table.items():
            for k, vv in v.items():
                x = states.index(str(s))
                y = chars.index(k)
                if vv in self.dfa_end_status:
                    vv = str(vv) + '(end state)'
                    t_content[x][y] = vv
                else:
                    t_content[x][y] = str(vv)

        return states, chars, t_content

    def move(self, s, c):
        if s in self.conv_table :
            table = self.conv_table[s]
            for p, s_to in table.items():
                if re.match(p, c) != None:
                    return s_to
            return 0

    def init_table(self, data):
        '''
        用于从文件读取DFA转化表后的初始化
        :param data: DFA转换表的字符串形式
        :return:
        '''
        pass