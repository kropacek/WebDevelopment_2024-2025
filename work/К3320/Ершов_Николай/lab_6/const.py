from domain.dto.command import CommandTypes
from logic.command_handler import CommandHandler
from logic.utils.math_operations import MathOperations

__all__ = (
    "command_handlers_mapping",
    "math_operations_mapping",
)


command_handlers_mapping = {
    CommandTypes.GREETINGS: CommandHandler.handle_say_hello,
    CommandTypes.MATHEMATICS: CommandHandler.handle_mathematics,
    CommandTypes.CHAT: CommandHandler.handle_chat,
}

math_operations_mapping = {
    "1": MathOperations.pythagoras,
    "2": MathOperations.quadratic,
    "3": MathOperations.trapezoid_area,
    "4": MathOperations.parallelogram_area,
}
