#!/usr/bin/env python3

import curses


class Hangman:
    def __init__(self, stdscr, max_tally=5):
        self.stdscr = stdscr
        self.tally = 0
        self.unused_letters = list('abcdefghijklmnopqrstuvwxyz')
        self.correct_letters = []
        self.max_tally = max_tally

    def end(self):
        self.stdscr.erase()
        self.stdscr.addstr(1, 0, 'Tally: '+str(self.tally) +
                           '/'+str(self.max_tally))
        self.stdscr.addstr(3, 0, 'The word was: '+self.input_str)
        if(self.tally == self.max_tally):
            self.stdscr.addstr(4, 0, 'You lose!')
        else:
            self.stdscr.addstr(4, 0, 'You win!')
        self.stdscr.getch()

    def request_word(self):
        curses.echo()
        self.stdscr.erase()
        self.stdscr.addstr("Enter your word to guess: ")
        self.input_str = self.stdscr.getstr().decode("utf-8")

    def start(self):
        self.stdscr.erase()
        self.request_word()
        for h in range(len(self.input_str)):
            self.stdscr.addstr(2, 2*h, '_')
        while(self.tally < self.max_tally and len(self.correct_letters) != len(self.input_str)):
            curses.noecho()
            self.stdscr.addstr(0, 0, ' '.join(self.unused_letters))
            self.stdscr.addstr(
                1, 0, 'Tally: '+str(self.tally)+'/'+str(self.max_tally))
            input_key = chr(self.stdscr.getch()).lower()
            input_key = input_key if 0 < ord(input_key)-96 < 27 else None
            if(input_key is None):
                continue
            if(not input_key in self.input_str and input_key in self.unused_letters):
                self.tally += 1
            else:
                indices = [i for i, x in enumerate(
                    self.input_str) if x == input_key]
                for j in indices:
                    self.correct_letters.append(self.input_str[j])
                    self.stdscr.addstr(2, 2*j, self.input_str[j])
            self.unused_letters[ord(input_key)-97] = ' '
        self.end()


def main(stdscr):
    stdscr.timeout(0)
    stdscr.nodelay(0)
    stdscr.refresh()
    game = Hangman(stdscr)
    game.start()


if(__name__ == '__main__'):
    curses.wrapper(main)
