from PyQt4 import QtGui,QtCore
import sys
from lexer.Lexer import Lexer
from parse.Parser import Parser
from semantic.Semantic import Semantic

class DFATable(QtGui.QTableWidget):
    def __init__(self, title):
        super(DFATable, self).__init__()
        self.setWindowTitle(title)
        self.resize(700, 600)


    def table(self, row, column, content):
        # 设置表格行列数
        self.setColumnCount(len(row))
        self.setRowCount(len(column))

        # 设置表头
        self.setHorizontalHeaderLabels(row)
        self.setVerticalHeaderLabels(column)

        # 添加内容
        for x in range(len(content)):
            for y in range(len(content[x])):
                self.setItem(x, y, QtGui.QTableWidgetItem(content[x][y]))

class TokenWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(TokenWidget, self).__init__(parent)

        # set window's location and size
        self.setWindowTitle("tokens")
        self.resize(600, 700)
        self.center()

        self.textEdit = QtGui.QTextEdit(self)
        self.textEdit.setGeometry(10,10,580, 680)

    # 窗口居中
    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)

class ParseWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(ParseWidget, self).__init__(parent)

        # set window's location and size
        self.setWindowTitle("parse")
        self.resize(800, 700)
        self.center()

        self.textEdit = QtGui.QTextEdit(self)
        self.textEdit.setGeometry(10,10,780, 680)

    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

class SemanticWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(SemanticWidget, self).__init__(parent)

        # set window's location and size
        self.setWindowTitle("semantic")
        self.resize(800, 700)
        self.center()

        self.textEdit = QtGui.QTextEdit(self)
        self.textEdit.setGeometry(10,10,780, 680)

    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)


class CompilerWindow(QtGui.QMainWindow):
    def __init__(self):
        super(CompilerWindow, self).__init__()
        self.tokens_widget = TokenWidget()
        self.parse_widget = ParseWidget()
        self.semantic_widget = SemanticWidget()
        self.dfa_table_widget = DFATable("DFA转换表")
        self.l = Lexer()
        self.p = Parser()
        self.s = Semantic()
        self.initUI()

    def initUI(self):
        self.resize(750, 800)
        self.setWindowTitle("语义分析")

        # exit toolbar
        self.exit = QtGui.QAction('Exit', self)
        self.exit.setShortcut('Ctrl+Q')
        self.exit.setStatusTip("Exit application")
        self.connect(self.exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT("close()"))

        # open file toolbar
        self.openfile = QtGui.QAction('打开文件', self)
        self.openfile.setShortcut('Ctrl+O')
        self.openfile.setStatusTip("Open file")
        self.connect(self.openfile, QtCore.SIGNAL('triggered()'), self.open_file)

        # lexer toolbar
        self.lexer = QtGui.QAction('词法分析', self)
        self.lexer.setShortcut('Ctrl+L')
        self.lexer.setStatusTip("lexer")
        self.connect(self.lexer, QtCore.SIGNAL('triggered()'), self.lexer_ana)

        # DFA toolbar
        self.dfa_table = QtGui.QAction('DFA转换表', self)
        self.dfa_table.setShortcut('Ctrl+D')
        self.connect(self.dfa_table, QtCore.SIGNAL('triggered()'), self.show_dfa_table)

        #parser toolbar
        self.parser = QtGui.QAction('语法分析', self)
        self.parser.setShortcut('Ctrl+P')
        self.parser.setStatusTip("parser")
        self.connect(self.parser, QtCore.SIGNAL('triggered()'), self.parser_ana)

        #semantic toolbar
        self.semantic = QtGui.QAction('语义分析', self)
        self.semantic.setShortcut('Ctrl+M')
        self.semantic.setStatusTip("semantic")
        self.connect(self.semantic, QtCore.SIGNAL('triggered()'), self.semantic_ana)

        #clear toolbar
        self.clear = QtGui.QAction('清空', self)
        self.clear.setShortcut('Ctrl+A')
        self.clear.setStatusTip("clear")
        self.connect(self.clear, QtCore.SIGNAL('triggered()'), self.clear_data)

        # add toolbar
        self.toolbar1 = self.addToolBar("打开文件")
        self.toolbar3 = self.addToolBar("词法分析")
        self.toolbar4 = self.addToolBar("DFA转换表")
        self.toolbar5 = self.addToolBar("语法分析")
        self.toolbar6 = self.addToolBar("语义分析")
        self.toolbar7 = self.addToolBar("清空")
        self.toolbar1.addAction(self.openfile)
        self.toolbar3.addAction(self.lexer)
        self.toolbar4.addAction(self.dfa_table)
        self.toolbar5.addAction(self.parser)
        self.toolbar6.addAction(self.semantic)
        self.toolbar7.addAction(self.clear)

        # add status bar
        self.statusBar().showMessage('Ready')

        # 中央文本框
        self.textEdit = QtGui.QTextEdit()
        #默认加载文件
        fname = open('声明语句.txt', 'r')
        data = fname.read()
        self.textEdit.setText(data)
        self.setCentralWidget(self.textEdit)
        self.setFocus()


    def open_file(self):
        # 文件选择器
        filename = QtGui.QFileDialog.getOpenFileName(self, "Open file", '.')
        if not filename == '':
            print("open" + filename)
            fname = open(filename, 'r')
            data = fname.read()
            self.textEdit.setText(data)

    def lexer_ana(self):
        # 获取文本框内容
        data = self.textEdit.toPlainText()

        tokens = self.l.lex(data)
        tokens_str = '行数\ttoken\n'
        for t in tokens:
            tokens_str += t + "\n"
        self.tokens_widget.textEdit.setText(tokens_str)
        self.tokens_widget.show()

    def parser_ana(self):
        data = self.textEdit.toPlainText()
        tokens = self.l.lex(data)
        parse_result = self.p.analyze(tokens)
        self.parse_widget.setWindowTitle("语法分析树")
        self.parse_widget.textEdit.setText(parse_result)
        self.parse_widget.show()

    def semantic_ana(self):
        data = self.textEdit.toPlainText()
        tokens = self.l.lex(data)
        parse_result = self.p.analyze(tokens)
        semantic_result = self.s.analyze(parse_result)
        self.semantic_widget.setWindowTitle("语义分析")
        self.semantic_widget.textEdit.setText(semantic_result)
        self.semantic_widget.show()

    def show_dfa_table(self):
        states, chars, t_content = self.l.dfa.get_dfa_table()
        self.dfa_table_widget.table(chars, states, t_content)
        self.dfa_table_widget.show()

    def clear_data(self):
        self.textEdit.setText("")

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    window = CompilerWindow()
    window.show()

    sys.exit(app.exec_())