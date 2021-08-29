## Install BT2 Debian
https://packages.debian.org/sid/amd64/python3-bt2/download

## <class 'bt2.message._EventMessageConst'>
['__class__', '__copy__', '__deepcopy__', '__del__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_borrow_default_clock_snapshot', '_borrow_event', '_check_has_default_clock_class', '_create_from_ptr', '_create_from_ptr_and_get_ref', '_event_pycls', '_get_default_clock_snapshot', '_get_ref', '_ptr', '_put_ref', 'addr', 'default_clock_snapshot', 'event']

## <class 'bt2.event._EventConst'>

['__class__', '__copy__', '__deepcopy__', '__del__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_borrow_class_ptr', '_borrow_common_context_field_ptr', '_borrow_packet_ptr', '_borrow_payload_field_ptr', '_borrow_specific_context_field_ptr', '_borrow_stream_ptr', '_create_field_from_ptr', '_create_from_ptr_and_get_ref', '_event_class_pycls', '_owner_get_ref', '_owner_ptr', '_owner_put_ref', '_packet_pycls', '_ptr', '_stream_pycls', 'addr', 'cls', 'common_context_field', 'id', 'name', 'packet', 'payload_field', 'specific_context_field', 'stream']

### Example
addr:  13445376
common_context_field:  None
id:  9
name:  comp
packet:  <bt2.packet._PacketConst object @ 0xcd25a0>
payload_field:  {'vmid': 0, 'baseid': 0, 'name': 'esm', 'IPM': 'IPDv02p1=2||IPDv02p3=3||IPDv02p5=4||ExternalAdvertise=5||ExternalRealize=6||ExternalDataInitialize=7', 'RPM': 'RunPhase1=1', 'FPM': 'FinalizePhase1=1||ExternalFinalizeReset=2'}
specific_context_field:  None
stream:  <bt2.stream._StreamConst object @ 0xcc8010>

## <class 'bt2.stream._StreamConst'>
['__class__', '__copy__', '__deepcopy__', '__del__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_borrow_class_ptr', '_borrow_trace_ptr', '_borrow_user_attributes_ptr', '_create_from_ptr', '_create_from_ptr_and_get_ref', '_create_value_from_ptr_and_get_ref', '_get_ref', '_ptr', '_put_ref', '_stream_class_pycls', '_trace_pycls', 'addr', 'cls', 'id', 'name', 'trace', 'user_attributes']

### Example
id:  3
addr:  22379424
cls:  <bt2.stream_class._StreamClassConst object @ 0x1543490>
name:  /home/rlong/Sandbox/esmf-profiler/test-traces/atm-ocn/esmf_stream_0003
trace:  <bt2.trace._TraceConst object @ 0x14b3080>
user_attributes:  {}

## <class 'bt2.trace._TraceConst'>
['__abstractmethods__', '__class__', '__class_getitem__', '__contains__', '__copy__', '__deepcopy__', '__del__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__setattr__', '__sizeof__', '__slots__', '__str__', '__subclasshook__', '__weakref__', '_abc_impl', '_borrow_class_ptr', '_borrow_stream_ptr_by_id', '_borrow_stream_ptr_by_index', '_borrow_user_attributes_ptr', '_create_from_ptr', '_create_from_ptr_and_get_ref', '_create_value_from_ptr_and_get_ref', '_get_ref', '_ptr', '_put_ref', '_stream_pycls', '_trace_class_pycls', '_trace_env_pycls', 'add_destruction_listener', 'addr', 'cls', 'environment', 'get', 'items', 'keys', 'name', 'remove_destruction_listener', 'user_attributes', 'uuid', 'values']

