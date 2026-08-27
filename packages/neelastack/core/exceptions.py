class NeelastackError(Exception): pass
class AuthenticationError(NeelastackError): pass
class AuthorizationError(NeelastackError): pass
class ProviderError(NeelastackError): pass
class ToolDenied(NeelastackError): pass
