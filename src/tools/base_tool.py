class BaseTool:
    name = ""
    description = ""
    parameters = {}

    def run(self, **kwargs) -> str:
        raise NotImplementedError("Tool must implement run method.")
