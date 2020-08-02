# external class/method imports
from typing import final

# syft imports
from .serializable import Serializable
from ...proto.core.common.object_pb2 import ProtoObjectWithId
from .uid import UID


@final
class AbstractObjectWithID(Serializable):
    """This exists to allow us to typecheck on the ObjectWithId object
    because we need a type which has already been initialized in
    order to add it as a type hint on the ObjectWithId object.
    """

@final
class ObjectWithId(AbstractObjectWithID):
    """This object is the superclass for nearly all Syft objects. Subclassing
    from this object will cause an object to be initialized with a unique id
    using the process specified in the UID class.

    .. note::
        At the time of writing, the only class in Syft which doesn't have an ID
        of some kind is the Client class because it's job is to point to another
        object (which has an ID).

    """

    def __init__(self, id: UID = None, as_wrapper:bool=False):
        """This initializer only exists to set the id attribute, which is the
        primary purpose of this class. It also sets the 'as_wrapper' flag
        for the 'Serializable' superclass.

        :param id: an override which can be used to set an ID for this object
            manually. This is probably only used for deserialization.
        :type id: UID
        :param as_wrapper: this flag determines whether the subclass can also
            be used as a wrapper class around a non-syft object. For details on
            why, see :py:mod:`syft.core.common.serializable.Serializable`.

        """

        # while this class is never used as a simple wrapper,
        # it's possible that sub-classes of this class will be.
        super().__init__(as_wrapper=as_wrapper)

        if id is None:
            id = UID()

        self.id = id

    def serialize(self):
        return ProtoObjectWithId(id=self.id.serialize())

    @staticmethod
    def deserialize(proto_obj: ProtoObjectWithId) -> AbstractObjectWithID:
        return ObjectWithId(id=UID.deserialize(proto_obj.id))
