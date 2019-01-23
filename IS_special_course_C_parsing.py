class CollinsSpan:
	def __init__(self, i, j, h, score):
		self.i = i
		self.j = j
		self.h = h
		self.score = score

	def span(self):
		return self.i, self.j, self.h, self.score

class CollinsParser:
	def __init__(self):
		self.chart = None

	def parse(self, words: list):
		self.initSpans(words)

		# merge spans in a bottom-up manner
		for l in range(1, len(words)+1):
			for i in range(0, len(words)):
				print(f"i => {i}")
				j = i + l
				print(f"j => {j}")
				if j > len(words): break
				for k in range(i+1, j):
					print(f"k => {k}")
					for h_l in range(i, k):
						print(f"h_l => {h_l}")
						for h_r in range(k, j):
							print(f"h_r => {h_r}")
							# merge spans
							span_l = self.chart[i][k][h_l]
							print(f"span_l => {span_l.__dict__}")
							span_r = self.chart[k][j][h_r]
							print(f"span_r => {span_r.__dict__}")

							# left -> right
							score = self.getScore(words, span_l, span_r)
							span = CollinsSpan(i, j, h_l, score)
							self.addSpan(span)

							# right -> left
							score = self.getScore(words, span_r, span_l)
							span = CollinsSpan(i, j, h_r, score)
							self.addSpan(span)

	def initSpans(self, words):
		# initialize chart as 3-dimensional list
		length = len(words) + 1
		chart = []
		for i in range(length):
			chart.append([])
			for j in range(length):
				chart[i].append([words[j-1]] * length)
		self.chart = chart
		print(f"self.chart => {self.chart}")
		print(f"chart[0][1][0] => {chart[0][1][0]}")

		# add 1-length spans to the chart
		for i in range(0, len(words)):
			span = CollinsSpan(i, i+1, i, 0.0)
			print(f"span in initSpan => {span.__dict__}")
			self.addSpan(span)

	def addSpan(self, new_span):
		print(f"new_span => {new_span.__dict__}")
		i, j, h = new_span.i, new_span.j, new_span.h
		old_span = self.chart[i][j][h]
		if old_span is None or old_span.score < new_span.score:
			# update chart
			self.chart[i][j][h] = new_span

	def getScore(self, words, head, dep):
		# currently, use naive scoring function
		h_word = words[head.h]
		if h_word == "read":
			score = 1.0
		elif h_word == "novel":
			score = 1.0
		else:
			score = 0.1

		# calculate score based on arc-factored model
		return head.score + dep.score + score

	def findBest(self, i, j):
		best_span = None
		for h in range(i, j):
			span = self.chart[i][j][h]
			if best_span is None or best_span.score < span.score:
				best_span = span
		return best_span

p = CollinsParser()

result = p.parse(["She", "read", "a", "short", "novel"])
print(result)