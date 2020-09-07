import glob
from music21 import stream
import numpy as np

import process_notes
import create_model
import make_prediction

def generate_song(notes, song_type, model_type):
    midi_stream = stream.Stream(notes)
    music_name = model_type + " - Notes - " + song_type + " Music.mid"
    midi_stream.write('midi', fp=music_name)

def get_notes(song_type, nb, seg):
    song_dir = "../data/"+song_type

    notes = []

    for file in glob.glob(song_dir+"/*.midi"):
        notes = notes + process_notes.divide_notes(file, nb, seg)

    notes = process_notes.remove_freq(notes)

    return notes

def predict_generate(nb, notes, song_type, model_type, nb_epochs, batch_size):

    weights_dir = "../model_weights/"+ model_type.upper()

    n_vocab, net_inp, net_out, pitch = process_notes.create_seq(notes)

    model = create_model.create_model(n_vocab, net_inp, model_type)

    fitted_model = create_model.model_fit(model, net_inp, net_out, nb_epochs, batch_size, song_type, nb, model_type, weights_dir)
  
    prediction_notes = make_prediction.generate_notes(fitted_model, net_inp, pitch, n_vocab, nb)

    return prediction_notes

def main():
    nb_epochs = 100
    batch_size = 64
    nb = 2

    song_type = ["Battle", "Route", "Buildings"]
    model_type = "FINAL" # ["LSTM", "GRU", "FINAL"]

    for theme in song_type:
        if model_type == "FINAL":
            notes_n1 = get_notes(song_type, nb, 1)
            notes_n2 = get_notes(song_type, nb, 2)

            prediction_n1 = predict_generate(1, notes_n1, theme, model_type, nb_epochs, batch_size)
            prediction_n2 = predict_generate(2, notes_n2, theme, model_type, nb_epochs, batch_size)

            output_notes = np.concatenate((prediction_n1, prediction_n2))

            gen_out_notes = make_prediction.transform_to_m21(output_notes, theme)

            generate_song(gen_out_notes, theme, model_type)

        else:
            nb = 1
            notes = get_notes(song_type, nb, 1)

            prediction_notes = predict_generate(nb, notes, theme, model_type, nb_epochs, batch_size)

            output_notes = make_prediction.transform_to_m21(prediction_notes, theme)

            generate_song(output_notes, theme, model_type)