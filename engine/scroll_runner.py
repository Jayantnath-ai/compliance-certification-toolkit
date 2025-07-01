import yaml

class ScrollRunner:
    """
    Loads and executes YAML scrolls (policy rules) against a context.
    """
    def __init__(self, scroll_paths):
        self.scroll_paths = scroll_paths
        self.scrolls = [yaml.safe_load(open(p)) for p in scroll_paths]

    def run_scrolls(self, context):
        results = {}
        for scroll in self.scrolls:
            key = scroll.get("title", scroll.get("section", "unknown"))
            # Simple rule check: all requirements must be keys in context with True value
            req = scroll.get("requirement")
            passed = context.get(req, False)
            results[key] = {"requirement": req, "passed": passed, "weight": scroll.get("impact_weight", 1)}
        return results
