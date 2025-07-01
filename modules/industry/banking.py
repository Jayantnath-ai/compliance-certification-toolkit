class BankingIndustry:
    def __init__(self):
        self.forks = [
            {"condition": "context.get('onboarding_consent')", "description": "Consent obtained"},
            {"condition": "context.get('data_minimization')", "description": "Data minimized"}
        ]
