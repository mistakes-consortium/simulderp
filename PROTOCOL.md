<A name="toc1-0" title="Roles" />
# Roles

There are two roles; one, the master node, and two, the slave nodes.  The master node is also the program running the IRC bot, which is how the users control and influence the bot and thus, the media players - which are under control of the slaves.  The slave nodes will also scan a directory for files, allowing the master node to request updates on the presence or non-presence of certain files.

<A name="toc1-5" title="Buses" />
# Buses

Both buses will be tcp sockets bound on the master node.  Slaves will connect to it.  All messages shall be JSON.

General message format:

    {
      'mtype' : ...
      'src' : ... (only for advise bus)
      'dest' : ... (optional, when not set commands are global, only for command bus)
      ...
    }

<A name="toc2-19" title="Advise Bus" />
## Advise Bus

The Advise bus will be a ZeroMQ SUB socket, bound at the master.  The slaves will advise the master of their status and file state using this bus.

<A name="toc3-24" title="slave_ready" />
### slave_ready

No special args.  Should be sent every 5 seconds at least, to let the master know everyone is ready.  This means that the slave is ready to recieve commands, and has nothing to do with the user's willingness to play the file immediately, or any file presence.

<A name="toc3-29" title="slave_exit" />
### slave_exit

No special args.

<A name="toc3-34" title="file_status" />
### file_status

Args: `filename`, `ts`

* `filename`
* `ts` shall be a gmt unix timestamp in seconds which is the greater of create time or modification time.

<A name="toc3-42" title="simul_started" />
### simul_started

Args: `filename`

As soon as the file playback is begun, this should be sent.  This lets the master node keep track that the playback started properly.

<A name="toc3-49" title="simul_notstarted" />
### simul_notstarted

Args: `filename`, `reason`

The master sent a simul-file command and the slave couldn't.  A reason should be specified.  The reason shall be text.

<A name="toc3-56" title="simul_playcompleted" />
### simul_playcompleted

Args: `filename`

As soon as file playback is completed, this should be sent.  This lets the master node announce that the playback completed.  Optional.

<A name="toc2-63" title="Command Bus" />
## Command Bus

The Command bus will be a ZeroMQ SUB socket bound on the master node.  Slaves will connect to it, and obey its commands.

<A name="toc3-68" title="simul_file" />
### simul_file

Args: `filename`

When this message is recieved, the slave should start looking for the file specified, and drop any tasks that are currently operating, except for a running media play.  `file-status` messages should be sent periodically to report on such status.

<A name="toc3-75" title="simul_start" />
### simul_start

Args: `filename`

When this message is recieved, the file should start playing immediately.  The slaves should all respond with either simul-started or simul-notstarted as soon as possible.

<A name="toc3-82" title="simul_stop" />
### simul_stop

Args: `filename`

When this message is recieved, someone was a jerk and failed to conform to proper simulwatching procedure in some manner, so it was decided that the simul would be stopped for the time being, to be restarted later.
