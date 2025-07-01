class ForkEvaluator:
    """
    Generates compliance decision paths (forks) based on context.
    """
    def __init__(self, forks):
        # forks: list of dicts with 'condition' and 'description'
        self.forks = forks

    def evaluate_forks(self, context):
        results = {}
        for fork in self.forks:
            cond = fork.get("condition")
            desc = fork.get("description")
            outcome = eval(cond, {}, context)
            results[desc] = outcome
        return results
