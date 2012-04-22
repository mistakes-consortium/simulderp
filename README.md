Our simulwatches of video entertainment will blot out the sun.

<A name="toc1-2" title="Requirements" />
# Requirements

You need the packages listed in requirements.pip.  You can use virtualenv+pip with that file, or you can install them separately.

<A name="toc1-7" title="Technical Notes" />
# Technical Notes

    $ ./simul_slave.py tcp://*:4000 tcp://*:4001 toba


    >>> master = simulproto.Master('tcp://*:4000', 'tcp://*:4001')
    >>> master.all_slaves
    []
    >>> master.step()
    >>> master.all_slaves
    [u'toba']
