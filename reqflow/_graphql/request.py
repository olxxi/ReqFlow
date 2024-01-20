class GraphQLRequest:
    def __init__(self, operation: str, variables: dict = None, is_mutation: bool = False):
        self.operations = operation
        self.variables = variables
        self.is_mutation = is_mutation

    @property
    def payload(self):
        # if self.operations is None or self.operations == "":
        #     raise ValueError("The query is required")

        # Return the request payload in the format expected by the GraphQL server
        return {"query": self.operations, "variables": self.variables}
