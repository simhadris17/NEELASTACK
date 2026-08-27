class EvaluationRunner:
    def run(self, cases, fn):
        return [{"input": c, "output": fn(c)} for c in cases]
