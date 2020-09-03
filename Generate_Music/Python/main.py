import glob
from music21 import stream

import Python.process_notes as process_notes
import Python.create_model as create_model
import Python.make_prediction as make_prediction

def generate_song(notes, song_type, model_type):
    midi_stream = stream.Stream(notes)
    music_name = model_type + " - Notes - " + song_type + " Music.mid"
    midi_stream.write('midi', fp=music_name)

def predict_generate(song_type, model_type, nb_epochs, batch_size):

    song_dir = "../data/"+song_type
    weights_dir = "../model_weights/"+ model_type.upper()

    notes = []

    for file in glob.glob(song_dir+"/*.midi"):
        notes += process_notes.no_divide_notes(file)

    n_vocab, net_inp, net_out, pitch = process_notes.create_seq(notes)

    X_train, X_val, y_train, y_val = process_notes.split_notes(net_inp, net_out)

    model = create_model.create_model(n_vocab, net_inp, model_type)

    fitted_model = create_model.model_fit(model, X_train, X_val, y_train, y_val, nb_epochs, batch_size, song_type, weights_dir)
  
    prediction_notes = make_prediction.generate_notes(fitted_model, net_inp, pitch, n_vocab)
    output_notes = make_prediction.transform_to_m21(prediction_notes, song_type)

    generate_song(output_notes, song_type, model_type)

def main():
    nb_epochs = 200
    batch_size = 64

    song_type = ["Battle", "Route", "Buildings"]
    model_type = ["LSTM", "GRU"]

    predict_generate(song_type[0], model_type[0], nb_epochs, batch_size)
