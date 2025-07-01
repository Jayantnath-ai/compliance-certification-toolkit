class SystemTarget:
    def __init__(self, name):
        self.name = name

    def get_context(self):
        # Return system-specific context (mock)
        return {"automated_profiling": False, "ephemeral_data_storage": True}
