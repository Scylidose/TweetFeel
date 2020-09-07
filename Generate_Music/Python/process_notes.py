from music21 import converter, instrument, note, chord, stream
import music21

import numpy as np
from keras.utils import np_utils

import pandas as pd
from scipy import stats

from collections import Counter

from sklearn.model_selection import train_test_split

def no_divide_notes(file):
  notes = []
  midi = converter.parse(file)
  notes_to_parse = None
  parts = instrument.partitionByInstrument(midi)
  if parts: # file has instrument parts
    notes_to_parse = parts.parts[0].recurse()
  else: # file has notes in a flat structure
    notes_to_parse = midi.flat.notes

  for element in range(0, len(notes_to_parse)):
    if isinstance(notes_to_parse[element], music21.note.Note):
      notes.append(str(notes_to_parse[element].pitch))
    elif isinstance(notes_to_parse[element], chord.Chord):
      notes.append('.'.join(str(n) for n in notes_to_parse[element].normalOrder))

  return notes

def divide_notes(file, nb, seg):
  notes = []

  midi = converter.parse(file)
  notes_to_parse = None
  parts = instrument.partitionByInstrument(midi)

  if parts: # file has instrument parts
    notes_to_parse = parts.parts[0].recurse()
  else: # file has notes in a flat structure
    notes_to_parse = midi.flat.notes

  threshold = int(len(notes_to_parse)/nb)

  for element in range(0, len(notes_to_parse)):

    if element >= threshold * (seg-1) and element < threshold * seg:
      if isinstance(notes_to_parse[element], music21.note.Note):
        notes.append(str(notes_to_parse[element].pitch))
      elif isinstance(notes_to_parse[element], chord.Chord):
        notes.append('.'.join(str(n) for n in notes_to_parse[element].normalOrder))

  return notes


def remove_freq(notes):
  freq = dict(Counter(notes))
  no=[count for _,count in freq.items()]

  no_zscore = np.absolute(stats.zscore(no)) < 2.7

  for i in range(len(freq.keys())):
    freq[list(freq.keys())[i]] = [list(freq.values())[i], no_zscore[i]]

  frequent_notes = [note_ for note_, count in freq.items() if count[1]]

  new_music=[]
  for note in notes:

      if note in frequent_notes:
        new_music.append(note)          
      
  return new_music

def create_seq(notes):
  sequence_length = 100

  # get all pitch names
  pitchnames = sorted(set(item for item in notes))
  # create a dictionary to map pitches to integers
  note_to_int = dict((note, number) for number, note in enumerate(pitchnames))

  network_input = []
  network_output = []
  n_vocab = len(np.unique(notes))

  # create input sequences and the corresponding outputs
  for i in range(0, len(notes) - sequence_length, 1):
      sequence_in = notes[i:i + sequence_length]
      sequence_out = notes[i + sequence_length]

      network_input.append([note_to_int[char] for char in sequence_in])
      network_output.append(note_to_int[sequence_out])
      
  n_patterns = len(network_input)
  # reshape the input into a format compatible with LSTM layers
  network_input = np.reshape(network_input, (n_patterns, sequence_length, 1))
  # normalize input
  network_input = network_input / float(n_vocab)
  network_output = np_utils.to_categorical(network_output)

  return n_vocab, network_input, network_output, pitchnames

def split_notes(net_inp, net_out):
    return train_test_split(net_inp, net_out, test_size=0.2, random_state=0)
