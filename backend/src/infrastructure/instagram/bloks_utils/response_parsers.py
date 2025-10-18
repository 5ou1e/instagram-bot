import json
from dataclasses import dataclass
from typing import Union

from src.domain.shared.interfaces.instagram.entities.challenge import ChallengeData
from src.domain.shared.interfaces.instagram.exceptions import BadResponseError
from src.infrastructure.instagram.bloks_utils.utils import (
    deserialize_bloks_action,
    find_action,
    parse_nested_json,
)


@dataclass
class SuccessLoginResult:
    login_response_data: dict


@dataclass
class ChallengeRequiredLoginResult:
    challenge_data: ChallengeData


@dataclass
class TwoStepVerificationRequiredLoginResult:
    data: dict


@dataclass
class UnknownLoginResult:
    response: dict


def parse_bloks_login_response(
    response: dict,
) -> Union[SuccessLoginResult, ChallengeRequiredLoginResult, UnknownLoginResult, TwoStepVerificationRequiredLoginResult]:
    action_string = (
        response.get("layout", {}).get("bloks_payload", {}).get("action", "")
    )
    if not action_string:
        raise BadResponseError(message="Отсутствует поле action в BloksLogin response")

    try:
        action = deserialize_bloks_action(action_string)
    except Exception as e:
        raise BadResponseError(
            message=f"Не удалось десериализовать bloks action: {action_string}"
        )

    # Сначала ищем успешный логин
    handle_login_response_action = find_action(
        action, "bk.action.caa.HandleLoginResponse"
    )
    if handle_login_response_action:
        return SuccessLoginResult(
            login_response_data=extract_login_response_data_from_action(
                handle_login_response_action
            )
        )

    two_step_verification_action = find_action(
        action, arg_value="com.bloks.www.ap.two_step_verification.entrypoint_async"
    )

    if two_step_verification_action:
        data = extract_two_step_verification_action_data(two_step_verification_action)
        return TwoStepVerificationRequiredLoginResult(data=data)

    # Если нет успешного логина, ищем checkpoint
    checkpoint_action = find_action(action, "bk.action.caa.PresentCheckpointsFlow")
    if checkpoint_action:
        challenge_data = extract_challenge_data_from_action(checkpoint_action)
        return ChallengeRequiredLoginResult(challenge_data=challenge_data)

    # Если ничего не нашли
    return UnknownLoginResult(response=response)


def extract_two_step_verification_action_data(
    two_step_verification_action: list,
) -> dict:
    try:
        map_make = find_action(
            two_step_verification_action, action_name="bk.action.map.Make"
        )

        names = [val for val in map_make[1][1:]]
        values = [val for val in map_make[2][1:]]
        return {k: v for k, v in zip(names, values)}
    except Exception as e:
        raise BadResponseError(
            message="Не удалось извлечь данные для two_step_verification_action"
        )


def extract_login_response_data_from_action(handle_login_response_action: list) -> dict:
    try:
        tree_make = find_action(handle_login_response_action, "bk.action.tree.Make")
        if tree_make:
            login_response_string = tree_make[3]
            return parse_nested_json(login_response_string)
    except Exception:
        pass

    raise BadResponseError(
        message="Не удалось извлечь login_response_data из HandleLoginResponse action"
    )


def extract_challenge_data_from_action(checkpoint_action: list) -> ChallengeData:
    challenge_data = json.loads(checkpoint_action[1])["error"]["error_data"]
    return ChallengeData(**challenge_data)
