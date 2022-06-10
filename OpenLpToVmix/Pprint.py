import win32api
import win32print

def win_print(filename, printer_name = None):
    if not printer_name:
        printer_name = win32print.GetDefaultPrinter()
    out = '/d:"%s"' % (printer_name)
    win32api.ShellExecute(0, "print", filename, out, ".", 0)


def test_print():
    win_print('nopol.txt')
    
    ##win_print('test.txt', 'PDFCreator')


if __name__ == '__main__':
    test_print()
