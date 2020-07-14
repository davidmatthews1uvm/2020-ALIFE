from __future__ import print_function

import os
import sys
import time
from builtins import input

sys.path.insert(0, '..')

import sqlite3 as lite
import pickle


class Word2VecVectorSpace(object):
    def __init__(self, database_file):
        self.database_file = database_file
        self.con = lite.connect(database_file)
        self.cur = self.con.cursor()

    def get_vector(self, word):
        """
        Searches for the vector representing the given string

        :param word: String to locate vector for
        :return: Numpy array of the vector corresponding to the word.
        If no corresponding vector is found, rasies a KeyError Exception
        ;rtype: numpy.ndarray
        """
        string = "SELECT * FROM Vectors WHERE name=?"
        params = (word,)
        self.cur.execute(string, params)
        raw_vector = self.cur.fetchone()
        if raw_vector is None:
            raise KeyError("Vector not found")
        else:
            vector = pickle.loads(raw_vector[1])
        return vector

    def build_database(self, w2v_file, binary_file=True, print_progress=False):
        try:
            from gensim.models import KeyedVectors
        except ImportError:
            print()
            print("ERROR! ABORTING:")
            print("You need to install gensim in order to generate a word2vec database.")
            print("Please view the README.md for more information.")
            exit(1)

        def add_vector(name, vec):
            self.cur.execute("insert into Vectors values (?,?)", (name, pickle.dumps(vec, protocol=0)))
            self.con.commit()

        def reset_database():
            self.cur.execute("drop table if exists Vectors")
            self.cur.execute("create table Vectors(name TEXT, vector BLOB)")

        def add_indexes():
            self.cur.execute("CREATE UNIQUE INDEX IF NOT EXISTS nameindex ON Vectors (name)")

        reset_database()
        word_vectors = KeyedVectors.load_word2vec_format(w2v_file, binary=binary_file)
        numb = 0

        for key in word_vectors.vocab:
            if numb % 2500 == 0 and print_progress:
                print("imported %d of %d vectors" % (numb, len(word_vectors.vocab)))
                sys.stdout.flush()
            numb += 1
            metadata = word_vectors.vocab[key]
            vec = word_vectors.vectors[metadata.index]
            add_vector(key, vec)
        add_indexes()

def display_menu():
    print("\n")
    print("word2vec database management tool")
    print("Type [N]ew to create a new database")
    print("Type [F]ind to search for a word embedding in the vector space")
    print("Type [C]ompare to compare two word embedings")
    print("Type [P]rint to print a word embedding")
    print("Type [E] to exit")
    print("")

if __name__ == "__main__":
    from scipy import spatial

    db = Word2VecVectorSpace(database_file='../database/w2vVectorSpace-google.db')

    cmd = ''
    while cmd.rstrip().upper() != "E":
        display_menu()
        cmd = input("Please type a command: ")
        if cmd.upper() == "N": # rebuild database
            print("Attention: rebuilding your vector space database will delete the current one. Please consider making a backup of your current database before proceeding.")
            confirm = input("Are you sure you want to build a new vector space database? y/[n]: ")
            if confirm.upper() != 'Y':
                print("Aborting rebuild process")
                continue
            file_name = input("Please enter the name of the word2vec embedding file: ")
            binary_raw = input("Is this file in a [b]inary or [t]xt format [b] or [t]: ")
            binary = None
            if binary_raw.upper() == "B":
                binary = True
            elif binary_raw.upper() == "T":
                binary = False
            else:
                print("Aborting rebuild process")
                continue
            confirm_proceed = input("This is the last chance to abort. Are you sure you would like to proceed? y/[n]: ")
            if confirm_proceed.upper() != 'Y':
                print("Aborting rebuild process")
                continue
            print("")
            print("Note: The first part of this process requires a lot of RAM. Please close non-essential programs.")
            print("")
            print("Starting rebuild process...")
            print("Loading in the vector space. This may take a while, please wait...")

            db.build_database(file_name, binary_file=binary, print_progress=True)

        if cmd.upper() == "F":
            word = input("Please type a word to look for: ")
            try:
                db.get_vector(word)
            except KeyError:
                print("Vector Not Found")
            else:
                print("Vector found!")
        elif cmd.upper() == "C":
            w1 = input("Please type a word1: ")
            try:
                v1 = db.get_vector(w1)
            except KeyError:
                print("Vector Not Found")

            else:
                w2 = input("Please type a word2: ")
                try:
                    v2 = db.get_vector(w2)
                except KeyError:
                    print("Vector Not Found")
                else:
                    print("Cos similarity is: ", 1 - spatial.distance.cosine(v1,v2))

        elif cmd.upper() == "P":
            w1 = input("Please type a word: ")
            try:
                v1 = db.get_vector(w1)
            except KeyError:
                print("Vector Not Found")

            else:
                print(v1)

