Our simulwatches of video entertainment will blot out the sun.

<A name="toc1-2" title="Technical Notes" />
# Technical Notes

    $ ./simul_slave.py tcp://*:4000 tcp://*:4001 toba


    >>> master = simulproto.Master('tcp://*:4000', 'tcp://*:4001')
    >>> master.all_slaves
    []
    >>> master.step()
    >>> master.all_slaves
    [u'toba']
