from app.controllers.search_params_model import SearchParams


class SearchParamsBuilder:
    """This class extracts parameter values from request and saves them in a
    SearchParams dataclass object."""

    @staticmethod
    def map_request_parameters(request):
        # Extract all query parameters from the request
        request_params = request.query_params
        mapped_params = {}

        for param, param_value in request_params.items():
            mapped_params[param] = param_value
        return mapped_params

    @staticmethod
    def get_search_params(request):
        """Map the request parameters to match the Pydantic model's field name."""
        mapped_params = SearchParamsBuilder.map_request_parameters(request)
        params = SearchParams(**mapped_params)
        return params