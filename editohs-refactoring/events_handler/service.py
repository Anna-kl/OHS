import functools
import json

from enums.type_of_object import TypeOfObject

from models.vf.armed_force import ArmedForce

from services.classes.event_store_class import EventStoreVf


@define
class HandlerService:
    data_object: object
    data_command: CommandService

    def __init__(self, data_event):
        try:
            type_of_object = TypeOfObject[data_event['type_of_object']]
            data_of_object = json.loads(data_event['data'])
        except:
            pass
        self.process = singledispatch(self.test_method)
        self.process.register(int, self._process_vf)
        self.test_method.register(list, self._test_method_list)

    def process(self, arg, verbose=False):
        if verbose:
            print("Let me just say,", end=" ")

        print(arg)
        
    def _process_vf(self, arg: ArmedForce, *args):
        event_store = EventStoreVf(arg, args[0])
        return event_store.process()

# def load_event(data_event):
#     type_of_object = TypeOfObject[data_event['type_of_object']]
#     data_of_object = json.loads(data_event['data'])
#     if type_of_object == type_of_object.VF:
#         vf = ArmedForce(**data_of_object)
#     return process_event(vf, data_event)
# 
# 
# @functools.singledispatch
# def process_event(arg, *args):
#     raise NotImplementedError
# 
# 
# @functools.singledispatch
# def load_data(arg, *args):
#     raise NotImplementedError
# 
# 
# @process_event.register
# def _(arg: ArmedForce, *args):
#     event_store = EventStoreVf(arg, args[0])
#     return event_store.process()
