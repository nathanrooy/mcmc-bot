import pickle
import zipfile

from random import choice, choices

STATE_SIZE = 3


def mc(p, max_len=400) -> str:
    # pick a starting state
    seed = choice([k for k in p.keys() if "<START>" in k])

    # generate markov trajectory
    output = list(seed)
    for i in range(500):
        # terminate on the absorption state.
        if output[-1] == "<END>":
            break

        # parse the current state
        current_state = tuple(output[i : i + STATE_SIZE])

        # populate the transition space
        next_states = list(p[current_state].items())

        # if needed, extend the transition space by reducing the state size
        if len(next_states) == 1 and next_states[0][1] == 1:
            for next_state in p.keys():
                if next_state[1:] == current_state[1:] and next_state != current_state:
                    for state in p[next_state].items():
                        next_states.append(state)

        # pick next state
        if len(next_states) == 1:
            output.append(next_states[0][0])
        else:
            s, w = zip(*next_states)
            output.append(choices(s, weights=w, k=1)[0])

    # some minimal formatting
    final = ""
    for i, word in enumerate(output[1:-1]):
        if word == "<NL>":
            final = final[:-1]
            final += "\n\n"
        else:
            final += word + " "

    return final[:-1]


def create_post():

    # load the transition matrix
    with zipfile.ZipFile("data/p.pkl.zip", "r") as zf:
        with zf.open("p.pkl", "r") as f:
            p = pickle.load(f)

    # construct new post
    while True:
        msg = mc(p)
        if len(msg) < 300:
            print(f"> {msg}")
            break

    return msg
