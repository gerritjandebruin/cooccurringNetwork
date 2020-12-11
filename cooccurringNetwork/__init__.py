from collections import deque
from typing import NamedTuple

from networkx import Graph
import pandas as pd
from tqdm import tqdm

class Event(NamedTuple):
  """
  Class containing an event. It has the following attributes:
  - Index                :     some unique integer
  - entityId             : unique identifier to the entity involved in the event
  - time
  - location   (optional)
  - attributes (optional): Any additional attributes can be stored in this dict.
  """
  Index: int
  entityId: str
  time: pd.Timestamp
  location: str = None
  attributes: dict

  
class Cooccurrence(NamedTuple):
  """
  Class mapping two events that were coinciding within deltaTime (optionally, at
  the same loc).
  """
  event: Event
  otherEvent: Event
  deltaTime: pd.Timedelta
  time: pd.Timestamp
  def __str__(self): 
    return (
      f'event     : {self.event}\n'
      f'otherEvent: {self.otherEvent}\n'
      f'deltaTime : {self.deltaTime}'
    )
  
def getCooccurrences(
  events: list[Event], *, deltaTimeMax: pd.Timedelta, verbose: bool = True
  ) -> list[Cooccurrence]:
  """
  Obtain a list of all co-occurences of two events, being at the same loc (when 
  that information is available) and within at most deltaTimeMax separation.
  """
  
  eventsPerLocation = dict()
  for event in events:
    if event.location not in eventsPerLocation: 
      eventsPerLocation[event.location] = list()
    eventsPerLocation[event.location].append(event)
  
  cooccurrences = list()
  queue = deque()
  kwargs = dict(disable=not verbose)
  for location, events in tqdm(eventsPerLocation.items(), position=0, **kwargs):
    for event in tqdm(events, position=1, desc=location, **kwargs):
      for otherEvent in queue.copy():
        if event.entityId != otherEvent.entityId:
          deltaTime = event.time - otherEvent.time
          if deltaTime < deltaTimeMax: 
            cooccurrences.append(
              Cooccurrence(
                event=event, otherEvent=otherEvent, deltaTime=deltaTime, 
                time=event.time
              )
            )
          else: queue.popleft()
      queue.append(event)
  return cooccurrences

def divideCooccurrences(
  cooccurrences: list[Cooccurrence], *, minGap: pd.Timedelta, verbose:bool=True
) -> tuple[list[Cooccurrence], list[Cooccurrence]]:
  """
  Divide a list of cooccurrencing events in systematic and random cooccurring
  events. An event is considered systematic if multiple events happen between 
  two entities with at minimum minGap time difference.
  
  Usage:
  systematic, random = divideCooccurrences(
    cooccurrences, minGap=pd.Timedelta(2, 'h')
  )
  """
  temp = dict()
  desc = 'Sort by identities'
  for cooccurrence in tqdm(cooccurrences, disable=not verbose, desc=desc):
    identities = tuple(
      sorted([cooccurrence.event.entityId, cooccurrence.otherEvent.entityId])
    )
    if identities not in temp: temp[identities] = list()
    temp[identities].append(cooccurrence)
    
  systematic = list()
  random = list()
  desc = 'Determine time gap'
  for _, cooccurrences in tqdm(temp.items(), disable=not verbose, desc=desc):
    cooccurrences.sort()
    if cooccurrences[-1].time - cooccurrences[0].time > minGap:
      systematic.extend(cooccurrences)
    else:
      random.extend(cooccurrences)
  return systematic, random 

def addEdge(graph: Graph, u: str, v: str) -> None:
  """Add edge to graph. If already exists, add one weight."""
  if not graph.has_edge(u,v): graph.add_edge(u, v, weight=1)
  else: graph.add_edge(u, v, weight=graph[u][v]['weight'] + 1)

def createGraph(cooccurrences: list[Cooccurrence]) -> Graph:
  """Create weighted graph from a sorted list of cooccurrences."""
  graph = Graph(None, final_date=None)
  for cooccurrence in cooccurrences:
    u = cooccurrence.event
    v = cooccurrence.otherEvent
    graph.add_node(u.entityId, time=u.time)
    graph.add_node(v.entityId, time=v.time)
    addEdge(graph, u.entityId, v.entityId)
  graph.graph['finalDate'] = cooccurrences[-1].time
  return graph
  
