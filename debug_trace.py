import sys
import inspect
import pprint

MODULES = {"settings_manager", "utils.s3_utils"}
pp = pprint.PrettyPrinter(indent=2, width=120, compact=True)

def tracer(frame, event, arg):
    if event not in ("call", "return"):
        return tracer

    module = inspect.getmodule(frame)
    if not module or module.__name__ not in MODULES:
        return tracer

    func_name = f"{module.__name__}.{frame.f_code.co_name}"

    if event == "call":
        print(f"-> {func_name}")
    elif event == "return":
        try:
            arg_str = pp.pformat(arg) if isinstance(arg, (dict, list, tuple)) else repr(arg)
        except Exception:
            arg_str = "<unreprable>"
        print(f"<- {func_name} returned {arg_str}")

    return tracer

# Activate profiler
sys.setprofile(tracer)

# Run the integration test
import test_s3_integration

test_s3_integration.test_s3_integration() 