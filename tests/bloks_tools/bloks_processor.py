from typing import Any, Dict, List, Optional
from dataclasses import dataclass


@dataclass
class ExpansionContext:
    """Контекст для развертывания"""
    structure: 'BloksStructure'
    current_payload_id: Optional[str] = None
    arguments: Optional[List[Any]] = None


@dataclass
class BloksPayload:
    """Структура для хранения распарсенного payload"""
    action: Any
    ft: Dict[str, Any]
    referenced_vars: List[str]
    data: List[Dict[str, Any]]  # Добавляем поле data


@dataclass
class BloksStructure:
    """Полная структура распарсенного Bloks ответа"""
    main: BloksPayload
    embedded: Dict[str, BloksPayload]  # payload_id -> BloksPayload


class BloksExpander:
    """Развертывает Bloks структуры без выполнения"""

    def expand(self, structure: 'BloksStructure', action: Any = None) -> Any:
        """
        Разворачивает action используя структуру

        Args:
            structure: BloksStructure с распарсенными данными
            action: Action для развертывания (если None, берется main.action)

        Returns:
            Развернутая структура
        """
        if action is None:
            action = structure.main.action

        context = ExpansionContext(structure=structure)
        return self._expand_with_context(action, context, depth=0)

    def _expand_with_context(self, action: Any, context: ExpansionContext, depth: int = 0) -> Any:
        """
        Внутренний метод развертывания с контекстом
        """
        # Защита от слишком глубокой рекурсии
        if depth > 100:
            return action

        # Если это не список или пустой - возвращаем как есть
        if not isinstance(action, list) or len(action) == 0:
            return action

        action_name = action[0]

        # Обработка ссылок на ft функции
        if isinstance(action_name, str) and action_name.startswith('#'):
            if len(action) >= 2:
                # Разворачиваем аргументы перед передачей в ft функцию
                expanded_args = []
                for arg in action[1:]:
                    expanded_args.append(self._expand_with_context(arg, context, depth + 1))
                context.arguments = expanded_args
            return self._expand_ft_reference(action_name, context, depth + 1)

        # Обработка базовых функций для развертывания
        handlers = {
            'bk.action.map.Make': self._expand_map_make,
            'bk.action.array.Make': self._expand_array_make,
            'bk.action.core.GetArg': self._expand_get_arg,
            'bk.action.bloks.GetPayload': self._expand_get_payload,
            'bk.action.core.FuncConst': self._expand_func_const,
            'bk.action.bloks.GetVariable2': self._expand_get_variable,
            'bk.action.bloks.GetVariableWithScope': self._expand_get_variable,
        }

        if action_name in handlers:
            return handlers[action_name](action, context, depth)

        # Проверяем, является ли это вызовом функции с аргументами
        if self._is_function_call(action):
            return self._expand_function_call(action, context, depth)

        # Для остальных функций - рекурсивно разворачиваем аргументы
        expanded = [action_name]
        for item in action[1:]:
            expanded.append(self._expand_with_context(item, context, depth + 1))
        return expanded

    def _expand_ft_reference(self, ref: str, context: ExpansionContext, depth: int) -> Any:
        """Разворачивает ссылку на ft функцию"""
        ft_id = ref[1:]  # Убираем #

        # Поиск ft функции в порядке приоритета
        ft_action = None
        new_payload_id = context.current_payload_id

        # 1. Текущий payload
        if context.current_payload_id:
            payload = context.structure.embedded.get(context.current_payload_id)
            if payload and ft_id in payload.ft:
                ft_action = payload.ft[ft_id]

        # 2. Main payload
        if ft_action is None and ft_id in context.structure.main.ft:
            ft_action = context.structure.main.ft[ft_id]
            new_payload_id = None

        # 3. Все embedded payloads
        if ft_action is None:
            for payload_id, payload in context.structure.embedded.items():
                if ft_id in payload.ft:
                    ft_action = payload.ft[ft_id]
                    new_payload_id = payload_id
                    break

        # Не нашли - возвращаем как есть
        if ft_action is None:
            return ref

        # Создаем новый контекст и разворачиваем
        new_context = ExpansionContext(
            structure=context.structure,
            current_payload_id=new_payload_id,
            arguments=context.arguments  # Аргументы уже развернуты
        )
        return self._expand_with_context(ft_action, new_context, depth)

    def _expand_map_make(self, action: List, context: ExpansionContext, depth: int) -> Dict[
        str, Any]:
        """Разворачивает bk.action.map.Make в словарь"""
        if len(action) < 3:
            return {}

        keys = self._expand_with_context(action[1], context, depth + 1)
        values = self._expand_with_context(action[2], context, depth + 1)

        # Преобразуем в списки если нужно
        keys_list = keys if isinstance(keys, list) else [keys]
        values_list = values if isinstance(values, list) else [values]

        result = {}
        for i, key in enumerate(keys_list):
            if i < len(values_list):
                result[key] = values_list[i]

        return result

    def _expand_array_make(self, action: List, context: ExpansionContext, depth: int) -> List[Any]:
        """Разворачивает bk.action.array.Make в список"""
        return [self._expand_with_context(item, context, depth + 1) for item in action[1:]]

    def _expand_get_arg(self, action: List, context: ExpansionContext, depth: int) -> Any:
        """Разворачивает bk.action.core.GetArg"""
        if len(action) < 2:
            return None

        arg_index = action[1]
        if context.arguments and isinstance(arg_index, int) and 0 <= arg_index < len(
                context.arguments):
            # Возвращаем аргумент как есть - он уже развернут
            return context.arguments[arg_index]

        # Если аргумента нет - возвращаем placeholder
        return f"{{ARG_{arg_index}}}"

    def _expand_get_payload(self, action: List, context: ExpansionContext, depth: int) -> Any:
        """Разворачивает bk.action.bloks.GetPayload"""
        if len(action) < 2:
            return None

        payload_id = action[1]

        if payload_id not in context.structure.embedded:
            return f"{{PAYLOAD_{payload_id}_NOT_FOUND}}"

        payload = context.structure.embedded[payload_id]

        # Разворачиваем аргументы для payload
        expanded_args = []
        if len(action) > 2:
            for arg in action[2:]:
                expanded_args.append(self._expand_with_context(arg, context, depth + 1))

        # Создаем новый контекст для payload
        new_context = ExpansionContext(
            structure=context.structure,
            current_payload_id=payload_id,
            arguments=expanded_args if expanded_args else None
        )

        return self._expand_with_context(payload.action, new_context, depth + 1)

    def _expand_get_variable(self, action: List, context: ExpansionContext, depth: int) -> Any:
        """Разворачивает bk.action.bloks.GetVariable2/GetVariableWithScope"""
        if len(action) < 2:
            return None

        var_id = action[1]

        # Ищем переменную в data текущего payload или main
        variable_data = None

        # Проверяем в текущем payload
        if context.current_payload_id and context.current_payload_id in context.structure.embedded:
            payload = context.structure.embedded[context.current_payload_id]
            if payload.data:
                for data_item in payload.data:
                    if data_item.get('id') == var_id:
                        variable_data = data_item.get('data', {})
                        break

        # Проверяем в main
        if variable_data is None and context.structure.main.data:
            for data_item in context.structure.main.data:
                if data_item.get('id') == var_id:
                    variable_data = data_item.get('data', {})
                    break

        if variable_data:
            # Возвращаем данные переменной
            return {
                "type": "variable",
                "id": var_id,
                "data": variable_data
            }

        # Если не нашли - возвращаем placeholder
        return f"{{VAR_{var_id}}}"

    def _expand_func_const(self, action: List, context: ExpansionContext, depth: int) -> Any:
        """Разворачивает bk.action.core.FuncConst - просто возвращает константу"""
        if len(action) < 2:
            return None
        return action[1]

    def _is_function_call(self, action: List) -> bool:
        """Определяет, является ли action вызовом функции с аргументами"""
        if len(action) < 2:
            return False

        template = action[0]
        return isinstance(template, list) and self._contains_get_arg(template)

    def _contains_get_arg(self, item: Any) -> bool:
        """Проверяет, содержит ли элемент GetArg"""
        if not isinstance(item, list):
            return False

        if len(item) >= 1 and item[0] == 'bk.action.core.GetArg':
            return True

        return any(self._contains_get_arg(sub) for sub in item if isinstance(sub, list))

    def _expand_function_call(self, action: List, context: ExpansionContext, depth: int) -> Any:
        """Разворачивает вызов функции с подстановкой аргументов"""
        template = action[0]
        args = action[1:]

        # Сначала разворачиваем аргументы
        expanded_args = []
        for arg in args:
            expanded_args.append(self._expand_with_context(arg, context, depth + 1))

        # Создаем новый контекст с развернутыми аргументами
        new_context = ExpansionContext(
            structure=context.structure,
            current_payload_id=context.current_payload_id,
            arguments=expanded_args
        )

        return self._expand_with_context(template, new_context, depth + 1)