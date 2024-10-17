import re
from datetime import date

from pydantic import BaseModel, field_validator, model_validator

from app.controllers.field_validation import (
    NUMERIC_FIELD_LIMITS,
    VALID_FIELD_VALUES,
)
from app.exceptions.exceptions import (
    InvalidParamError,
)
from app.utils.helpers import (
    check_params_are_none_except_excluded,
    clean_str,
    str_to_list,
)


class SearchParams(BaseModel):
    """Class for modeling search parameters"""

    page: int = 1
    per_page: int = 10
    commune: list | None = None
    code_postal: list | None = None
    forme_juridique: list | None = None

    # Field Validators (involve one field at a time)
    @field_validator("page", "per_page", mode="before")
    def cast_as_integer(cls, value: str, info) -> int:
        try:
            int(value)
        except ValueError:
            raise InvalidParamError(
                f"Veuillez indiquer un paramètre `{info.field_name}` entier."
            )
        return int(value)

    @field_validator(
        "page",
        "per_page",
        mode="after",
    )
    # Apply after first validator and Pydantic internal validation
    def check_if_number_in_range(cls, value, info):
        limits = NUMERIC_FIELD_LIMITS.get(info.field_name)
        if value < limits.get("min") or value > limits.get("max"):
            raise InvalidParamError(
                f"Veuillez indiquer un paramètre `{info.field_name}` entre "
                f"`{limits.get('min')}` et `{limits.get('max')}`, "
                f"par défaut `{limits['default']}`."
            )
        return value

    @field_validator(
        "forme_juridique",
        "commune",
        "code_postal",
        mode="before",
    )
    def convert_str_to_list(cls, str_of_values: str) -> list[str]:
        list_of_values = str_to_list(clean_str(str_of_values))
        return list_of_values

    @field_validator("code_postal", "commune", mode="after")
    def list_of_values_should_match_regular_expression(
        cls, list_values: list[str], info
    ) -> list[str]:
        for value in list_values:
            valid_values = VALID_FIELD_VALUES.get(info.field_name)["valid_values"]
            if not re.search(valid_values, value):
                raise InvalidParamError(
                    f"Au moins une valeur du paramètre {info.field_name} "
                    "est non valide."
                )
        return list_values

    @field_validator(
        "forme_juridique",
        mode="after",
    )
    def list_of_values_must_be_valid(cls, list_of_values: list[str], info) -> list[str]:
        valid_values = VALID_FIELD_VALUES.get(info.field_name)["valid_values"]
        for value in list_of_values:
            if value not in valid_values:
                raise InvalidParamError(
                    f"Au moins un paramètre "
                    f"`{VALID_FIELD_VALUES.get(info.field_name)['alias']}` "
                    f"est non valide. "
                    f"Les valeurs valides : {[value for value in valid_values]}."
                )
        return list_of_values

    # Model Validators (involve more than one field at a time)
    @model_validator(mode="after")
    def total_results_should_be_smaller_than_10000(self):
        page = self.page
        per_page = self.per_page
        if page * per_page > NUMERIC_FIELD_LIMITS["total_results"]["max"]:
            raise InvalidParamError(
                "Le nombre total de résultats est restreint à 10 000. "
                "Pour garantir cela, le produit du numéro de page "
                "(par défaut, page = 1) et du nombre de résultats par page "
                "(par défaut, per_page = 10), c'est-à-dire `page * per_page`, "
                "ne doit pas excéder 10 000."
            )
        return self

    @model_validator(mode="after")
    def check_if_all_empty_params(self):
        """
        If all parameters are empty (except matching size and pagination
        because they always have a default value) raise value error
        Check if all non-default parameters are empty, raise a InvalidParamError
        if they are
        """
        excluded_fields = [
            "page",
            "per_page",
        ]

        all_fields_are_null_except_excluded = check_params_are_none_except_excluded(
            self.dict(exclude_unset=True), excluded_fields
        )
        if all_fields_are_null_except_excluded:
            raise InvalidParamError(
                "Veuillez indiquer au moins un paramètre de recherche."
            )
        return self