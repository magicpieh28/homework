class CollinsSpan:
	def __init__(self, i, j, h, score):
		self.i = i
		self.j = j
		self.h = h
		self.score = score

	def __str__(self):
		return "(%s, %s, %s, %s)" % (self.i, self.j, self.h, self.score)

class CollinsParser:
	def __init__(self):
		self.chart = None

	def parse(self, words: list):
		self.initSpans(words)

		# merge spans in a bottom-up manner
		pair = {}
		for l in range(1, len(words)+1):
			for i in range(0, len(words)):
				j = i + l
				if j > len(words): break
				for k in range(i+1, j):
					# print(f"k => {k}")
					for h_l in range(i, k):
						for h_r in range(k, j):
							# merge spans
							span_l = self.chart[i][k][h_l]
							span_r = self.chart[k][j][h_r]

							# left -> right
							l_score = self.getScore(words, span_l, span_r)
							span = CollinsSpan(i, j, h_l, l_score)
							h, score = self.addSpan(span)
							pair[h] = score

							# right -> left
							r_score = self.getScore(words, span_r, span_l)
							span = CollinsSpan(i, j, h_r, r_score)
							h, score = self.addSpan(span)
							pair[h] = score

		self.pair = pair
		return print(self.findBest(0, len(words)))

	def initSpans(self, words):
		# initialize chart as 3-dimensional list
		length = len(words) + 1
		chart = []
		for i in range(length):
			chart.append([])
			for j in range(length):
				chart[i].append([None] * length)
		self.chart = chart
		# print(f"self.chart => {self.chart}")

		# add 1-length spans to the chart
		for i in range(0, len(words)):
			span = CollinsSpan(i, i+1, i, 0.0)
			self.addSpan(span)

	def addSpan(self, new_span):
		i, j, h = new_span.i, new_span.j, new_span.h
		old_span = self.chart[i][j][h]
		if old_span is None or old_span.score < new_span.score:
			# update chart
			self.chart[i][j][h] = new_span
		return h, new_span.score

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

	def print_head(self, words):
		heads = [None] * len(words)
		scores = [score for score in self.pair.values()]
		best_span = self.findBest(0, len(words))
		for idx in range(0, len(words)):
			if best_span.h != idx:
				try:
					head = words[scores.index(max(scores[idx+1:]))]
					heads[idx] = head
				except ValueError:
					head = words[best_span.h]
					heads[idx] = head
		return print(heads)


p = CollinsParser()

words = ["She", "read", "a", "short", "novel"]
p.parse(words)
p.print_head(words)