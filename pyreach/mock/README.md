# PyReach Gym Unit Testing

Both the `pyreach/mock` and `pyreach/impl` directories provide implementations
of the PyReach Host API interfaces defined in the top-level `pyreach` directory.
The PyReach Gym sits on top of PyReach Host API and does not use any private
interfaces. The `pyreach/impl` directory provides an actual implementation that
communicates with both real and simulated robots. The `pyreach/mock` directory
provides a mock implementation is used exclusively for PyReach Gym unit testing.

There are many Python mock testing frameworks of varying complexity. The
"official" one is `mock` in the Python `unittest` package. This is an
action/assertion based framework. There are others that are a record/playback
based framework. For PyReach Gym, a record/playback framework is a better fit.
While there are plenty record/playback frameworks out there, finding one that
has on-going support is more problematic. After digging around, none of them
stood out as being the worth the risk adding a dependency on package that may
not ultimately be supported in the long run. Thus, the conclusion was use the
`unittest` `mock` or "do something else". "do something else" won.

Instead, a very simple strategy is used for Gym unit tests. The vast majority of
the tests are action/assertion. In fact, the vast majority of the interfaces can
return the same value every time they are called. Only a few need to return
different values each time they are called. So a very light weight playback
strategy is used for these other cases.

A two level dictionary scheme is used, where the first level is keyed on class
name and the second level is keyed on method name. For example:

```
 return_values = {
     "ArmMock": {
         "state": [ v1, v2, v3, ...]
     }
 }
 mock_hose: host.Host = host_mock.HostMock(return_values)
```

This is passed into the `HostMock` constructor at unit test Gym environment set
up time. The lower level mocks will read the return values and use them for each
method call. Thus, sequential calls to the ArmMock.state() method return `v1`,
`v2`, `v3`, ... in sequence.
