from lib.bot import bot

VERSION = "0.0.13-alpha.1"

# class InterceptHandler(logging.Handler):
#     def emit(self, record):
#         # Get corresponding Loguru level if it exists
#         try:
#             level = log.level(record.levelname).name
#             if level == "DEBUG":
#                 level = log.level("TRACE").name
#         except ValueError:
#             level = record.levelno
#
#         # Find caller from where originated the logged message
#         frame, depth = logging.currentframe(), 2
#         while frame and frame.f_code.co_filename == logging.__file__:
#             frame = frame.f_back
#             depth += 1
#
#         log.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())
#
#
# logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

bot.run(VERSION)
