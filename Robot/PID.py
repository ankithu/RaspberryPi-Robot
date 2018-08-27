
class PID:
	def init(self, set, p, i , d):
		self.error = 0.0
		self.last = 0.0
		self.sum = 0.0
		self.p = p
		self.i = i
		self.d = d
		self.set = set
	def calculate(self, val):
		self.error = self.set - val
		self.sum = self.sum + self.error
		pTerm = self.p * self.error
		dTerm = self.d * self.last
		iTerm = self.i * self.sum
		self.last = self.error
		result = pTerm + iTerm + dTerm
		return result






