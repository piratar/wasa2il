# wasa2il - ‫وسائل

Wasa2il is a participatory democracy software project. It is based around the core
idea of polities - political entities - which users of the system can join or leave, 
make proposals in, alter existing proposals, and adopt laws to self-govern.

The goal of this is to make it easy for groups on any scale - from the local 
whiskey club to the largest nation - to self-organize and manage their intents,
goals and mutual understandings.


## Polities

A polity is a political entity which consists of a group of people and a set of laws
the group has decided to adhere to. In an abstract sense, membership in a polity
grants a person certain rights and priviledges. For instance, membership in a 
school's student body may grant you the right to attend their annual prom,
and membership in a country (i.e. residency or citizenship) grants you a right 
to live there and do certain things there, such as start companies. stand in 
elections, and so on.

Each polity has different rules - these are also called statutes, bylaws or laws - 
which affect the polity on two different levels.

Firstly, there are meta-rules, which describe how rules are formed, how
decisions are made, how meetings happen, and how governance in general 
happens. Wasa2il has to be flexible enough to accomodate the varying 
meta-rules of a given polity, otherwise the polity may decide that Wasa2il isn't 
useful to them. Sometimes these rules are referred to as "rules of procedure" 
or "constitution", depending on the type of polity which is using them.

Secondly there are external rules, which are the decisions the polity makes which
don't affect its internal decisionmaking process.

Wasa2il needs to have the capacity to manage both types of rules and present
both in a coherent and comprehensive way. In particular, there needs to be an
available list of the laws which the polity has adopted, and changes to those
laws which have meta-effects must alter the way Wasa2il works for that polity.

## Topics, Issues, Documents and Votes

Within any polity, there can be any number of different topics that need to be
discussed. The members of a polity decide which topics are relevant to them.
The way in which this is decided depends on the meta-rules of the polity.

Topics are used to manage and display a list of issues. Issues are conversations
which have been brought to discussion within a polity, and can belong to 
numerous topics. The purpose of an issue and its associated conversation is to
arrive at a decision. The decision is represented by a document which can be
adopted or rejected.

Documents which have been adopted represent the law of the polity. Sometimes
laws need to change, so it needs to be possible to propose changes to a law
even after it has been adopted. Doing so would cause a new issue to be raised
and deliberated on.

The decision making process is normally concluded by a vote. Votes can take
many forms. There are multiple methods of voting and multiple ways of calculating
the results. While in most cases the correct approach for the creation of new
laws would be to decide on one unique result.

[As a side: If faced with multiple options for a particular article, for instance, the
Condorcet method may be the best way to get an acceptable result. It might even
be determined that if no Condorcet winner exists amongst the proposals, there
should be some process to push closer to a consensus. This is tricky, as if the
Schultze method is simply used to create a winner there could be a complaint that
results are being forced out, whereas if there is a simple method to postpone an
issue indefinitely opponents could gang up to game the system and eliminate the
possibility of a Condorcet winner. Some middle ground should exist, and Wasa2il
should support the creation of that.]

# Installation

## Locally

    make init
    make run

`make init` will setup a local virtualenv for the python dependencies, and then
run the `initial_setup.py` script which prompts for a username, e-mail and
password of the first (admin) user, which get added to the sqlite database.
`make run` runs the server using the python executable from the previously
installed virtualenv.


## Docker

    docker build -t piratar/wasa2il .
    docker run --name wasa2il-dev-container -p 8000:8000 -it piratar/wasa2il

The first command builds a new docker image and gives it the name `piratar/wasa2il`
The second command starts a new docker container based of the latest version
of the `piaratar/wasa2il` image, forwards port 8000 of the docker host to the
same port on the docker container, and names it `wasa2il-dev-container`.  The
Docker CMD command runs `initial_setup.py` so when running the container for
the first time you will be prompted for username, e-mail and password.

Since the sqlite database is created inside the container on the first run,
and not for example mounted through a volume, if you want your test data to
persist you must re-use the container after building it.  You can stop and
start the named container like so:

    docker stop wasa2il-dev-container

and

    docker start wasa2il-dev-container


## Debian

see instructions: INSTALL.Debian.txt

But in general, just run python initial_setup.py and you will be all set.
