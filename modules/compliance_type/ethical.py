class EthicalCompliance:
    def __init__(self, rules):
        self.rules = rules

    def evaluate(self, context):
        # Dummy ethical evaluation
        return {rule: context.get(rule, False) for rule in self.rules}
