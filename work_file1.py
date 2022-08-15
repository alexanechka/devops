# Для тренировки и закрепления материала требуется на любом императивном языке, поддерживающем структурную парадигму
# программирования (С, Python, JS, Go, Rust, Pascal), написать консольную программу вычисления значения произвольного
# математического выражения, содержащего следующие операции:
#
# + Унарный плюс (Пример: +5)
# - Унарный минус (Пример: -2)
# + Сложение (Пример: 3 + 6)
# - Вычитание (Пример: 1 - 4)
# ***** Умножение (Пример: 2 * 3)
# / Деление (Пример: 5 / 2)
# ( ) Скобки (Пример: 1 - (5 + 2))
# Для решения этой задачи требуется воспользоваться обратной польской записью, а главное — программа должна выполняться
# в структурном стиле. Нужно, чтобы все алгоритмы и структуры данных (стек, очередь и другое) реализовывались
# самостоятельно. Кроме самого числового результата нужно вывести на экран выражение, составленное в обратной польской
# записи. Ниже представлен пример работы программы.
# Ввод:
# (1 + 2) * 4 + 3
#
# Вывод:
# 1 2 + 4 × 3 +
# 15
#
# Для преобразования выражений из классической в обратную польскую нотацию необходимо использовать
# алгоритм Дейкстры "Сортировочная станция"
#
# Разработать калькулятор с функционалом, аналогичным программе из задания ко второму семинару,
# но в объектно-ориентированном стиле.
# Теперь нужно разбирать строку полностью, а не считать, что лексемы обязательно разделены пробелами

# мои примеры 1+3--5+(1+3)*6

import operator


# добавление в стек в зависимости от типа
def add_to_stack(stack_pr, el):
    if type(el) == list:
        for el_ls in el:
            if el_ls != '':
                stack_pr.append(el_ls)
    elif el != '':
        stack_pr.append(el)


# получение строки обратной польской записи из списка
def get_dijkstra_list(dijkstra):
    ds_ls = []
    if type(dijkstra) == list:
        ds_ls = dijkstra
    else:
        prev_str = ''
        for sym in dijkstra:
            if sym == ' ':
                add_to_stack(ds_ls, prev_str)
                prev_str = ''
            else:
                prev_str = prev_str + sym
        add_to_stack(ds_ls, prev_str)
    return ds_ls


class Calculator:
    def __init__(self, dijkstra):
        self.result = 0
        self.operators = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv
        }
        self.result_count(dijkstra)

    def __str__(self):
        return str(self.result)

    def result_count(self, dijkstra):
        operators = self.operators
        stack = []

        dijkstra_ls = get_dijkstra_list(dijkstra)

        lst_to_count = dijkstra_ls.copy()
        str_to_count = dijkstra_ls.copy()
        for sym in str_to_count:
            if sym == '':
                continue
            elif sym[0].isdigit():
                stack.append(sym)
                lst_to_count.remove(sym)
            else:
                if len(stack) < 2:
                    continue
                nb1, nb2 = stack.pop(), stack.pop()
                stack.append(operators[sym](float(nb2), float(nb1)))
                lst_to_count.remove(sym)

        if len(stack) != 0:
            self.result = stack.pop()


class DijkstraString:
    def __init__(self, user_str_to_change):
        self._symbols = ['(', '+', '-', '*', '/', ')', '.', ',']
        self._brackets = ['(', ')']
        self._num_separators = ['.', ',']
        self._operators = ['+', '-', '*', '/']
        self._priorities = {
            '(': 1,
            '+': 2,
            '-': 2,
            '*': 3,
            '/': 3,
            ')': 4,
            '!': 0
        }
        self.result = 0
        self.dijkstra = []
        self.new_lst_to_change = []
        self.change_string_to_format(user_str_to_change)
        self.dijkstra_format()
        self.dijkstra_str = " ".join(self.dijkstra)

    def change_string_to_format(self, user_str_to_change):
        prev_sym = ''
        symbols = self._symbols
        add_bracket = False
        new_lst_to_change = []

        for sym_st in user_str_to_change:
            # убираем повтор разделителей дробной части
            if sym_st in self._num_separators and prev_sym in self._num_separators:
                continue
            # добавление символов в дробную часть числа без перехода к след. элементу
            elif not sym_st.isdigit() and prev_sym == '.':
                new_lst_to_change[-1] = new_lst_to_change[-1] + '0'
                prev_sym = '0'
            # закрывающая скобка при унарном минусе без перехода к след. элементу
            elif add_bracket and (sym_st in self._brackets or sym_st in self._operators):
                new_lst_to_change.append(')')
                prev_sym = ')'
                add_bracket = False

            # пропуск ненужных символов
            if not sym_st.isdigit() and sym_st not in symbols and sym_st != ' ':
                continue
            # добавление нового числа
            elif sym_st.isdigit() and not prev_sym.isdigit() and prev_sym not in self._num_separators:
                new_lst_to_change.append(sym_st)
                prev_sym = sym_st
            # добавление символа в число
            elif sym_st.isdigit() and (prev_sym.isdigit() or prev_sym in self._num_separators):
                new_lst_to_change[-1] = new_lst_to_change[-1] + sym_st
                prev_sym = sym_st
            # добавление разделителя в число
            elif sym_st in self._num_separators and prev_sym.isdigit():
                new_lst_to_change[-1] = new_lst_to_change[-1] + '.'
                prev_sym = '.'
            # унарный плюс
            elif sym_st == '+' and not prev_sym.isdigit() and prev_sym != ')':
                continue
            # унарный минус
            elif sym_st == '-' and not prev_sym.isdigit() and prev_sym != ')':
                new_lst_to_change.append('(')
                new_lst_to_change.append('0')
                new_lst_to_change.append('-')
                add_bracket = True
                prev_sym = sym_st
            # добавление оператора
            elif sym_st in self._operators and (prev_sym.isdigit() or prev_sym == ')'):
                new_lst_to_change.append(sym_st)
                prev_sym = sym_st
            # добавление скобки '('
            elif sym_st == '(' and (prev_sym in self._operators or prev_sym == '' or prev_sym == '('):
                new_lst_to_change.append(sym_st)
                prev_sym = sym_st
            # добавление скобки ')'
            elif sym_st == ')' and (prev_sym.isdigit() or prev_sym == ')'):
                new_lst_to_change.append(sym_st)
                prev_sym = sym_st

        self.new_lst_to_change = new_lst_to_change

    def get_formatted_data(self):
        return self.new_lst_to_change

    # вывод выражения в обратной польской записи
    def __str__(self):
        return self.dijkstra_str

    # Разбор строки
    def dijkstra_format(self):
        priorities = self._priorities
        stack = []
        dijkstra_lst = []

        for el in self.new_lst_to_change:
            if el[0].isdigit():
                add_to_stack(dijkstra_lst, el)
            elif el in priorities.keys():
                if el == '(' or len(stack) == 0:
                    add_to_stack(stack, el)
                elif el == ')':
                    el_from_stack = self.info_from_stack(stack, el, 1)
                    add_to_stack(dijkstra_lst, el_from_stack)
                else:
                    el_from_stack = self.info_from_stack(stack, el)
                    add_to_stack(dijkstra_lst, el_from_stack)
            else:
                continue

        add_to_stack(dijkstra_lst, self.info_from_stack(stack, '!'))
        self.dijkstra = dijkstra_lst

    # Преобразование строки в обратную польскую запись
    def info_from_stack(self, stack, sym_func, priority_to_stop=0):

        stack_ls = []
        n = len(stack)
        sym_to_stack = ''
        priorities = self._priorities

        while n > 0:
            last_sym = stack[-1]
            last_sym_priority = priorities.get(last_sym)
            sym_priority = priorities.get(sym_func)

            if last_sym_priority == priority_to_stop:
                stack.pop()
                return stack_ls
            elif sym_priority == 4:
                sym_to_print = stack.pop()
                if sym_to_print in ['(', ')']:
                    sym_to_print = ''
            elif sym_priority > last_sym_priority:
                add_to_stack(stack, sym_func)
                return stack_ls
            else:
                sym_to_stack = sym_func
                sym_to_print = stack.pop()
                if sym_to_print in ['(', ')']:
                    sym_to_print = ''

            add_to_stack(stack_ls, sym_to_print)

            n = len(stack)

        add_to_stack(stack, sym_to_stack)

        return stack_ls


# Ввод строки пользователем
user_str = input('Введите выражение для преобразования: ')
print(user_str)

ds = DijkstraString(user_str)
print(ds.get_formatted_data())
print(ds)

culc = Calculator(ds.dijkstra_str)
print(culc)
