def timer(func):
	import time
	from functools import wraps

	@wraps(func)
	def func_timer(*args, **kwagrs):
		t1 = time.time()
		func(*args, **kwagrs)
		t2 = time.time()
		print('{} used {} seconds'.format(func.__name__, t2 - t1))
	return func_timer

class Employee():

    increase_rate = 1.05

    def __init__(self, first, last, salary):
        self.first = first
        self.last = last
        self.salary = salary
        # self.email = self.first + '.' + self.last + '@company'

    def increase_salary(self):
    	return self.salary * self.increase_rate
    
    @property
    def email(self):
    	return self.first + '.' + self.last + '@company.com'
    
    @property
    def full_name(self):
        return self.first + ' ' + self.last

    @full_name.setter
    def full_name(self, name):
    	self.first, self.last = str(name).split()
    	# print(self.first, self.last)
    @full_name.deleter
    def full_name(self):
    	self.first, self.last = None, None
    	print('Deleted')

    def __repr__(self):
        return '%s(%r)' % (self.__class__, self.__dict__)

    def __add__(self, other):
    	return self.salary + other.salary

    # def __str__(self):
    # 	return str(self.__class__)

class Developer(Employee):
	
	increase_rate = 1.10

	def __init__(self, first, last, salary, program_language):
		super().__init__(first, last, salary)
		self.program_language = program_language

class Manager(Employee):

	def __init__(self, first, last, salary, supervisor):
		super().__init__(first, last, salary)
		self.supervisor = [supervisor]

	def add_supervisor(self, emp):
		if emp not in self.supervisor:
			self.supervisor.append(emp)
		else:
			return('%s already exist' % emp.full_name)

	def del_suppervisor(self, emp):
		if emp in self.supervisor:
			self.supervisor.remove(emp)
		else:
			return('%s not exist' % emp.full_name)

	def get_suppervisor(self):
		if self.supervisor != []:
			for emp in self.supervisor:
				print('--> %s' % emp.full_name)
		else:
			print('There is no employees under %s currently' % self.full_name)

em1 = Employee('Joe', 'Wu', 100000)
em2 = Developer('Zhe', 'Wang', 80000, 'Python')
em3 = Manager('Ryan', 'Wang', 300000, em2)
em1.increase_rate = 2

# print(em1 + em2)
# print(em1.__dict__)
# print(em1.increase_salary())
# print(em2.increase_salary())
# print(em2.program_language)
# print(em1.__dict__)
# print(em1.full_name, em1.email, em1.salary)
# print(em1.first, em1.last, em1.email)
# del em1.full_name





# @timer
def main():
	import signal
	import sys

	em3.add_supervisor(em1)
	# em3.del_suppervisor(em2)
	def signal_handler(signal, frame):
		print('You pressed Ctrl+C!')
		sys.exit(0)

	signal.signal(signal.SIGINT, signal_handler)
	print('Press Ctrl+C')
	signal.pause()

	em3.get_suppervisor()
	for i in range(10000):
		pass

main()