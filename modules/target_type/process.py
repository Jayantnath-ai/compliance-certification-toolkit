class ProcessTarget:
    def __init__(self, name):
        self.name = name

    def get_context(self):
        # Return process-specific context (mock)
        return {"onboarding_consent": True, "data_minimization": True}
