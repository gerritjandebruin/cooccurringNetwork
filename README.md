# cooccurringNetwork

This is a simple package that allows to create a so-called co-occurring network
from event data. In short, such a network maps events that occur at (almost) the
same time. Optionally, it could also be constraint such that only events at the 
same location at the same time are mapped. Hence a spatio-temporal network is 
obtained. 

This package makes use of the 
[NetworkX library](https://networkx.org/documentation/stable/). 

## Installation
This package can be directly installed using pip and git:
```
pip install git+https://github.com/gerritjandebruin/cooccurringNetwork/
```
This package does use Python >= 3.9.0, as well as networkx, pandas and tqdm.
The dependencies are automatically installed, when using the pip install
command.

## Usage
There are two classes, Event and Cooccurrence. The Event class can be created
like this:
```python
time = pd.Timestamp(year=2017, month=1, day=1, hour=12)
eventA = Event(
  Index=0, entity='John Doe', time=time, attributes=dict(a=1), location='NY'
)
eventB = Event(1, 'Jane Doe', time=time, attributes=dict(a=2), location='NY')
eventC = Event(2, 'Jane Doe', time=time, attributes=dict(a=2), location='W')
``` 

The function `getCooccurences` allows to obtain a list of all co-occurences of 
two events:
```python
events = [eventA, eventB, eventC]
cooccurences = get_cooccurrences(events, max_timedelta=pd.Timedelta('1m'))
```

Since this can obtain a lot of random co-occurence events because two entities
happen by change on the same time, there is also a function 
`divide_cooccurences`. This function checks whether co-occurences happen 
multiple times separated by a minimum time gap.

## More information
This package was used in a publication at the 
[2019 Complex Networks Conference](https://www.2019.complexnetworks.org/index).

## Attribution
If you use this package in a publication, please cite:
> de Bruin G.J., Veenman C.J., van den Herik H.J., Takes F.W. (2020) Understanding Dynamics of Truck Co-Driving Networks. In: Cherifi H., Gaito S., Mendes J., Moro E., Rocha L. (eds) Complex Networks and Their Applications VIII. COMPLEX NETWORKS 2019. Studies in Computational Intelligence, vol 882. Springer, Cham. https://doi.org/10.1007/978-3-030-36683-4_12
