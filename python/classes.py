from function import Function

class NClass:
	def __init__(self, name, types, values, constructors, public=False):
		self.name = name
		self.types = types
		self.values = values
		self.constructors = constructors
		self.public = public

	def call_constructor(self, *args):
		pass
		# Calls contructor and returns a record of values and things

class NConstructor(Function):
	def __init__(self, scope, args, body, public=False, argument_cache=None):
		super().__init__(scope, args, None, body, public=public)
		self.argument_cache = argument_cache or []

	async def run(self, arguments):
		arguments = self.argument_cache + arguments
		if len(arguments) < len(self.arguments):
			return NConstructor(
				self.scope,
				self.arguments,
				self.codeblock,
				public,
				argument_cache=self.argument_cache
			)

		scope = self.scope.new_scope(parent_function=None)
		for value, (arg_pattern, _) in zip(arguments, self.arguments):
			scope.assign_to_pattern(arg_pattern, value)
		await scope.eval_command(self.codeblock)
		class_instance = {}
		for prop_name, var in scope.variables.items():
			if var.public:
				class_instance[prop_name] = var.value
		return class_instance