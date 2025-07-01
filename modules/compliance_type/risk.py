class RiskCompliance:
    def __init__(self, risk_factors):
        self.risk_factors = risk_factors

    def evaluate(self, context):
        # Dummy risk calculation: boolean factors to risk score
        score = sum(1 for factor in self.risk_factors if context.get(factor, False))
        return {"risk_score": score}
